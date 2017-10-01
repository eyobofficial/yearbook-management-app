from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

# Import user authentication forms
from django.contrib.auth.forms import UserCreationForm

# Import models
from .models import StudentYearbook

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)

class YearbookForm(forms.ModelForm):
    class Meta:
        model = StudentYearbook
        fields = ['first_name', 'last_name', 'nickname', 'birthdate', 'bio', 'quote', 'thank_you_message',]

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
                    Fieldset(
                        '<span class="fa fa-user-circle"></span>&nbsp; Student Details',
                        'first_name',
                        'last_name',
                        'nickname',
                        'birthdate',
                    ),
                    Fieldset(
                        '<span class="fa fa-bullhorn"></span>&nbsp; Fun Stuffs',
                        'bio',
                        'quote',
                        'thank_you_message',
                    ),
                    ButtonHolder(
                        Submit('submit', 'Submit', css_class='btn btn-block btn-lg btn-primary')
                    )
                )
        super(YearbookForm, self).__init__(*args, **kwargs)

class YearbookSubmitForm(forms.Form):
    i_agree = forms.BooleanField('I confirm that the above profile!', help_text='Please confirm before you submit your profile')
