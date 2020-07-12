
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import MyUser, Agency, Client, Admin
from django.forms import inlineformset_factory
from django import forms
from django_countries.data import COUNTRIES
User = get_user_model()

class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
		attrs={'class': 'form-control', 'type': 'password', 'placeholder':'Type your Password'}
			)
		)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(
		attrs={'class': 'form-control', 'type': 'password', 'placeholder':'Please Re-enter your Password'}
            )
		)
	username = forms.CharField(
            label='Username',
            max_length=300,
            required=True,
            widget=forms.TextInput(
                attrs={'class': 'form-control', 'type': 'text', 'placeholder':'e.g: Jhon6969'}
            )
        )
	
	email = forms.EmailField(
		label='Email Address',
            max_length=300,
            required=True,
            widget=forms.TextInput(
                attrs={'class': 'form-control', 'type': 'email', 'placeholder':'Example@example.com'}
            )
	)

	mobile_no = forms.CharField(
		label='Contact No',
            max_length=20,
            required=True,
            widget=forms.TextInput(
                attrs={'class': 'form-control', 'type': 'tel','placeholder': '+8801677088385'}
            )
	)

	full_name = forms.CharField(
		label='Full Name',
            max_length=255,
            required=True,
            widget=forms.TextInput(
                attrs={'class': 'form-control', 'type': 'text','placeholder': 'John Smith'}
            )
	)



	class Meta(object):
		model = MyUser
		fields = ['username','full_name','email', 'mobile_no']
		widgets = {
                    'user_type': forms.HiddenInput()
                }

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if not password2:
			raise forms.ValidationError("You must confirm your password")
		if password1 != password2:
			raise forms.ValidationError("Your passwords do not match")
		return password2

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])

		if commit:
			user.save()
		return user
	
class AgencyCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
		attrs={'class': 'form-control', 'type': 'password', 'placeholder':'Type your Password'}
			)
		)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(
		attrs={'class': 'form-control', 'type': 'password', 'placeholder':'Please Re-enter your Password'}
            )
		)
	username = forms.CharField(
            label='Username',
            max_length=300,
            required=True,
            widget=forms.TextInput(
                attrs={'class': 'form-control', 'type': 'text', 'placeholder':'e.g: Jhon6969'}
            )
        )
	
	email = forms.EmailField(
		label='Email Address',
            max_length=300,
            required=True,
            widget=forms.TextInput(
                attrs={'class': 'form-control', 'type': 'email', 'placeholder':'Example@example.com'}
            )
	)

	mobile_no = forms.CharField(
		label='Contact No',
            max_length=20,
            required=True,
            widget=forms.TextInput(
                attrs={'class': 'form-control', 'type': 'tel','placeholder': '+8801677088385'}
            )
	)

	full_name = forms.CharField(
		label='Company Name',
            max_length=100,
            required=True,
            widget=forms.TextInput(
                attrs={'class': 'form-control', 'type': 'text',
                       'placeholder': 'Holiday Tours & Travels'}
            )
	)



	class Meta(object):
		model = MyUser
		fields = ['username','full_name','email', 'mobile_no']
		widgets = {
                    'user_type': forms.HiddenInput()
                }

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if not password2:
			raise forms.ValidationError("You must confirm your password")
		if password1 != password2:
			raise forms.ValidationError("Your passwords do not match")
		return password2

	def save(self, commit=True):
		user = super(AgencyCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])

		if commit:
			user.save()
		return user

class MyUserForm(forms.ModelForm):

	# password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
	# 	attrs={'class': 'form-control', 'type': 'password', 'placeholder':'Type your Password'}
	# 		)
	# 	)
	# password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(
	# 	attrs={'class': 'form-control', 'type': 'password', 'placeholder':'Please Re-enter your Password'}
    #         )
	# 	)
	username = forms.CharField(
            label='Username',
            max_length=300,
            required=True,
            widget=forms.TextInput(
                attrs={'placeholder':'e.g: Jhon6969'}
            )
        )
	
	email = forms.EmailField(
		label='Email Address',
            max_length=300,
            required=True,
            widget=forms.TextInput(
                attrs={ 'placeholder':'Example@example.com'}
            )
	)

	mobile_no = forms.CharField(
		label='Contact No',
            max_length=20,
            required=True,
            widget=forms.TextInput(
                attrs={'placeholder': '+8801677088385'}
            )
	)

	full_name = forms.CharField(
		label='Name',
            max_length=255,
            required=True,
            widget=forms.TextInput(
                attrs={'placeholder': 'John Smith'}
            )
	)
	class Meta(object):
		model = MyUser
		fields = ['username', 'full_name', 'email', 'mobile_no']
		exculde = ('password1','password2')
		widgets = {
                    'user_type': forms.HiddenInput()
                }
	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if not password2:
			raise forms.ValidationError("You must confirm your password")
		if password1 != password2:
			raise forms.ValidationError("Your passwords do not match")
		return password2

	def save(self, commit=True):
		user = super(MyUserForm, self).save(commit=False)
		# user.set_password(self.cleaned_data['password1'])

		if commit:
			user.save()
		return user

class AgencyForm(forms.ModelForm):

	class Meta(object):
		model = Agency
		fields = ['website', 'address', 'country']


class AdminCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
		attrs={'class': 'form-control', 'type': 'password', 'placeholder':'Type your Password'}
			)
		)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(
		attrs={'class': 'form-control', 'type': 'password', 'placeholder':'Please Re-enter your Password'}
            )
		)
	username = forms.CharField(
            label='Username',
            max_length=300,
            required=True,
            widget=forms.TextInput(
                attrs={'class': 'form-control', 'type': 'text', 'placeholder':'e.g: Jhon6969'}
            )
        )
	
	email = forms.EmailField(
		label='Email Address',
            max_length=300,
            required=True,
            widget=forms.TextInput(
                attrs={'class': 'form-control', 'type': 'email', 'placeholder':'Example@example.com'}
            )
	)





	class Meta(object):
		model = MyUser
		fields = ['username','email']
		widgets = {
                    'user_type': forms.HiddenInput()
                }

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if not password2:
			raise forms.ValidationError("You must confirm your password")
		if password1 != password2:
			raise forms.ValidationError("Your passwords do not match")
		return password2

	def save(self, commit=True):
		user = super(AdminCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])

		if commit:
			user.save()
		return user

		


class UserLoginForm(forms.Form):
	email = forms.CharField(label='Email Address',
	 widget=forms.PasswordInput(
		attrs={'class': 'form-control', 'type': 'email','placeholder': 'Type your Registered Email'}
            )
	)
	password = forms.CharField(label='Password', widget=forms.PasswordInput
                            (
                                attrs={'class': 'form-control', 'type': 'password',
                                       'placeholder': 'Please Type your Password'}
                            )
	)

	def clean(self, *args, **kwargs):
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')
		user_qs_final = User.objects.filter(
            	 Q(username__iexact=email) |
				Q(email__iexact=email)
			).distinct()

		if not user_qs_final.exists() and user_qs_final.count != 1:
			raise forms.ValidationError("Invalid credentials - user does note exist")
		user_obj = user_qs_final.first()

		if not user_obj.check_password(password):
			raise forms.ValidationError("credentials are not correct")
		
		self.cleaned_data["user_obj"] = user_obj
		return super(UserLoginForm, self).clean(*args, **kwargs)
		

# def loginPage(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.info(request, 'Username or Password is incorrect')

#     context = {}
#     return render(request, 'pyapp/login.html', context)


class UserProfileForm_MyUser(forms.ModelForm):

	full_name = forms.CharField(
		label='Full Name',
            max_length=255,
            required=True,
            widget=forms.TextInput(
                attrs={'class': 'form-control', 'type': 'text','placeholder': 'John Smith'}
            )
	)

	class Meta(object):
		model = MyUser
		fields = ['full_name']

	
class UserProfileForm_Clients(forms.ModelForm):
	nationality_option = [('Bangladeshi', 'Bangladeshi'),('Indian', 'Indian'),('Chinese', 'Chinese'),('Japanese', 'Japanese')]
	photo = forms.ImageField(
		label='Upload Your Photo',
        required=False,
		widget=forms.FileInput(attrs={'class': 'form-control'}))

		
	
	dob = forms.DateField(
		label='Date of Birth',
		required=False,
		widget=forms.DateTimeInput(
			attrs={'class': 'form-control datetimepicker-input', 'type':'date'}
		)
	)
	nationality = forms.ChoiceField(
		label='Nationality',
        required=False,
		choices=nationality_option,
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
	)
	languages = forms.CharField(
		label='Languages',
		max_length=255,
		required=False,
		widget=forms.TextInput(
			attrs={'class': 'form-control', 'type': 'text',
                            'placeholder': 'Bangla, English, Spanish'}
		)
	)
	occupation = forms.CharField(
		label='Occupation',
		max_length=20,
		required=False,
		widget=forms.TextInput(
			attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'E.g: Doctor'}
                    )
	)
	website = forms.URLField(
		label='Website',
		max_length=40,
		required=False,
		widget=forms.URLInput(
			attrs={'class': 'form-control', 'placeholder': 'E.g: www.ghuri.com'}
		)
		
	)
	phone = forms.CharField(
		label='Contact No',
		max_length=20,
		required=False,
		widget=forms.TextInput(
			attrs={
				'class': 'form-control', 'type': 'text', 'placeholder': '+39 12863548497'}
		)
	)
	passport_no = forms.CharField(
		label='Passport No',
		max_length=10,
		required=False,
        				widget=forms.TextInput(
                                            attrs={
                                            	'class': 'form-control', 'type': 'text', 'placeholder': 'BG 0367345'}
                                        )
	)
	issue_date = forms.DateField(
		label='Issue Date',
		required=False,
		widget=forms.DateTimeInput(
			attrs={'class': 'form-control', 'type': 'date'}
		)
	)
	expiry_date = forms.DateField(
		label='Expiry Date',
		required=False,
		widget=forms.DateTimeInput(
			attrs={'class': 'form-control', 'type': 'date'}
		)
	)
	height = forms.IntegerField(
		label='Heigh in INCH',
		required=False,
		widget=forms.NumberInput(
			attrs={'class': 'form-control', 'type': 'number', 'placeholder': '178'}
		)
	)
	dietery_requirement = forms.CharField(
		label='Dietary Requirement',
		required=False,
		widget=forms.Textarea(
			attrs={'class': 'form-control', 'type': 'text',
                            'placeholder': 'Enter your dietary requirements, E.g vegeterian, vegan, jain, kosher, halal etc.'}
		)
	)
	medical_condition = forms.CharField(
		label='Medical Conditions',
		required=False,
		widget=forms.Textarea(
			attrs={'class': 'form-control', 'type': 'text',
                            'placeholder': 'Enter any medical conditions that are relevant from a travel perspective.'}
		)
	)
	country = forms.ChoiceField(
		choices = sorted(COUNTRIES.items()),
		widget=forms.Select(
            attrs={'class': 'form-control'}
        )
	)

	class Meta(object):
		model = Client
		fields = ['photo', 'dob', 'nationality', 'languages', 'occupation', 'website', 'phone', 'passport_no',
           'issue_date', 'expiry_date', 'height', 'dietery_requirement', 'medical_condition', 'country']

	# def __init__(self, *args, **kwargs):
	# 	super().__init__(*args, **kwargs)
	# 	self.fields['url'].widget.attrs.update({'class': 'form-control'})
        


# class UserPasswordForm(forms.ModelForm):
# 	password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
# 		attrs={'class': 'form-control', 'type': 'password', 'placeholder':'Type your Password'}
# 			)
# 		)
# 	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(
# 		attrs={'class': 'form-control', 'type': 'password', 'placeholder':'Please Re-enter your Password'}
#             )
# 		)

# 	def clean_password2(self):
# 		password1 = self.cleaned_data.get('password1')
# 		password2 = self.cleaned_data.get('password2')

# 		if not password2:
# 			raise forms.ValidationError("You must confirm your password")
# 		if password1 != password2:
# 			raise forms.ValidationError("Your passwords do not match")
# 		return password2

# 	def save(self, commit=True):
# 		user = super(UserCreationForm, self).save(commit=False)
# 		user.set_password(self.cleaned_data['password1'])

# 		if commit:
# 			user.save()
# 		return user