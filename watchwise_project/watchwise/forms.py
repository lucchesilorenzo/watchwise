from django import forms
from .models import Profile


class NameForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)
    your_data = forms.DateField(label="Your Date")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["user", "birth_date",]