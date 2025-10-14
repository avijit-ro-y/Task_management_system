from django.db import models

# Create your models here.

class Project(models.Model):
    name=models.CharField(max_length=100)
    start_date=models.DateField()
    description=models.TextField(blank=True,null=True)
    def __str__(self):
        return self.name
    

class Employee(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField(unique=True)
    
    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES=[
        ('PENDING','Pending'),
        ('IN_PROGRESS','In Progress'),
        ('COMPLETED','Completed'),
    ]
    project=models.ForeignKey(Project,on_delete=models.CASCADE,default=1)
    title=models.CharField(max_length=250)
    description =models.TextField() 
    assigned_to=models.ManyToManyField(Employee)
    due_date=models.DateField()
    status=models.CharField(max_length=30,choices=STATUS_CHOICES,default='PENDING')
    is_completed=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    
class TaskDetail(models.Model):
    High='H'
    Medium='M'
    Low='L'
    Priority_options=(
        ('H','High'),
        ('M','Medium'),
        ('L','Low'),
        
    )
    task=models.OneToOneField(Task,on_delete=models.CASCADE,related_name="details")
    assigned_to=models.CharField(max_length=100)
    priority=models.CharField(max_length=1,choices=Priority_options,default=Low)
    notes=models.TextField(blank=True,null=True)
    def __str__(self):
        return f"Details form task {self.task.title}"
