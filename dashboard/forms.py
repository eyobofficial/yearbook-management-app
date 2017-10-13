from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

# Import user authentication forms
from django.contrib.auth.forms import UserCreationForm

# Import Auth Models
from django.contrib.auth.models import User

# Import models
from .models import (Profile,
                     StudentYearbook,
                     Poll,
                     PollChoice,
                     Vote,
                     )

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)

class YearbookForm(forms.ModelForm):
    class Meta:
        model = StudentYearbook
        fields = ['first_name', 'last_name', 'nickname', 'birthdate', 'gown_photo', 'suit_photo', 'baby_photo', 'bio', 'quote', 'thank_you_message',]

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
                        '<span class="fa fa-camera"></span>&nbsp; Pictures',
                        'gown_photo',
                        'suit_photo',
                        'baby_photo',
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
    i_agree = forms.BooleanField(label='&nbsp; I confirm I have checked all the details are mine.')

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll 
        fields = ('poll_text', 'description',)

class UserAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',]

        def __init__(self, *args, **kwargs):
            self.helper = FormHelper()
            self.helper.layout = Layout(
                        Fieldset(
                            '<span class="fa fa-user-circle"></span>&nbsp; Student Details',
                            'first_name',
                            'last_name',
                            'email',
                        ),
                        ButtonHolder(
                            Submit('submit', 'Update Profile', css_class='btn btn-lg btn-primary')
                        )
                    )
            super(UserAccountForm, self).__init__(*args, **kwargs)