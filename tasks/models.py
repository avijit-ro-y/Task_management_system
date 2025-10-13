from django.db import models

# Create your models here.

class Project(models.Model):
    name=models.CharField(max_length=100)
    start_date=models.DateField()

class Employee(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField(unique=True)
    
    def __str__(self):
        return self.name

class Task(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE,default=1)
    title=models.CharField(max_length=250)
    descripotion=models.TextField()
    assigned_to=models.ManyToManyField(Employee)
    due_date=models.DateField()
    is_completed=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now=True)
    
class TaskDetail(models.Model):
    High='H'
    Medium='M'
    Low='L'
    Priority_options=(
        ('H','High'),
        ('M','Medium'),
        ('L','Low'),
        
    )
    task=models.OneToOneField(Task,on_delete=models.CASCADE)
    assigned_to=models.CharField(max_length=100)
    priority=models.CharField(max_length=1,choices=Priority_options,default=Low)

