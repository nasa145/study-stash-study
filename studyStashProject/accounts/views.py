

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from paymentapp.models import Subscription
from .models import UserProfile, ApplicationUser
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.http import HttpResponse
from django.urls import reverse
from django.utils.http import urlencode
from django.core.mail import EmailMessage
from datetime import datetime 
from django.contrib import messages 
from django.views.decorators.http import require_POST

# A VIEW TO LOGIN THE USER WITH CUSTOM LOGIC
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST['password']

        # Authenticate the user using the custom backend
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "You are now logged in " )
                return redirect('activeuserapp:user_dashboard')

            else:
                messages.error(request, 'Your account is not yet activated. Please check your email for confirmation instructions.')
                return redirect('accounts:login')
        else:
            messages.error(request, 'Incorrect credentials. Please check your username/email and password.')
            return redirect('accounts:login') 

    return render(request, 'accounts/registration/login.html')




# A REGISTRATION VIEW FOR USER REGISTRATION LOGIC
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Check if passwords match
        if password1 != password2:
            messages.error(request, 'Passwords do not match. Please try again.')
            return redirect('accounts:register')

        # Check if email is already in use
        if ApplicationUser.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use. Please use a different email address.')
            return redirect('accounts:register')

        # Check if username is already in use
        if ApplicationUser.objects.filter(username=username).exists():
            messages.error(request, 'Username is already in use. Please choose a different username.')
            return redirect('accounts:register')

        # Create a new user object but set it as inactive
        user = ApplicationUser.objects.create_user(username, email, password1)
        user.is_active = False
        user.save()

        # After successfully registration also create the profule for the user
        user_profile = UserProfile.objects.create(user=user)

        # Generate email confirmation token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Send email confirmation using EmailMessage
        current_site = get_current_site(request)
        mail_subject = 'Activate your account'
        current_year = datetime.now().year
        message = render_to_string('accounts/registration/activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': uid,
            'token': token,
            'year': current_year,
        })
        email_message = EmailMessage(mail_subject, message, 'appsnasa57@gmail.com', [user.email])
        email_message.content_subtype = 'html'  
        email_message.send()

        messages.success(request, 'Registration successful! Check your email for confirmation instructions.')
        return redirect('accounts:success_register')

    return render(request, 'accounts/registration/register.html')




# A VIEW THAT TAKES THE USER TO SUCCESS REGISTRATION PAGE
def success_register_view(request):
    return render(request, 'accounts/registration/success_register.html')


#  A VIEW TO ACTIVATE THE USER
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = ApplicationUser.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated. You can now log in.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Invalid activation link. Please contact support.')
    except (TypeError, ValueError, OverflowError, ApplicationUser.DoesNotExist):
        messages.error(request, 'Invalid activation link. Please contact support.')
        return redirect('accounts:login')

    return redirect('accounts:login')



# A VIEW TO EDIT THE PROFILE OF THE USER
@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        profile.first_name = request.POST.get('first_name')
        profile.last_name = request.POST.get('last_name')
        profile.mobile_number = request.POST.get('mobile_number')
        profile.location = request.POST.get('location', '')
        profile.photo = request.FILES.get('photo', profile.photo)
        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('accounts:profile')

    return render(request, 'profile/profile.html', context)


# Custom password reset view
def custom_password_reset(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        try:
            user = ApplicationUser.objects.get(email=email)
        except ApplicationUser.DoesNotExist:
            user = None

        if user:
            # Generate a custom reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Send password reset email
            current_site = get_current_site(request)
            mail_subject = 'Password Reset'
            message = render_to_string('accounts/registration/custom_password_reset_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            email_message = EmailMessage(mail_subject, message, 'appsnasa57@gmail.com', [user.email])
            email_message.content_subtype = 'html'
            email_message.send()

            return redirect('accounts:password_reset_done')

    return render(request, 'accounts/registration/custom_password_reset_form.html')



# Custom password reset confirm view
def custom_password_reset_confirm(request, uidb64, token):
    try:
        uid = uid = force_str(urlsafe_base64_decode(uidb64))
        user = ApplicationUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, ApplicationUser.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST['password']
            password2 = request.POST['confirm_password']
            if password == password2:
                user.set_password(password)
                user.save()
                return redirect('accounts:password_reset_complete')
            else:
                messages.error(request, 'Passwords do not match.')
                return redirect('accounts:password_reset_confirm', uidb64=uidb64, token=token)

    return render(request, 'accounts/registration/custom_password_reset_confirm.html')



# Password reset complete view
def custom_password_reset_complete(request):
    return render(request, 'accounts/registration/custom_password_reset_complete.html')


# Password reset done view
def custom_password_reset_done(request):
    return render(request, 'accounts/registration/custom_password_reset_done.html')



# A view to chnage the password for the user
@login_required
@require_POST
def password_change(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password')
        new_password2 = request.POST.get('confirm_new_password')

        # Check if the old password is correct
        if request.user.check_password(old_password):
            # Check if the new passwords match
            if new_password1 == new_password2:
                # Update the user's password
                request.user.set_password(new_password1)
                request.user.save()
                messages.success(request, 'Your password has been changed successfully.')
                return redirect('acccounts:account')
            else:
                messages.error(request, 'New passwords do not match.')
                return redirect('activeuserapp:account')
        else:
            messages.error(request, 'The old password is incorrect.')
            return redirect('activeuserapp:account')

    return redirect('activeuserapp:account')



def available_plans_view(request):
    return render(request, 'accounts/registration/pages/available_plans.html')


def not_found_view(request):
    return render(request, 'accounts/registration/pages/not_found.html')