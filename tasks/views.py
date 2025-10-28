from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm,TaskDetailModelForm
from tasks.models import Task,Project
from django.db.models import Count,Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from users.views import is_admin

# Create your views here.
def is_manager(user):
    return user.groups.filter(name='Manager')

def is_employee(user):
    return user.groups.filter(name='Employee')

@user_passes_test(is_manager,login_url='no-permission') #ei decorator ekta function ney jeta true hole next step e jete dey...otherwise na 
def manager_dashboard(request):
    type=request.GET.get('type','all')
    base_query=Task.objects.select_related('details').prefetch_related('assigned_to')
    # total_task=tasks.count()
    # completed_task=Task.objects.filter(status='COMPLETED').count()
    # in_progress=Task.objects.filter(status='IN_PROGRESS').count()
    # pending_task=Task.objects.filter(status='PENDING').count()
    counts=Task.objects.aggregate(
        total=Count('id'),
        completed=Count('id',filter=Q(status='COMPLETED')),
        in_progress=Count('id',filter=Q(status='IN_PROGRESS')),
        pending=Count('id',filter=Q(status='PENDING')),
        )
    if type=='completed':
        tasks=base_query.filter(status='COMPLETED')
    elif type=='in-progress':
        tasks=base_query.filter(status='IN_PROGRESS')
    elif type=='pending':
        tasks=base_query.filter(status='PENDING')
    elif type=='all':
        tasks=base_query.all()
    context={
        "tasks":tasks,
        # "total_task":total_task,
        # "pending_task":pending_task,
        # "in_progress":in_progress,
        # "completed_task":completed_task,
        "counts":counts,
        "role":'manager'
    }
    return render(request,"dashboard/manager_dashboard.html",context)

@user_passes_test(is_employee,login_url='no-permission') #ei decorator ekta function ney jeta true hole next step e jete dey...otherwise na 
def employee_dashboard(request):
    return render(request,"dashboard/user_dashboard.html")

@login_required #login decorator
@permission_required('tasks.add_task',login_url='no-permission') #ekhane tasks model name and add_task code name
def task_form(request): #create task
    task_form=TaskModelForm()
    task_detail_form=TaskDetailModelForm()
    
    if request.method=="POST":
        task_form=TaskModelForm(request.POST) #image file access korar jonno request.FILES use hoy
        task_detail_form=TaskDetailModelForm(request.POST,request.FILES)
        if task_form.is_valid() and task_detail_form.is_valid():
            
            """for model form"""
            task=task_form.save()
            task_detail=task_detail_form.save(commit=False)
            task_detail.task=task
            task_detail.save()
            messages.success(request,'Task Created Successfully')
            return redirect('create-task')
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
    context={"task_form":task_form,"task_detail_form":task_detail_form}
    return render(request,"task_form.html",context)


@login_required #login decorator
@permission_required('tasks.change_task',login_url='no-permission') #ekhane tasks model name and  add_task code name
def update_task(request,id):
    task=Task.objects.get(id=id)
    task_form=TaskModelForm(instance=task)
    
    if task.details:
        task_detail_form=TaskDetailModelForm(instance=task.details)
    
    if request.method=="POST":
        task_form=TaskModelForm(request.POST,instance=task)
        task_detail_form=TaskDetailModelForm(request.POST,instance=task.details)
        if task_form.is_valid() and task_detail_form.is_valid():
            
            """for model form"""
            task=task_form.save()
            task_detail=task_detail_form.save(commit=False)
            task_detail.task=task
            task_detail.save()
            messages.success(request,'Task Updated Successfully')
            return redirect('update-task',id)
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
    context={"task_form":task_form,"task_detail_form":task_detail_form}
    return render(request,"task_form.html",context)

@login_required #login decorator
@permission_required('tasks.delete_task',login_url='no-permission') #ekhane tasks model name and  add_task code name
def delete_task(request,id):
    if request.method=='POST':
        task=Task.objects.get(id=id)
        task.delete()
        messages.success(request,"Task deleted successfully")
        return redirect('manager-dashboard')
    else:
        messages.error(request,"Error!")
        return redirect('manager-dashboard')

@login_required #login decorator
@permission_required('tasks.view_task',login_url='no-permission') #ekhane tasks model name and  add_task code name
def view_task(request):
    tasks=Task.objects.all()
    task_3=Task.objects.get(id=1)
    pending_tasks=Task.objects.filter(status="PENDING")
    select_tasks=Task.objects.select_related("details").all()
    task_count=Task.objects.aggregate(num_task=Count('id'))
    task_count_under_project=Project.objects.annotate(num_task=Count('task'))
    return render(request,"show_task.html",{"tasks":tasks ,"tasks3":task_3,"pendingtasks":pending_tasks,"selecttasks":select_tasks,"task_count":task_count,"task_count_each":task_count_under_project})

@login_required
@permission_required('tasks.view_task',login_url='no-permission')
def task_details(request,task_id):
    task=Task.objects.get(id=task_id)
    status_choices=Task.STATUS_CHOICES
    if request.method =="POST":
        selected_status=request.POST.get('task_status')
        task.status=selected_status
        task.save()
        return redirect('task-details',task.id)
    return render(request,'task_details.html',{'task':task ,'status_choices':status_choices})

@login_required
def dashboard(request):
    if is_manager(request.user):
        return redirect('manager-dashboard')
    
    elif is_employee(request.user):
        return redirect('user-dashboard')
    
    elif is_admin(request.user):
        return redirect('admin-dashboard')
    
    return render('no-permission')