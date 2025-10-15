from django import forms
from tasks.models import Task,TaskDetail

class TaskForm(forms.Form):
    title=forms.CharField(max_length=250)
    descripotion=forms.CharField(widget=forms.Textarea)
    due_date=forms.DateField(widget=forms.SelectDateWidget)
    assigned_to=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=[])
    
    def __init__(self,*args,**kwargs):
        employees=kwargs.pop("employees",[])
        super().__init__(*args,**kwargs)
        self.fields['assigned_to'].choices=[(emp.id,emp.name) for  emp in employees]

class StyledFormMixin:
    default_classes="border-2 border-gray-200 w-full rounded-lg shadow-sm focus:border-rose-300 focus:ring-rose-500"
    def apply_styled_widget(self):
        for filed_name,field in self.fields.items():
            if isinstance(field.widget,forms.TextInput):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder':f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder':f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class':self.default_classes
                })
            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class':"space-y-2"
                })
            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })
        
        

       
class TaskModelForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model=Task
        fields='__all__'
        widget={
            'due_date':forms.SelectDateWidget,
            'asssigned_to':forms.CheckboxSelectMultiple
        }
        # widgets={
        #     'title':forms.TextInput(attrs={
        #         "class":,
        #         "placeholder":'Enter task title'
        #         }
        #     ),
        #     'description':forms.TextInput(attrs={
        #         "class":"border-2 border-gray-200 w-full rounded-lg shadow-sm focus:border-rose-300 focus:ring-rose-500",
        #         "placeholder":'Enter description'
        #         }
        #     ),
        #     'due_date':forms.SelectDateWidget(attrs={
        #         "class":"border-2 border-gray-200 w-full rounded-lg shadow-sm focus:border-rose-300 focus:ring-rose-500",
        #         }
        #     ),
        #     'assigned_to':forms.CheckboxSelectMultiple(attrs={
        #         "class":"border-2 border-gray-200 w-full rounded-lg shadow-sm focus:border-rose-300 focus:ring-rose-500",
        #         "placeholder":'Enter name'
        #         }
        #     )
        # }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.apply_styled_widget()
        
class TaskDetailModelForm(StyledFormMixin,forms.ModelForm):
    class  Meta:
        model=TaskDetail
        fields=['priority','notes']
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.apply_styled_widget()