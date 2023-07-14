from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django import forms

class NewTicketForm(forms.Form):
    subject = forms.CharField(max_length=100)
    body = forms.CharField(widget=forms.Textarea)
    priority = forms.ChoiceField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Email or Username')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': True})

    def clean_username(self):
        username = self.cleaned_data['username']
        if '@' in username:
            return username.lower() 
        return username