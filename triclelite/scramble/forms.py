from django import forms

class ScrambleForm(forms.Form):
    key_one = forms.CharField(label='', max_length=256, widget=forms.TextInput(attrs={'placeholder': 'Enter your first key'}))
    key_two = forms.CharField(label='', max_length=256, widget=forms.TextInput(attrs={'placeholder': 'Enter your second key'}))
    key_three = forms.CharField(label='', max_length=256, widget=forms.TextInput(attrs={'placeholder': 'Enter your third key'}))

    retrieve_token = forms.CharField(label='', max_length=256, widget=forms.TextInput(attrs={'placeholder': 'retrieve_token'}))

    CHOICES=[('Scramble','Scramble'), ('Unscramble','Unscramble')]
    mode = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class':'regDropDown'}))

    zipcode = forms.CharField(label='', required=False, max_length=256, widget=forms.TextInput(attrs={'placeholder': 'Enter your zip file password'}))

    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True,}))
