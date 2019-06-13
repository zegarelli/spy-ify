from django import forms

class PostForm(forms.Form):
    summary = forms.CharField(label='Post Summary', max_length=100)
    text = forms.TextInput()
    related_posts = forms.CheckboxSelectMultiple()
