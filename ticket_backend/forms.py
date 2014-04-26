from django import forms

class ActivityForm(forms.Form):
    caption = forms.CharField(label='caption', max_length=100)
    destruction = forms.CharField(widget=forms.Textarea)
    

class CatagoryForm(forms.Form):
    catagory_name = forms.CharField()