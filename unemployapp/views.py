from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Date, Application, Activity
import datetime

# Create your views here.
def index(request):
    all_dates = Date.objects.order_by("date")
    all_applications = Application.objects.order_by("company_name")
    all_activities = Activity.objects.all()
    
    context = {
        "all_dates": all_dates,
        "all_applications": all_applications,
        "all_activities": all_activities
    }

    return render(request, 'unemployapp/index.html', context)

#takes new application from form in html and saves it
#redirects back to homescreen
def new_app(request):
    new_app_date = request.POST['new_app_date']
    new_app_date = datetime.datetime.strptime(new_app_date, '%Y-%m-%d').date()

    date_exists = check_date(new_app_date)

    if date_exists:
        new_app_date = Date.objects.get(date=new_app_date)
    else:
        new_date = Date(date=new_app_date)
        new_date.save()
        new_app_date = new_date

    new_app_co_name = request.POST['new_app_co_name']
    new_app_location = request.POST['new_app_location']
    new_app_contact_method = request.POST['new_app_contact_method']
    new_app_work_type = request.POST['new_app_work_type']
    new_app_results = request.POST['new_app_results']

    application = Application(date=new_app_date, company_name=new_app_co_name, location=new_app_location, contact_method=new_app_contact_method, work_type=new_app_work_type, results=new_app_results)
    application.save()

    return HttpResponseRedirect(reverse('unemployapp:index'))


#takes new activity from form in html and saves it
#redirects back to homescreen
def new_act(request):
    new_act_date = request.POST['new_act_date']
    new_act_date = datetime.datetime.strptime(new_act_date, '%Y-%m-%d').date()
    

    date_exists = check_date(new_act_date)

    if date_exists:
        new_act_date = Date.objects.get(date=new_act_date)
    else:
        new_date = Date(date=new_act_date)
        new_date.save()
        new_act_date = new_date
    
    new_activity = request.POST['new_activity']
    
    activity = Activity(date=new_act_date, activity=new_activity)
    activity.save()
    
    return HttpResponseRedirect(reverse('unemployapp:index'))

#just checks if this date exists already
def check_date(new_act_date):
    all_dates = Date.objects.all()

    for date in all_dates:
        if date.date == new_act_date:
            return True
    return False