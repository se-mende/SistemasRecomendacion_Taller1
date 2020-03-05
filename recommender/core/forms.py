from django import forms

class SearchUserForm(forms.Form):
    query = forms.CharField(label='Id o nombre', 
                            max_length=100, 
                            min_length=4, 
                            required=True, 
                            help_text='')
    

