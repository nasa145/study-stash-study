from django.shortcuts import render

def account(request):
    return render(request, 'activeuserapp/userdashboard/account.html')

def docs(request):
    return render(request, 'activeuserapp/userdashboard/docs.html')

def help(request):
    return render(request, 'activeuserapp/userdashboard/help.html')

def notifications(request):
    return render(request, 'activeuserapp/userdashboard/notifications.html')

def settings(request):
    return render(request, 'activeuserapp/userdashboard/settings.html')

def today_task(request):
    return render(request, 'activeuserapp/userdashboard/today_task.html')

def user_dashboard(request):
    return render(request, 'activeuserapp/userdashboard/user_dashboard.html')

def active_index(request):
    return render(request, 'activeuserapp/landingtemplates/active_index.html')


