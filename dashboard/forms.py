from django import forms

class TestForm(forms.Form):
    test_title = forms.CharField()
    test_summary = forms.CharField(widget=forms.Textarea)