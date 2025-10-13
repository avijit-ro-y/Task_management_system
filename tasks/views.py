from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm
from tasks.models import Employee,Task

# Create your views here.
def manager_dashboard(request):
    return render(request,"dashboard/manager_dashboard.html")
def user_dashboard(request):
    return render(request,"dashboard/user_dashboard.html")
def task_form(request):
    employees=Employee.objects.all()
    form=TaskModelForm()
    
    if request.method=="POST":
        form=TaskModelForm(request.POST)
        if form.is_valid():
            
            """for model form"""
            form.save()
            return render(request,'task_form.html',{"form":form,"message":"Task added successfully"})
            '''-----for django form------'''
            # data=form.cleaned_data
            # title=data.get('title')
            # description=data.get('descripotion')
            # assigned_to=data.get('assigned_to')
            # due_date=data.get('due_date')
            # task=Task.objects.create(title=title,descripotion=description,due_date=due_date)
            # for emp_id in assigned_to:
            #     employee=Employee.objects.get(id=emp_id)
            #     task.assigned_to.add(employee)
            # return HttpResponse("Task added successfully")
    context={"form":form}
    return render(request,"task_form.html",context)