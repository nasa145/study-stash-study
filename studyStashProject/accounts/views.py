from django.shortcuts import render

def login_view(request):
    return render(request, 'accounts/registration/login.html')

def password_reset_complete_view(request):
    return render(request, 'accounts/registration/password_reset_complete.html')

def password_reset_confirm_view(request):
    return render(request, 'accounts/registration/password_reset_confirm.html')

def password_reset_done_view(request):
    return render(request, 'accounts/registration/password_reset_done.html')

def password_reset_form_view(request):
    return render(request, 'accounts/registration/password_reset_form.html')

def phone_verification_view(request):
    return render(request, 'accounts/registration/phone_verification.html')

def register_view(request):
    return render(request, 'accounts/registration/register.html')

def success_register_view(request):
    return render(request, 'accounts/registration/success_register.html')

def available_plans_view(request):
    return render(request, 'accounts/registration/pages/available_plans.html')

def not_found_view(request):
    return render(request, 'accounts/registration/pages/not_found.html')