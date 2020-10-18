from django.db import models
import uuid

# Create your models here.
from django.core.validators import RegexValidator

from django.contrib.auth.models import (
		BaseUserManager, AbstractBaseUser, User
	)
from django.db.models.signals import post_save
from django.dispatch import receiver

USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'


class MyUserManager(BaseUserManager):
	def create_user(self, username, email, password=None):
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
					username = username,
					email = self.normalize_email(email)
				)
		user.set_password(password)
		user.save(using=self._db)
		return user
		# user.password = password # bad - do not do this

	def create_superuser(self, username, email, password=None):
		user = self.create_user(
				username, email, password=password
			)
		user.is_admin = True
		user.is_staff = True
		user.save(using=self._db)
		return user



class MyUser(AbstractBaseUser):
	user_id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
	username = models.CharField(
					max_length=15,
					validators = [
						RegexValidator(regex = USERNAME_REGEX,
										message='Username must be alphanumeric or contain numbers',
										code='invalid_username'
							)],
					unique=True
				)
	email = models.EmailField(
			max_length=255,
			unique=True,
			verbose_name='email address'
		)
	full_name = models.CharField(max_length=255, blank=True, null=True)
	mobile_no = models.CharField(max_length=20, unique=True, null=True)
	user_type = models.CharField(max_length=200, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)

	objects = MyUserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	def __str__(self):
		return self.username

	def get_short_name(self):
		# The user is identified by their email address
		return self.username


	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True

class Admin(models.Model):
	ROLE = (
        ('admin', 'admin'),
        ('editor', 'editor'),
		)
	admin_id = models.AutoField(primary_key=True)
	user = models.OneToOneField(MyUser, on_delete=models.CASCADE,related_name='admin')
	name = models.CharField(max_length=200, null=True)
	role = models.CharField(max_length=200, blank=True, null=True, choices=ROLE)
	photo = models.FileField(upload_to="profileImage", default='profileImage/blank.png', blank=True, null=True)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


class Client(models.Model):
	client_id = models.AutoField(primary_key=True)
	user_id = models.OneToOneField(MyUser, on_delete=models.CASCADE,related_name='client')
	name = models.CharField(max_length=200, null=True)
	photo = models.FileField(upload_to="profileImage", default='profileImage/blank.png', blank=True, null=True)
	dob = models.DateField(null=True)
	nationality = models.CharField(max_length=50, blank=True,null=True)
	languages = models.CharField(max_length=200, blank=True, null=True)
	occupation = models.CharField(max_length=50, blank=True, null=True)
	website = models.URLField(max_length=250, blank=True, null=True)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone = models.CharField(validators=[phone_regex], max_length=12, unique=True, blank=True, null=True)
	passport_regex = RegexValidator(regex=r'^(?!^0+$)[a-zA-Z0-9]{3,20}$', message="Passport number must be entered in the format: 'BB 0351657'. ")
	passport_no = models.CharField(validators=[passport_regex],max_length=10, unique=True, blank=True,null=True)
	issue_date = models.DateField(null=True)
	expiry_date = models.DateField(null=True)
	height = models.IntegerField(blank=True, null=True)
	dietery_requirement = models.CharField(max_length=500, blank=True,null=True)
	medical_condition = models.CharField(max_length=500, blank=True, null=True)
	country = models.CharField(max_length=44, blank=True, null=True)
	
	
	def __str__(self):
		return self.name


class Agency(models.Model):
    agency_id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(MyUser, on_delete=models.CASCADE, blank=True, null=True,related_name='agency')
    name = models.CharField(max_length=200, null=True)
    website = models.URLField(max_length=250, blank=True, null=True)
    photo = models.FileField(upload_to="profileImage", default='profileImage/blank.png', blank=True, null=True)
    total_package = models.IntegerField(null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
	
    def __str__(self):
        return self.name





@receiver(post_save, sender=MyUser)
def create_admin(sender, instance, created, **kwargs):
	if created:
		if instance.user_type == 'client':
			qs = Client.objects.filter(user_id=instance)
			if not qs.exists():
				Client.objects.create(
					user_id=instance, name=instance.username
				)
		elif instance.user_type == 'agency':
			qs = Agency.objects.filter(user_id=instance)
			if not qs.exists():
				Agency.objects.create(
					user_id=instance, name=instance.username
					)
		elif instance.user_type == 'admin':
			qs = Admin.objects.filter(user=instance)
			if not qs.exists():
				Admin.objects.create(
						user=instance, name=instance.username
						)
		else:
			pass
