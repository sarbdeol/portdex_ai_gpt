from django.shortcuts import render


def textGenerator(request):
    return render(request,"generator/textGenerator.html",{'headTitle' : 'Text Generator','toggle' : "true"})

def financeverify(request):
    return render(request,"generator/financeverify.html", {'headTitle' : 'Finance verify','toggle' : "true"})
