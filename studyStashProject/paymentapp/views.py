from django.shortcuts import render

# Create your views here.
def available_plans_view(request):
    return render(request, 'paymentapp/available_plans.html')

def payment_details_view(request):
    return render(request, 'paymentapp/payment_details.html')
