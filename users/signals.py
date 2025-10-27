from django.dispatch import receiver
from django.db.models.signals import post_save 
from django.contrib.auth.models import User,Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail

@receiver(post_save,sender=User)
def send_activation_email(sender,instance,created,**kwargs):
    if created:
        token=default_token_generator.make_token(instance)
        activation_url=f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/"
        
        #email properties
        subject='Activation id'
        message=f'Hi {instance.username},\n\n\Please activate your id by the link {activation_url}'
        recipient_list=[instance.email]
        
        try: #error avoid korar jonno
            send_mail(subject,message,settings.EMAIL_HOST_USER,recipient_list)
        except Exception as e:
            print(f"Failed to sent mail to {instance.username} for the error {str(e)}")
            
@receiver(post_save,sender=User)
def assign_role(sender,instance,created,**kwargs):
    if created:
        user_group,created=Group.objects.get_or_create(name='User') #previously group thakle get korbe ar new hole create korbe...and user ekhane group name
        instance.groups.add(user_group)
        instance.save()