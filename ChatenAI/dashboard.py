from django.shortcuts import render
import uuid  # To generate unique chat IDs




def appearance(request):
    return render(request,"dashboard/appearance.html", {'headTitle' : 'Settings','header' : 'header'})
    
def application(request):
    return render(request,"dashboard/application.html", {'headTitle' : 'Settings','header' : 'header'})
    
def chatExport(request):
    return render(request,"dashboard/chatExport.html", {'headTitle' : 'Chat Exports','header' : 'header'})
    
def help(request):
    if 'chat_id' not in request.session:
        request.session['chat_id'] = str(uuid.uuid4())
    return render(request, 'dashboard/help.html', {
        'chat_id': str(uuid.uuid4()),
        'headTitle' : 'Help & FAQ',
        'header' : 'header'
    })
    # return render(request,"dashboard/help.html", {'headTitle' : 'Help & FAQ','header' : 'header'})
    
def notification(request):
    return render(request,"dashboard/notification.html", {'headTitle' : 'Notification','header' : 'header'})
    
def plansBilling(request):
    return render(request,"dashboard/plansBilling.html", {'headTitle': 'Plans & Billing','header': 'header'})
    
def profileDetails(request):
    return render(request,"dashboard/profileDetails.html", {'headTitle' : 'Profile Details','header' : 'header'})
    
def releaseNotes(request):
    return render(request,"dashboard/releaseNotes.html", {'headTitle' : 'Releasse Notes'})
    
def sessions(request):
    return render(request,"dashboard/sessions.html", {'headTitle': 'Releasse Notes'})
    