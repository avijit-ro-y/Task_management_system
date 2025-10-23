from django.db.models.signals import post_delete,m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from tasks.models import Task


@receiver(m2m_changed,sender=Task.assigned_to.through) #decorator ekta function er behavior internally change korte help kore  
def notify_employee_on_task_creation(sender,instance,action,**kwargs):
    if action=='post_add':
        assigned_mail=[emp.email for emp in instance.assigned_to.all()]
        send_mail(
            "New task assigned", #email message subject
            f"You have assigned to {instance.title}", #mail message
            "avijitroy926avijit@gmail.com", #sender
            assigned_mail, #receiver
        )
    instance.is_completed=True #jodi kono task is completed optione click kora chara save kora hoy tahole seta automatically is completed hoye jae(tik chinho diye)

@receiver(post_delete,sender=Task)
def delete_associate_details(sender,instance,**kwargs):
    if instance.details:
        instance.details.delete() #details task  class er related name
        print("Delete sucessfully")