from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError


forbidden_users = ['admin', 'css', 'js', 'authenticate', 'login', 'logout', 'administrator', 'root',
	'email', 'user', 'join', 'sql', 'static', 'python', 'delete']


class SignUpForm(UserCreationForm):
    """Sign Up form for new users."""
    username = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name' , 'last_name' ,  'password1' , 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)


    def clean(self):

        # data from the form is fetched using super function
        super(SignUpForm, self).clean()

        # extract the username and text field from the data
        first_name = self.cleaned_data.get('first_name')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        username_list = list(username)
        periods_list = ['/','"', "'", '!', '#', '*', '%', '$', '^', '&', '(', ')', '+', ',', '?', '\\' ]


        if username:

        # conditions to be met for the username length
            if len(username) < 3:
                self._errors['username'] = self.error_class([
                'Minimum 3 characters required'])

            if username in forbidden_users:
                self._errors['username'] = self.error_class([
                'Invalid name for user, this is a reserverd word.'])

            for var in username:
                if var in  periods_list:
                    self._errors['username'] = self.error_class([
                    'Enter a valid username. This value may contain only letters, numbers, and @ . _ etc characters.'])

        if first_name:
            if len(first_name) < 2:
                self._errors['first_name'] = self.error_class([
                'Minimum 2 characters required'])

        if email:
            if User.objects.filter(email=email).exists():
                self._errors['email'] = self.error_class([
                'A user with this email already exists!'])

        # return any errors if found
        return self.cleaned_data

#Gender options
gender_choices = (
    ('Male','Male'),
    ('Female', 'Female'),
    )


class ProfileUpdateForm(forms.ModelForm):
    """Form to update/edit profile."""
    gender = forms.ChoiceField(choices=gender_choices)
    class Meta:
        model = Profile
        fields = ['gender', 'age' , 'bio', 'hometown', 'facebook', 'twitter', 'instagram', 'youtube']
        widgets = {
        'gender': forms.Select(choices=gender_choices),
        }

    def clean(self):

        # data from the form is fetched using super function.
        super(ProfileUpdateForm, self).clean()

        # extract the age from the data.
        age = self.cleaned_data.get('age')

        if age:
            if age < 12 or age > 150:
                 self._errors['age'] = self.error_class([
                'Age must be greater then 11 and less then 151.'])

        # return any errors if found
        return self.cleaned_data


class UserUpdateForm(forms.ModelForm):
    """Update user details."""
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    class Meta:
        model = User
        fields = ['username','first_name' , 'last_name', 'email']

    def clean(self):

        # data from the form is fetched using super function
        super(UserUpdateForm, self).clean()

        # extract the username and text field from the data
        first_name = self.cleaned_data.get('first_name')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        username_list = list(username)
        periods_list = ['/','"', "'", '!', '#', '*', '%', '$', '^', '&', '(', ')', '+', ',', '?', '\\' ]


        if username:

        # conditions to be met for the username length
            if len(username) < 3:
                self._errors['username'] = self.error_class([
                'Minimum 3 characters required'])

            for var in username:
                if var in  periods_list:
                    self._errors['username'] = self.error_class([
                    'Enter a valid username. This value may contain only letters, numbers, and @ . _ etc characters.'])

        if first_name:
            if len(first_name) < 2:
                self._errors['first_name'] = self.error_class([
                'Minimum 2 characters required'])

        if email:
            if User.objects.filter(email=email).exists():
                user_obj = User.objects.get(email=email)
                if user_obj.username != username:
                    self._errors['email'] = self.error_class([
                    'A user with this email already exists!'])

        # return any errors if found
        return self.cleaned_data


class ChangePasswordForm(forms.ModelForm):
	id = forms.CharField(widget=forms.HiddenInput())
	old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), label="Old password", required=True)
	new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), label="New password", required=True)
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), label="Confirm new password", required=True)

	class Meta:
		model = User
		fields = ('id', 'old_password', 'new_password', 'confirm_password')

	def clean(self):
		super(ChangePasswordForm, self).clean()
		id = self.cleaned_data.get('id')
		old_password = self.cleaned_data.get('old_password')
		new_password = self.cleaned_data.get('new_password')
		confirm_password = self.cleaned_data.get('confirm_password')
		user = User.objects.get(id=id)
		if not user.check_password(old_password):
			self._errors['old_password'] =self.error_class(['Old password do not match.'])
		if new_password != confirm_password:
			self._errors['new_password'] =self.error_class(['Passwords do not match.'])
		return self.cleaned_data
