from django.shortcuts import render
from django.http import JsonResponse
import requests
import os,json
from django.conf import settings 
from datetime import datetime, timedelta
from .models import ChatLog
from dotenv import load_dotenv
from django.utils.timezone import localtime
from collections import defaultdict
import uuid  # To generate unique chat IDs

# Load environment variables from .env file
load_dotenv()

# Access the OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")
def fetch_crypto_data():
    url = "https://api.coinlore.net/api/tickers/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["data"]  # Extract the list of crypto data
    else:
        print(f"Failed to fetch crypto data: {response.status_code}")
        return None

# Step 2: Format the data to include in the OpenAI system message
def format_crypto_data_for_openai(crypto_data, limit=5):
    # Limit the number of cryptocurrencies sent to avoid excessive context length
    limited_data = crypto_data[:limit]
    formatted_data = "Here is the latest crypto data:\n\n"
    for crypto in limited_data:
        formatted_data += (
            f"- {crypto['name']} ({crypto['symbol']}):\n"
            f"  symbol: ${crypto['symbol']}\n"
            f"  Price (USD): ${crypto['price_usd']}\n"
            f"  Market Cap: ${crypto['market_cap_usd']}\n"
            f"  24h Volume: ${crypto['volume24']}\n\n"
        )
    return formatted_data




def index(request):
    if 'chat_id' not in request.session:
        request.session['chat_id'] = str(uuid.uuid4())
    return render(request, 'index.html', {
        'chat_id': request.session['chat_id'],
        'headTitle':'Home'
    })

def dashboard(request):
    if request.method == "POST":
        # Generate a new chat_id when the form is submitted
        new_chat_id = str(uuid.uuid4())
        
        # Return the new chat_id as JSON for the frontend to handle
        return JsonResponse({"chat_id": new_chat_id})

    if 'chat_id' not in request.session:
        request.session['chat_id'] = str(uuid.uuid4())
    return render(request, 'dashboard.html', {
        'chat_id': str(uuid.uuid4()),
        'headTitle':'Dashboard',
        'category':'finance'
    })



def text_generator(request, chat_id):
    # Generate a new chat_id if none is provided
    print(request)
    if not chat_id:
        chat_id = str(uuid.uuid4())  # Generate a new chat_id for a new session
        chat_logs = []
    else:
        # Retrieve chat logs for the specific chat_id
        chat_logs = ChatLog.objects.filter(chat_id=chat_id).order_by('timestamp')

    # Get unique chat IDs and the first message of each chat as the title
    unique_chats = ChatLog.objects.values('chat_id').distinct()
    chat_history = defaultdict(list)

    for unique_chat in unique_chats:
        # Get the first message for each unique chat_id
        first_message = ChatLog.objects.filter(chat_id=unique_chat['chat_id']).first()
        title = first_message.user_message if first_message else "Chat"  # Adjust 'user_message' as appropriate

        # Determine the date grouping label
        timestamp = first_message.timestamp if first_message else datetime.now()
        date_key = localtime(timestamp).date()

        if date_key == datetime.today().date():
            date_label = "Today"
        elif date_key == (datetime.today().date() - timedelta(days=1)):
            date_label = "Yesterday"
        else:
            date_label = date_key.strftime('%Y-%m-%d')

        # Append each entry to the corresponding date group in chat_history
        chat_history[date_label].append({
            'chat_id': unique_chat['chat_id'],
            'title': title
        })

    # Sort chat_history by a custom order: Today, Yesterday, then other dates in descending order
    sorted_chat_history = dict(
        sorted(chat_history.items(), key=lambda x: (x[0] != 'Today', x[0] != 'Yesterday', x[0]))
    )


    # Pass the sorted chat history to the template
    return render(request, 'generator/financeverify.html', {
        'message': "What do you want to know about finance?",
        'chat_id': chat_id,
        'chat_logs': chat_logs,
        'chat_history': sorted_chat_history , # Sorted by date with titles grouped
        'category':''
    })


def get_openai_response(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "")
        # print(user_message)
        # Add any necessary processing here
        openai_response = call_openai(user_message)  # Define this function below
        return JsonResponse({"response": openai_response})



def send_message(request, chat_id):
    if request.method == 'POST':
        print(chat_id)
        # Parse JSON data
        if not chat_id:
            chat_id = "default_chat_id"     
        data = json.loads(request.body)
        user_message = data.get('userMessage', '')
        source = data.get('source', '')

        # Log source and message for debugging
        print("Source:", source)
        print("User Message:", user_message)

        # Determine the reply based on the source of the message
        if source == 'text_generator':
            reply = f"{user_message}"

        else:
            reply = f"General response: {user_message}"

        # Optionally, send the message to OpenAI
        openai_response = call_openai(user_message)  # Uncomment if OpenAI is needed
        # print(openai_response)
        reply = openai_response if openai_response else reply
        # print('reply is ',reply)
        # Save the user message and response to the ChatLog
        ChatLog.objects.create(chat_id=chat_id, user_message=user_message, ai_response=reply)
        return JsonResponse({"response": reply})

    return JsonResponse({"error": "Only POST method is allowed"}, status=405)
import logging
from openai import OpenAI 
client = OpenAI(api_key=OPENAI_API_KEY) 

# Assuming `client` is your OpenAI or assistant service client (e.g., OpenAI's API client)
# You need to initialize this client with your credentials

# Define a function to run the assistant based on the thread
def run_assistant(thread):
    import datetime
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    crypto_data = fetch_crypto_data()
#     # print(crypto_data)
    formatted_crypto_data = format_crypto_data_for_openai(crypto_data)
    # Retrieve the assistant using its ID
    assistant = client.beta.assistants.retrieve(OPENAI_ASSISTANT_ID)
    
    # Create a new run for the given thread with specific instructions
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions=( 
                f"\n\nHere is the latest crypto data, including Dogecoin:\n{formatted_crypto_data}\n\nToday’s date is {date}. "
                "Structure all answers in web-ready HTML without code block markers. Use <p> tags for each paragraph, and also add links if available. providing practical insights tailored to a business audience. "
        ), 
            
        )

    # Poll for the run status to check when it is completed
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # Fetch the generated message from the thread's messages
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    new_message = messages.data[0].content[0].text.value
    
    logging.info(f"Generated message: {new_message}")
    
    # Return the generated message
    return new_message

# Function to generate a response based on the message
def call_openai(message_body): 
    thread = client.beta.threads.create() 
    thread_id = thread.id 
    client.beta.threads.messages.create( 
        thread_id=thread_id, 
        role="user", 
        content=message_body, 
    ) 
    new_message = run_assistant(thread) 
    return new_message


# def call_openai(message):
#     import datetime
#     date = datetime.datetime.now().strftime('%Y-%m-%d')
#     crypto_data = fetch_crypto_data()
#     # print(crypto_data)
#     formatted_crypto_data = format_crypto_data_for_openai(crypto_data)
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer {OPENAI_API_KEY}'
#     }
#     data = {
#         "model": "gpt-4o-mini",
#         "messages": [
#         {"role": "system", "content": (
#             "You are the Portdex.ai assistant, a digital expert designed to support users with insights across finance, industry trends, services, company data, cryptocurrencies, financial advisories, tax matters, and legal service providers. "
#             f"\n\nHere is the latest crypto data, including Dogecoin:\n{formatted_crypto_data}\n\nToday’s date is {date}. "
#             "Your primary goal is to offer strategic, data-driven guidance that aligns with Portdex.ai's commitment to delivering actionable intelligence and clarity in decision-making. "
#             "If the user asks about any cryptocurrency listed in the provided data (like Dogecoin), reference this data to give updated information. "
#             "When addressing finance or crypto topics, highlight recent developments, market updates, and practical applications using the most relevant available data. "
#             "For questions outside finance, services, industries, companies, crypto, financial advisories, tax, and legal topics, respond with: 'I can provide only data related to finance, services, industries, companies, crypto, financial advisory, tax, and legal services.' "
#             "Structure all answers in web-ready HTML without code block markers. Use <p> tags for each paragraph, providing practical insights tailored to a business audience. "
#             "Maintain a supportive and positive tone, aligning with Portdex.ai’s mission to empower users with accurate, strategic insights."
#         )},
#         {"role": "user", "content": message}
#     ]
#     }
#     response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
#     # print(response.json())
#     if response.status_code == 200:
#         response_data = response.json()
#         return response_data['choices'][0]['message']['content']
#     else:
#         return "Error: Unable to fetch response."
    


def load_chat(request, chat_id):
    # Retrieve all chat logs for the given chat_id
    chat_logs = ChatLog.objects.filter(chat_id=chat_id).order_by("timestamp")

    # Load recent chat history summaries for the sidebar
    chat_history = ChatLog.objects.filter(chat_id=chat_id).order_by('-timestamp')[:5]

    return render(request, 'generator/financeverify.html', {
        'chat_logs': chat_logs,
        'chat_id': chat_id,
        'chat_history': chat_history,
    })