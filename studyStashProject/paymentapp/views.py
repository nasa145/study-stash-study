

from django.shortcuts import render, redirect, get_object_or_404
from .models import Plan, Subscription, Payment
from django.conf import settings
import braintree
from django.contrib.auth.decorators import login_required
from requests.exceptions import ConnectionError
from django.http import HttpResponseServerError
from django.contrib import messages


# Create your views here.
@login_required
def available_plans_view(request):
    plans = Plan.objects.all()
    return render(request, 'paymentapp/available_plans.html', {"plans":plans})



# instantiate Braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

@login_required
def payment_process(request, id):
    if request.method == 'POST':
        try:
            # Get the credit card information from the request.
            cardholder_name = request.POST['cardholder_name']
            credit_card_number = request.POST['credit_card_number']
            expiration_date = request.POST['expiration_date']
            cvv = request.POST['cvv']

            amount = '10.00'  # Amount should be a string

            plan = Plan.objects.get(pk=id)

            # Create a Braintree transaction object.
            result = gateway.transaction.sale({
                'amount': f'{plan.price}',
                'credit_card': {
                    'number': credit_card_number,
                    'expiration_date': expiration_date,
                    'cvv': cvv,
                }
            })


            # Check if the transaction was successful.
            if result.is_success:
                Subscription.objects.create(
                    user=request.user, plan=plan
                )

                Payment.objects.create(
                    user=request.user, plan=plan, transaction_id=result.transaction.id
                )
                request.user.plan = plan
                request.user.save()
                return redirect('paymentapp:done')
            else:
                # If the transaction failed, return an error message.
                print(result.message)
                return redirect('paymentapp:canceled')
        except ConnectionError as e:
            # Handle the connection error gracefully
            messages.error(request, "There was an issue processing your payment. Please try again later.")
            return redirect('paymentapp:process')

    else:
        return render(request, 'paymentapp/process.html')


    
@login_required
def payment_done(request):
    return render(request, 'paymentapp/done.html')

@login_required
def payment_canceled(request):
    return render(request, 'paymentapp/canceled.html')