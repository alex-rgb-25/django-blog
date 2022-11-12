from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Blog

# class RegisterForm(UserCreationForm):

#     class Meta:
#         model = User
#         fields = ["username","password1", "password2"]
#         widgets = {
#             "sent_to" : forms.TextInput(attrs={'class':'form-control', 'placeholder':""}),
#         }

#     #clear helper messages
#     def __init__(self, *args, **kwargs):
#         super(RegisterForm, self).__init__(*args, **kwargs)

#         for fieldname in ['username', 'password1', 'password2']:
#             self.fields[fieldname].help_text = None


class PostForm(forms.Form):
    title = forms.CharField(label="Title:", max_length=60,)
    url = forms.CharField(label="Image URL:", max_length=600, required=False)
    text= forms.CharField(widget=forms.Textarea(attrs={"rows":6, "cols":40}))
    tags = forms.CharField(label="Tags:", max_length=60, required=False,
     widget=forms.TextInput(attrs={'placeholder': 'comma separated values'})
     )


class SearchForm(forms.Form):
    tag = forms.CharField(label="", max_length=60, 
    widget=forms.TextInput(attrs={'placeholder': 'eg: seasons, cat'}))



# custom login form
class MyAuthForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username','password']
    def __init__(self, *args, **kwargs):
        super(MyAuthForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'})
        self.fields['username'].label = False
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'password'}) 
        self.fields['password'].label = False


        # custom register form
class MyRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1', 'password2']
    def __init__(self, *args, **kwargs):
        super(MyRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'})
        self.fields['username'].label = False
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'password'}) 
        self.fields['password1'].label = False
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'repeat password'}) 
        self.fields['password2'].label = False

        for fieldname in ['username', 'password1', 'password2']:
             self.fields[fieldname].help_text = None


# custom comment form

class CommentForm(forms.Form):
    comment = forms.CharField(label="", max_length=200, 
    widget=forms.TextInput(attrs={'placeholder': 'write a comment...'}))


class EditForm(forms.Form):
    title = forms.CharField(label="Title:", max_length=60,)
    url = forms.CharField(label="Image URL:", max_length=600, required=False)
    text= forms.CharField(widget=forms.Textarea(attrs={"rows":6, "cols":40}))
    tags = forms.CharField(label="Tags:", max_length=60, required=False,
     widget=forms.TextInput(attrs={'placeholder': 'comma separated values'})
     )