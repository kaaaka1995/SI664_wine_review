from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from winereviews.models import Wine
from django.forms import ModelForm, Textarea,ModelMultipleChoiceField,fields
from .models import *



class WineForm(forms.ModelForm):
    
    
    class Meta:
        model = Wine
        fields = '__all__'
        
        #fields = ('wine_name','taster',)
       
        # widgets = {
        #     #'description': Textarea(attrs={'cols': 80, 'rows': 10}),
        #     'description':forms.MultipleChoiceField()
        # }

  
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'submit'))


# class WineForm(forms.ModelForm):
#     description_list = fields.CharField(required=False, widget=forms.Textarea())

#     class Meta:
#         model = Wine
#         exclude = ('description',)

#     def clean_actors_list(self):
#         data = self.cleaned_data
#         description_list = data.get('description_list', None)
#         if description_list is not None:
#             for text in description_list.split(';'):
#                 Description(description_text=text).save2()

#         return description_list

#     def save2(self, commit=False):
#         mminstance = super(WineForm, self)#.save(commit=False)
#         description_list = self.cleaned_data.get('description_list', None)
#         if description_list is not None:
#             for text in description_list.split(";"):
#                 d=Description(description_text=text)
#                 d.save()
#                 mminstance.description.add(d)

#         mminstance.save(commit=True)
#         return mminstance

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_method = 'post'
#         self.helper.add_input(Submit('submit', 'submit'))









# class ModelCommaSeparatedChoiceField(ModelMultipleChoiceField):
#     widget = Textarea
#     def clean(self, value):
#         if value is not None:
#             value = [item.strip() for item in value.split(";")] # remove padding
#         return super(ModelCommaSeparatedChoiceField, self).clean(value)

# class WineForm(forms.ModelForm):
#     description = ModelCommaSeparatedChoiceField(
#                required=False, 
#                queryset=Description.objects.filter(), 
#                to_field_name='description_text')
    
#     class Meta:
#         model = Wine
#         fields = '__all__'
#         #fields = ('wine_name','taster',)
       
#         # widgets = {
#         #     #'description': Textarea(attrs={'cols': 80, 'rows': 10}),
#         #     'description':forms.MultipleChoiceField()
#         # }

  
        

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_method = 'post'
#         self.helper.add_input(Submit('submit', 'submit'))