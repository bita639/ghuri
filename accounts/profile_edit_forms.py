
# from django.contrib.auth import get_user_model
# from .models import MyUser, Agency, Client, Admin
# from django import forms

# User = get_user_model()

# class UserProfileForm_MyUser(forms.ModelForm):

# 	full_name = forms.CharField(
# 		label='Full Name',
#             max_length=255,
#             required=True,
#             widget=forms.TextInput(
#                 attrs={'class': 'form-control', 'type': 'text','placeholder': 'John Smith'}
#             )
# 	)

# 	class Meta(object):
# 		model = MyUser
# 		fields = ['full_name']

# 	def save(self, commit=True):
# 		user = super(UserProfileForm_MyUser, self).save(commit=False)

# 		if commit:
# 			user.save()
# 		return user
	
# class UserProfileForm_Clients(forms.ModelForm):

# 	dob = forms.DateField(
#             label='DOB',
#             max_length=300,
#             required=False,
#             widget=forms.DateField(
#                 attrs={'class': 'form-control', 'type': 'date', 'placeholder':'01-01-1985'}
#             )
#         )
	
# 	nationality = forms.Select(
# 		label='Nationality',
#             max_length=300,
#             required=False,
#             widget=forms.TextInput(
#                 attrs={'class': 'form-control', 'placeholder':'Bangladeshi'}
#             )
# 	)

	
# 	languages = forms.CharField(
# 		label='Languages',
#         max_length=255,
#         required=False,
#         widget=forms.TextInput(
#             attrs={'class': 'form-control', 'type': 'text','placeholder': 'Bangla, English, Spanish'}
#         )
# 	)

#     occupation = forms.CharField(
#         label='Occupation',
#         max_length=255,
#         required=False,
#         widget=forms.

#     )
# 	class Meta(object):
# 		model = Client
# 		fields = ['username','full_name','email']

# 	def save(self, commit=True):
# 		user = super(UserProfileForm_Clients, self).save(commit=False)

# 		if commit:
# 			user.save()
# 		return user
	
