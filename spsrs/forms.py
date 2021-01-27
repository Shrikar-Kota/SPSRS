from django import forms
from django.contrib.auth import authenticate
from spsrs.models import user, feedback, student
from django.contrib.auth.forms import UserCreationForm

# class UserRegistrationForm(UserCreationForm):
# 	rollno = forms.CharField(max_length=12, help_text='Required. Add a valid rollno.')

# 	class Meta:
# 		model = user
# 		fields = ('rollno', 'password1', 'password2')
# 	def clean(self):
# 		if self.is_valid():
# 			rollno = self.cleaned_data['rollno']
# 			password = self.cleaned_data['password1']

class UserAuthenticationForm(forms.ModelForm):
	password = forms.CharField(label = 'password', widget = forms.PasswordInput)

	class Meta:
		model = user
		fields = ('rollno', 'password')

	def clean(self):
		if self.is_valid():
			rollno = self.cleaned_data['rollno']
			password = self.cleaned_data['password']
			if not authenticate(rollno= rollno, password= password):
				raise forms.ValidationError('Invalid Login')
class FeedbackForm(forms.ModelForm):

	class Meta:
		model = feedback
		fields = ('rollno','First','second','third','fourth','fifth','suggestion')
class StudentRegistrationForm(forms.ModelForm):
	
	class Meta:
		model = student
		fields = ('rollno','name', 'dob', 'section', 'year')
class ViewForm(forms.ModelForm):

	class Meta:
		model = student
		fields = ('section', 'year')
class Update1Form(forms.ModelForm):
	height_one				= forms.FloatField()
	weight_one				= forms.FloatField()
	class Meta:
		model = student
		fields = ('height_one','weight_one')
class Update2Form(forms.ModelForm):
	height_two				= forms.FloatField()
	weight_two				= forms.FloatField()
	class Meta:
		model = student
		fields = ('height_two','weight_two')
class FbStudentForm(forms.ModelForm):

	feedback = forms.CharField(max_length = 500)
	class Meta:
		model = student
		fields = ('feedback',)