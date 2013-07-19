from django import forms
from django.contrib.auth.models import User	# Gives access to user objects
from django.forms import ModelForm			# Lets us pass a model to the form; django will create a form from the model
from chirp.models import Chirper

class RegistrationForm(ModelForm):
	username	= forms.CharField(label=(u'Username'))			# The 'u' means that it's unicode
	email		= forms.EmailField(label=(u'Email Address'))	# django will automatically validate email address
	password	= forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False)) # Make password input hidden
	password1	= forms.CharField(label=(u'Confirm Password'), widget=forms.PasswordInput(render_value=False))

	class Meta:
		model = Chirper # Takes chirper model and makes form from it
		exclude = ('user',)
		
	def clean_username(self):
		username = self.cleaned_data['username'] # form data after we've posted it to the view is stored into local variable 'username'
		try: # see if username exists
			User.objects.get(username=username)
		except User.DoesNotExist: # if username is available, we're good
			return username
		raise forms.ValidationError("Username in unavailable.")
	 	
	def clean(self):
		if 'password' not in self.cleaned_data or 'password1' not in self.cleaned_data:
			raise forms.ValidationError("Password fields must not be empty.")
		if self.cleaned_data['password'] != self.cleaned_data['password1']:
		
			# The next line is important because without it the ValidationError would be stored in "Form.non_field_errors()" and wouldn't
			# display on either of the two password fields. Here we're setting and assigning the error manually.
			self._errors["password1"] = self.error_class([u'Passwords do not match.'])
			raise forms.ValidationError("The passwords do not match.") #This won't display, but it's necessary to indicate that there was a ValidationError
		else:
			return self.cleaned_data
			
class LoginForm(forms.Form):
	username	= forms.CharField(label=(u'User Namer'))
	password	= forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))