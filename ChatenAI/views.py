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
from django.core.paginator import Paginator
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


import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_rates(coin):
    # URL of the Ethereum exchanges page
    url = f'https://coinranking.com/coin/{coin}/exchanges'

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table containing exchange listings
        table = soup.find('table')
        
        # Check if the table exists
        if table:
            # Extract table rows
            rows = table.find('tbody').find_all('tr')
            
            # Initialize data storage for first two columns
            data = []
            
            # Iterate over each row
            for row in rows[:10]:
                # Extract columns in the current row
                cols = row.find_all('td')
                # Get text from the first two columns
                if len(cols) >= 2:  # Ensure there are at least two columns
                    col1 = cols[2].get_text(separator=" ", strip=True).replace("\n", "").strip()
                    col2 = cols[3].get_text(separator=" ", strip=True).replace("\n", "").strip()
                    data.append([col1, col2])
            
            # Create a pandas DataFrame with the data
            df = pd.DataFrame(data, columns=['Exchanges', 'Price'])
            
            # Display the DataFrame
            print(df)
            return df
        else:
            print('Exchange table not found on the page.')
            return 'no exchange rate found'
    else:
        print(f'Failed to retrieve the page. Status code: {response.status_code}')
        return 'Failed to retrieve the price'
def get_coin_name(message_body):
    # message_body='provide all exchange rates of dogcoin'
    import requests
    import json

    url = "https://api.openai.com/v1/chat/completions"

    payload = json.dumps({
    "model": "gpt-4o-mini",
    "messages": [
        {
        "role": "system",
        "content": f"Extract cryptocurrency names from the following message in the format 'coinname-symbol':\n\n{message_body}\n\nExample Output:\nbitcoin-btc\nethereum-eth\nsolana-sol"
        }
    ]
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {OPENAI_API_KEY}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.json()['choices'][0]['message']['content'])
    coin=response.json()['choices'][0]['message']['content']
    return coin
    
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
def run_assistant(thread,message_body):
    import datetime
    date = datetime.datetime.now().strftime('%Y-%m-%d')
#     crypto_data = fetch_crypto_data()
# #     # print(crypto_data)
#     formatted_crypto_data = format_crypto_data_for_openai(crypto_data)
    # Retrieve the assistant using its ID
    assistant = client.beta.assistants.retrieve(OPENAI_ASSISTANT_ID)
    if any(keyword in message_body for keyword in ['rate', 'crypto', 'rates', 'price']):
        
        coin=get_coin_name(message_body)
        formatted_crypto_data=get_rates(coin)
        ins=f"\n\nHere is the latest crypto data:\n{formatted_crypto_data}"
    else:
        ins=None
    assistant = client.beta.assistants.update(
	assistant_id=assistant.id,
	# tool_resources={"file_search": {"vector_store_ids": ['vs_3ILDTuF1KoHBko7M3OzA6JCr']}},
	)
    # Create a new run for the given thread with specific instructions
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        
        instructions=( 
                f"{ins}\n\nToday’s date is {date}. "
                "response Use HTML formatting like chatbot response with `<h4>`, `<h5>`, and `<p>` tags and cards for organized responses.transparant background color and dont include images in response"
                "Dont mention this *Based on the information from the uploaded files*"
                # "When the user requests cryptocurrency rates, present information from no fewer than two sources (preferably three). "
                # "Compare the rates from these sources and present a brief analysis of any discrepancies or noteworthy changes."
                # "Clearly mention the names of all the sources and provide clickable HTML links for direct referencing."
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
    
    thread = client.beta.threads.create(
        tool_resources={
			"file_search": {
			"vector_store_ids": ["vs_3ILDTuF1KoHBko7M3OzA6JCr"]
			}
		}
	) 
    thread_id = thread.id 
    client.beta.threads.messages.create( 
        thread_id=thread_id, 
        role="user", 
        content=message_body, 
        
    ) 
    new_message = run_assistant(thread,message_body) 
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



def product_list(request):
    # Fetch data from the external API
    response = requests.get("https://walluk.s3.eu-north-1.amazonaws.com/themes/themes%26plugins.json")
    if response.status_code == 200:
        products = response.json()  # Assuming the API returns a JSON array of themes/plugins
    else:
        products = []
    print(request)
    # Extract distinct categories for the filter dropdown
    categories = list({product.get("category") for product in products if product.get("category")})

    sellers = list({product.get("author") for product in products if product.get("author")})
    sellers = sorted(sellers)  # Sort the list alphabetically
    # Filter by category if selected
    selected_category = request.GET.get('category', '')
    if selected_category:
        products = [product for product in products if product.get("category") == selected_category]
    
    selected_author = request.GET.get('author', '')
    print('selected_author',selected_author)
    if selected_author:
        products = [product for product in products if product.get("author") == selected_author]

    # Implement pagination, 10 items per page
    paginator = Paginator(products, 30)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)

    

    context = {
        'products': products_page,
        'categories': categories,
        'selected_category': selected_category,
        'authors': sellers,
        'selected_author': selected_author,
        'chat_id': str(uuid.uuid4()),
    }

    return render(request, 'products.html', context)




def freelancers_list(request):
    # Fetch data from the API
    response = requests.get("https://walluk.s3.eu-north-1.amazonaws.com/freelancers/freelancer_data.json")  # Replace with the actual API URL
    if response.status_code == 200:
        freelancers = response.json()
    else:
        freelancers = []

    # Get the selected category from the request
    selected_category = request.GET.get('category', '')

    # Filter freelancers by the selected category
    if selected_category:
        freelancers = [freelancer for freelancer in freelancers if freelancer.get("category") == selected_category]

    # Extract unique categories for filtering
    categories = list(set(freelancer["category"] for freelancer in freelancers if "category" in freelancer))

    context = {
        'freelancers': freelancers,
        'categories': categories,
        'selected_category': selected_category,
        'chat_id': str(uuid.uuid4()),
    }

    return render(request, 'developers.html', context)



def ai_repositories(request):
    # Fetch JSON data from the API
    finance_json_url = 'https://walluk.s3.amazonaws.com/gitrepos/finance_repo.json'
    education_json_url = 'https://walluk.s3.amazonaws.com/gitrepos/education_ai_repo.json'

    # Determine category from request
    selected_category = request.GET.get('category', 'finance')  # Default is 'finance'

    # Fetch the appropriate JSON data based on the selected category
    if selected_category == 'education':
        response = requests.get(education_json_url)
    else:
        response = requests.get(finance_json_url)

    repos_data = json.loads(response.text)

    # Optionally, filter by programming languages/types (if requested)
    selected_type = request.GET.get('type', None)
    if selected_type:
        repos_data = [repo for repo in repos_data if selected_type.lower() in [tag.lower() for tag in repo.get('topics', [])]]

    context = {
        'repos': repos_data,
        'selected_type': selected_type,
        'selected_category': selected_category,
        'chat_id': str(uuid.uuid4()),
    }
    return render(request, 'finance_repo.html', context)


def ai_developers(request):
    # S3 URL with developer data
    s3_url = "https://walluk.s3.eu-north-1.amazonaws.com/freelancers/ai-developers.json"

    try:
        # Fetch the developer data from S3
        response = requests.get(s3_url)
        response.raise_for_status()
        developers_data = response.json()  # Parse JSON from the response
    except requests.exceptions.RequestException as e:
        developers_data = []  # Fallback if the S3 request fails
        print(f"Error fetching data from S3: {e}")
    # Paginate the developers data (20 items per page)
    paginator = Paginator(developers_data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Pass developers data to the template
    return render(request, 'ai_developers.html', {'developers': developers_data,'chat_id': str(uuid.uuid4()),'page_obj':page_obj})


# Function to fetch all coin data from the JSON
def get_all_coins():
    url = 'https://s3.coinmarketcap.com/generated/core/crypto/cryptos.json'
    response = requests.get(url)
    return response.json()

# Function to fetch prices from CoinLore API
def get_coin_prices():
    url = 'https://api.coinlore.net/api/tickers/'
    response = requests.get(url)
    return response.json()

def all_coins(request):
    # Fetch coin data from the JSON
    data = get_all_coins()
    cryptos = [dict(zip(data["fields"], value)) for value in data["values"]]

    # Fetch prices from CoinLore API
    prices_data = get_coin_prices()
    coin_prices = {coin['symbol'].lower(): coin for coin in prices_data['data']}

    # Merge the prices with the coin data based on the coin symbol
    for crypto in cryptos:
        if crypto.get('rank') not in ['', 0,' ']:
            print(f"Rank: {crypto.get('rank')} - Name: {crypto.get('name')}")
            coin_symbol = crypto.get('symbol').lower()  # Use symbol instead of name
            if coin_symbol in coin_prices:
                crypto['price_usd'] = coin_prices[coin_symbol]['price_usd']
                crypto['percent_change_24h'] = coin_prices[coin_symbol].get('percent_change_24h', '0.00')  # Handle missing values
                crypto['percent_change_1h'] = coin_prices[coin_symbol].get('percent_change_1h', '0.00')
                crypto['percent_change_7d'] = coin_prices[coin_symbol].get('percent_change_7d', '0.00')
                crypto['market_cap_usd'] = coin_prices[coin_symbol].get('market_cap_usd', '0.00')
                crypto['volume24'] = coin_prices[coin_symbol].get('volume24', 0)
            else:
                # Set to None or default if no price is found
                crypto['price_usd'] = None
                crypto['percent_change_24h'] = '0.00'
                crypto['percent_change_1h'] = '0.00'
                crypto['percent_change_7d'] = '0.00'
                crypto['market_cap_usd'] = '0.00'
                crypto['volume24'] = 0
        
        # Convert rank to integer (if it exists) to ensure sorting works correctly
            crypto['rank'] = int(crypto.get('rank'))  # Ensure 'rank' is an integer
        
    # Sort the cryptocurrencies by 'rank' (ascending)
    filtered_cryptos = [crypto for crypto in cryptos if crypto.get('rank') not in ['0', 0]]

    # Sort the filtered list by 'rank' (ascending)
    filtered_cryptos.sort(key=lambda x: x['rank'])  # Sorting by 'rank'
    # Pagination setup
    paginator = Paginator(filtered_cryptos, 100)  # Show 100 coins per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    # Render the template with paginated data
    return render(request, 'all_coins.html', {'page_obj': page_obj, 'chat_id': str(uuid.uuid4())})


def get_trending_coins():
    url = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/spotlight?dataType=1&limit=5&start=1"
    response = requests.get(url)
    return response.json()

# API Functions
def get_coin_details(coin_slug):
    url = f'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/market-pairs/latest?slug={coin_slug}&start=1&limit=10&category=spot&centerType=all&sort=cmc_rank_advanced&direction=desc&spotUntracked=true'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    return response.json()

def get_graph_data(crypto_slug, period='1'):
    url = f'https://api.coinmarketcap.com/nft/v3/nft/chain/total?cryptoSlug={crypto_slug}&period={period}'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    return response.json()

def get_crypto_news(crypto_id, language='en'):
    url = f'https://api.coinmarketcap.com/aggr/v3/news/cdp?mode=top&cryptoId={crypto_id}&language={language}'
    response = requests.get(url)
    # print(response.json())
    return response.json()

import time
def coin_detail(request, coin_slug, crypto_id):
    # Fetch coin details
    coin_data = get_coin_details(coin_slug)['data']
    # print(coin_data)
    # Fetch trending coins
    trending_data = get_trending_coins()

    # Fetch graph data
    graph_response = get_graph_data(coin_slug)
    graph_records = graph_response["data"]["records"] if graph_response else []

    # Prepare graph data (timePeriod -> readable format, volumeUsd)
    graph_labels = [
        time.strftime('%H:%M %p', time.gmtime(int(record["timePeriod"]) / 1000))
        for record in graph_records
    ]
    graph_values = [record["volumeUsd"] for record in graph_records]

    # Fetch cryptocurrency-related news
    news_data = get_crypto_news(crypto_id)['data']['news']
    graph_data = graph_response["data"] if graph_response else {}
    stats = {
        "marketCapUsd": graph_data.get("marketCapUsd", 0),
        "volumeUsd": graph_data.get("volumeUsd", 0),
        "volumeRate": graph_data.get("volumeRate", 0),
        "totalSupply": 19.79,  # Example value, replace with actual data if available
        "maxSupply": 21  # Example value, replace with actual data if available
    }
    # Render template
    context = {
        'coin_data': coin_data,
        'stats':stats,
        'trending_data': trending_data['data']['trendingList'],
        'graph_labels': graph_labels,
        'graph_values': graph_values,
        'news_data': news_data,
        'chat_id': str(uuid.uuid4())
    }
    return render(request, 'coin_detail.html', context)