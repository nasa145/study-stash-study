from django.shortcuts import render

def index(request):
    return render(request, 'studystashapp/publicTemplates/index.html')

def legal_information(request):
    return render(request, 'studystashapp/publicTemplates/legalinformation.html')

