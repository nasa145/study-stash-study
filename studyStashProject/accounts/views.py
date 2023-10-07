
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from paymentapp.models import Subscription
from .models import UserProfile, User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.http import HttpResponse
from django.urls import reverse
from django.utils.http import urlencode
from django.core.mail import EmailMessage
from datetime import datetime

# A VIEW TO LOGIN THE USER WITH CUSTOM LOGIC
def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST['password']

        # Authenticate the user using email or username
        user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            if user.is_active:
                # Check if the user has an active subscription
                subscription = Subscription.objects.filter(user=user, is_active=True).first()

                if subscription:
                    # User has an active subscription, redirect to the dashboard
                    login(request, user)
                    return redirect('activeuserapp:user_dashboard')
                else:
                    # User does not have an active subscription, redirect to available plans
                    messages.error(request, 'You need to purchase a plan to access the dashboard.')
                    return redirect('paymentapp:available_plans')
            else:
                messages.error(request, 'Your account is not yet activated. Please check your email for confirmation instructions.')
                return redirect('accounts:login')  # Redirect to the login page with an error message
        else:
            messages.error(request, 'Incorrect credentials. Please check your username/email and password.')
            return redirect('accounts:login')  # Redirect to the login page with an error message

    return render(request, 'accounts/registration/login.html')

# A REGISTRATION VIEW FOR USER REGISTRATION LOGIC
def register_view(request):
    if request.method == 'POST':
        # Get user input from the custom HTML form
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Check if passwords match
        if password1 != password2:
            messages.error(request, 'Passwords do not match. Please try again.')
            return redirect('accounts:register')

        # Check if email is already in use
        # User = get_user_model()
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use. Please use a different email address.')
            return redirect('accounts:register')

        # Check if username is already in use
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already in use. Please choose a different username.')
            return redirect('accounts:register')

        # Create a new user object but set it as inactive
        user = User.objects.create_user(username, email, password1)
        user.is_active = False
        user.save()

        # Generate email confirmation token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        print(uid)
        print(uid)

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
        email_message.content_subtype = 'html'  # Set the content type to HTML
        email_message.send()

        messages.success(request, 'Registration successful! Check your email for confirmation instructions.')
        return redirect('accounts:success_register')

    return render(request, 'accounts/registration/register.html')




# A VIEW THAT TAKES THE USER TO SUCCESS REGISTRATION PAGE
def success_register_view(request):
    return render(request, 'accounts/registration/success_register.html')


#  A VIEW TO ACTIVATE THE USER
def activate_account(request, uidb64, token):
    # User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated. You can now log in.')
        else:
            messages.error(request, 'Invalid activation link. Please contact support.')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, 'Invalid activation link. Please contact support.')

    return redirect('accounts:login')



# A VIEW TO EDIT THE PROFILE OF THE USER
@login_required
def profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)  # Get or create user's profile

    if request.method == 'POST':
        # Update the user's profile data based on the submitted form data
        profile.full_name = request.POST.get('full_name', '')
        profile.mobile_number = request.POST.get('mobile_number', '')
        profile.location = request.POST.get('location', '')
        # Handle photo upload if needed
        profile.photo = request.FILES.get('photo', profile.photo)
        profile.save()
        # Redirect to the profile page with a success message
        messages.success(request, 'Profile updated successfully.')
        return redirect('accounts:profile')

    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'profile/profile.html', context)


# Custom password reset view
def custom_password_reset(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
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
            email_message.content_subtype = 'html'  # Set the content type to HTML
            email_message.send()

            return redirect('accounts:password_reset_done')

    return render(request, 'accounts/registration/custom_password_reset_form.html')




# Custom password reset confirm view
def custom_password_reset_confirm(request, uidb64, token):
    try:
        uid = uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
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


def available_plans_view(request):
    return render(request, 'accounts/registration/pages/available_plans.html')


def not_found_view(request):
    return render(request, 'accounts/registration/pages/not_found.html')
