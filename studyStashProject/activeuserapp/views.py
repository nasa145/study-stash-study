from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from .models import Task, DownloadedTask, SubmmittedTasks
from django.utils import timezone
from datetime import datetime
from paymentapp.models import Subscription
from django.contrib import messages 
from django.db.models import Sum

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


# AFTER TEMPLATE DESIGN COMPLETION THIS SHOULD BE REPLACED WITH AVAILABLE_TASKS VIEW
def today_task(request):
    return render(request, 'activeuserapp/userdashboard/today_task.html')


# A VIEW TO THE USER DASHBOARD
def user_dashboard(request):
    total_downloads_by_user = DownloadedTask.objects.filter(user=request.user).count()
    total_uploads_by_user = SubmmittedTasks.objects.filter(user=request.user).count()
    if total_uploads_by_user is None:
        total_uploads_by_user = 0

    # calculate or retrieve the total earning of te user from when he joined the site
    user_submiited_tasks_paid_for = SubmmittedTasks.objects.filter(user=request.user,paidStatus='PAID')
    total_profit_user_earned_from_site = user_submiited_tasks_paid_for.aggregate(total_Earnings=Sum('amount_to_be_paid_as_reward'))['total_Earnings']
    if total_profit_user_earned_from_site is None:
        total_profit_user_earned_from_site = 0

    # calculate and display the yusers pending payment for which the tasks are approved and accepted
    pending_payments = SubmmittedTasks.objects.filter(user=request.user, approvalStatus='ACCEPTED', paidStatus='NOT_PAID')
    total_pending_payment = pending_payments.aggregate(total_payment=Sum('amount_to_be_paid_as_reward'))['total_payment']

    if total_pending_payment is None:
        total_pending_payment = 0

    user_plan_price = Subscription.objects.get(user=request.user).plan.price
    amount_user_should_in_a_month_according_to_his_plan = user_plan_price + total_pending_payment


    return render(request, 'activeuserapp/userdashboard/user_dashboard.html', {
        'total_downloads_by_user':total_downloads_by_user,
        'total_uploads_by_user':total_uploads_by_user,
        'total_profit_user_earned_from_site':total_profit_user_earned_from_site,
        'total_pending_payment':total_pending_payment,
        'amount_user_should_in_a_month_according_to_his_plan':amount_user_should_in_a_month_according_to_his_plan,
    })



def active_index(request):
    return render(request, 'activeuserapp/landingtemplates/active_index.html')

def legal_information(request):
    return render(request, 'activeuserapp/landingtemplates/legalinformation.html')






def available_tasks(request):
    current_datetime = timezone.now()
    available_tasks = Task.objects.filter(expiration_date__gt=current_datetime)
    return render(request, 'activeuserapp/userdashboard/available_tasks.html', {'available_tasks': available_tasks})



# A VIEW TO ENABLE A USER TO DOWNLOAD TASK
def download_task(request, task_id):

    today = datetime.today().weekday()
    if today not in [0, 1]:
        messages.error(request, "Task download is only allowed on Monday and Tuesday.")
        return HttpResponseForbidden("Task download is only allowed on Monday and Wednesday.")

    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return HttpResponseForbidden("Task not found or no longer available.")

    expiration_datetime = datetime.combine(task.expiration_date, datetime.min.time())
    current_datetime = datetime.now()
    if expiration_datetime < current_datetime:
        return HttpResponseForbidden("Task is no longer available.")

    user = request.user
    active_subscription = Subscription.objects.filter(user=user, is_active=True).first()
    if not active_subscription:
        return HttpResponseForbidden("Please purchase a subscription to download tasks.")

    downloaded_task = DownloadedTask.objects.filter(user=user, task=task).first()

    if downloaded_task:
        with open(task.pdf_file.path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{task.title}.pdf'
            response['X-Success-Message'] = 'Task download is successful.'
            return response

    with open(task.pdf_file.path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{task.title}.pdf'

    downloaded_task = DownloadedTask(user=user, task=task)
    downloaded_task.save()

    response['X-Success-Message'] = 'Task download is successful.'
    return response




def submit_task(request, task_id):

    today = datetime.today().weekday()
    if today not in [5, 6]:
        messages.error(request, "Task submission is only allowed on Saturday and Sunday.")

        # should be removed 
        return HttpResponseForbidden("Task submission is only allowed on Saturday and Sunday.")

    active_subscription = Subscription.objects.filter(user=request.user, is_active=True).first()
    if not active_subscription:
        messages.error(request, "Please purchase an active subscription to submit tasks.")

        # should be removed 
        return HttpResponseForbidden("Please purchase an active subscription to submit tasks.")
    
    downloaded_object_to_be_uploaded = DownloadedTask.objects.get(useer=request.user, pk=task_id)

    task = downloaded_object_to_be_uploaded.task


    if request.method == 'POST':

        submission = SubmmittedTasks(user=user, task=task, is_submitted=True)
        submission.pdf_file = request.FILES['pdf_file']
        submission.submitted_date = timezone.now()
        submission.save()
        messages.success(request, "Task submitted successfully!")

        # chnage the status of the task to be uplaoded
        downloaded_object_to_be_uploaded.uploaded_status = True

        # this should be remioved and replaced
        return HttpResponse("Task submitted successfully!")

    return render(request, 'submit_task.html')




def calculate_earnings(request):
    user = request.user

    paid_submissions = SubmmittedTasks.objects.filter(user=user, paidStatus='PAID')

    total_earnings = paid_submissions.aggregate(total_earnings=models.Sum('amount_to_paid'))['total_earnings']

    if total_earnings is None:
        total_earnings = 0

    return render(request, 'earnings.html', {'total_earnings': total_earnings})

  

def user_submitted_tasks(request):
    # Query all submitted tasks by the user
    submitted_tasks = SubmmittedTasks.objects.filter(user=request.user)
    return render(request, 'user_submitted_tasks.html', {'submitted_tasks': submitted_tasks})



def downlaoded_tasks(request):
    downloaded_tasks = DownloadedTask.objects.filter(user=request.user, uploaded_Status=False)
    

