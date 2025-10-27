from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from django.contrib.auth import login,logout
#from users.forms import RegisterForm,CustomRegisterForm
from users.forms import CustomRegisterForm
from django.contrib import messages
from users.forms import LoginForm,AssignRoleForm,CreateGroupForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test

# Create your views here.
def sign_up(request):
    if request.method=='GET':
        form=CustomRegisterForm()
        
    if request.method=='POST':
        form=CustomRegisterForm(request.POST) #user er deya datagulo onno jaygay store kora
        if form.is_valid():
            # username=form.cleaned_data.get('username')
            # password=form.cleaned_data.get('password1')
            # confirm_password=form.cleaned_data.get('password2')
            # if password==confirm_password:
            #     User.objects.create(username=username,password=password)
            # else:
            #     print('Password are not same')
            
            user=form.save(commit=False) #user er datagulo neya holo
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active=False #activate status ta false kore deya holo jeno activation link chara login korte na pare
            user.save()
            messages.success(request,"A mail sent for activation!")
            return redirect('sign-in')
    context={
    'form':form,
    }   
    return render(request,'registration/register.html',context)

def sign_in(request):
    form=LoginForm()
    if request.method=='POST':
        form=LoginForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            # username=request.POST.get('username')
            # password=request.POST.get('password')
            
            # user=authenticate(request,username=username,password=password)
            login(request,user)
            return redirect('home')
    return render(request,'registration/login.html',{'form':form})

@login_required #ei decorator use kora hoy jate keu login chara access korte na pare
def sign_out(request):
    if request.method=='POST':
        logout(request)
        return redirect('home')
    
def activate_user(request,user_id,token):
    try:
        user=User.objects.get(id=user_id)
        if default_token_generator.check_token(user,token):
            user.is_active=True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse("Invalid token!")
    except  User.DoesNotExist:
        return HttpResponse("User not found!!")

#test for user...it will check if the user is admin or not
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

@user_passes_test(is_admin,login_url='no-permission') #ei decorator ekta function ney jeta true hole next step e jete dey...otherwise na 
def admin_dashboard(request):
    users=User.objects.all()
    return render(request,'admin/dashboard.html',{"users":users})

@user_passes_test(is_admin,login_url='no-permission')  
def assign_role(request,user_id):
    user=User.objects.get(id=user_id)
    form=AssignRoleForm() #form ta k patahy deya holo
    if request.method=="POST":
        form=AssignRoleForm(request.POST)
        if form.is_valid():
            role=form.cleaned_data.get('role') #role ta ke  ber kore ana holo
            user.groups.clear() #remove old role 
            user.groups.add(role) 
            messages.success(request,f"User {user.username} has been assigned  to the {role.name} role")
            return redirect('admin-dashboard')
    return render(request,'admin/assign_role.html',{"form":form})

@user_passes_test(is_admin,login_url='no-permission')  
def create_group(request):
    form=CreateGroupForm() #form ta k patahy deya holo
    if request.method=="POST":
        form=CreateGroupForm(request.POST)
        if form.is_valid():
            group=form.save()
            messages.success(request,f"Group {group.name} has been created sucessfully!")
            return redirect('create-group')
    return render(request,'admin/create_group.html',{"form":form})

@user_passes_test(is_admin,login_url='no-permission')  
def group_list(request):
    groups=Group.objects.all()
    return render(request,'admin/group_list.html',{"groups":groups})

