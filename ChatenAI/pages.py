from django.shortcuts import render
import uuid  # To generate unique chat IDs

def blog(request):
    return render(request, "pages/blog.html", { 'headTitle':'Dashboard', 'title':'Our Blog', 'subTitle' :'Blog','header' : 'header3' })
    
def blogDetails(request):
    return render(request, "pages/blogDetails.html", { 'headTitle' : 'Blog Details', 'title' : 'Blog Details','subTitle' : 'Blog Details','header' : 'header3'})
    
def contact(request):
    return render(request, "pages/contact.html")
    
def pricing(request):
    return render(request, "pages/pricing.html", {'headTitle' :'Pricing','header' :'header2'})
    
def privacyPolicy(request):
    return render(request, "pages/privacyPolicy.html")
    
def roadmap(request):
    if 'chat_id' not in request.session:
        request.session['chat_id'] = str(uuid.uuid4())
    return render(request, 'pages/roadmap.html', {
        'chat_id': str(uuid.uuid4()),
        'headTitle' : 'Roadmap','title' : 'Roadmap','subTitle' : 'Roadmap','header' : 'Roadmap'
    })
    # return render(request, "pages/roadmap.html",{'headTitle' : 'Roadmap','title' : 'Roadmap','subTitle' : 'Roadmap','header' : 'header3'})
    
def signin(request):
    return render(request, "pages/signin.html", {'headTitle' : 'Log In','header' : 'header5'})
    
def signup(request):
    return render(request, "pages/signup.html", {'headTitle' : 'SignUp','header' : 'header5'})
    
def styleGuide(request):
    return render(request, "pages/styleGuide.html", {'headTitle' : 'Style Guide','title' : 'Style Guide','subTitle' : 'Style Guide','header' : 'header3'})
    
def team(request):
    return render(request, "pages/team.html", {'headTitle' : 'Team','title' : 'Our Team', 'subTitle' : 'Team', 'header' : 'header3'})
    
def termsPolicy(request):
    if 'chat_id' not in request.session:
        request.session['chat_id'] = str(uuid.uuid4())
    return render(request, 'pages/termsPolicy.html', {
        'chat_id': str(uuid.uuid4()),
        'headTitle' : 'Terms and Policy'
    })
    # return render(request, "pages/termsPolicy.html", {'headTitle' : 'Terms and Policy'})
    
def utilize(request):
    return render(request, "pages/utilize.html", {'headTitle' : 'How to use','title' : 'How to use','subTitle' : 'How to use','header' : 'header3'})
    