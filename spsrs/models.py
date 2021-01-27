from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import date
# Create your models here.


class MyAccountManager(BaseUserManager):
	def create_user(self, rollno, password = None):
		if not rollno:
			raise ValueError('user must have rollno')


		user = self.model(
				rollno = rollno,
			)
		user.set_password(password)
		user.save(using = self._db)
		return user

	def create_superuser(self, rollno, password):
		user = self.create_user(
				rollno = rollno,
			)	
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using = self._db)
		return user


class user(AbstractBaseUser):
	rollno					= models.CharField(max_length = 12, unique = True)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', null = True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)
	previous_login 			= models.DateTimeField(verbose_name='Previous Login', null = True)


	USERNAME_FIELD = 'rollno'
	REQUIRED_FIELDS = []

	objects = MyAccountManager()

	def __str__(self):
		return self.rollno

	def has_perm(self, perm, obj = None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True
	
	def is_staff(self):
		return self.is_staff

section = [
			#CSE
			('C1','CSE-1'),
			('C2','CSE-2'),
			('C3','CSE-3'),
			#ECE
			('E1','ECE-1'),
			('E2','ECE-2'),
			('E3','ECE-3'),
			#EEE
			('J1','EEE-1'),
			('J2','EEE-2'),
			#IT
			('I3','IT-3'),
			('I1','IT-1'),
			('I2','IT-2'),
			#MECH
			('A1','MECH-1'),
			('A2','MECH-2'),
			#CIVIL
			('D1','CIVIL-1'),
			('D2','CIVIL-2'),
			#PROD
			('P','PROD'),
			#CHEM
			('K','CHEM'),
			#BIO
			('B','BIOTECH'),
			#MBA
			('L','MBA'),
			#MTECH
			('M','MTECH'),
			#MCA
			('N','MCA'),
]

year = [
		('1st','first year'),
		('2nd','second year'),
		('3rd','third year'),
		('4th','fourth year'),
]

feedback = [
			(1,'Poor'),
			(2,'Satisfactory'),
			(3,'Good'),
			(4,'Very Good'),
			(5,'Awesome'),
]
class student(models.Model):
	rollno					= models.CharField(max_length = 12, unique = True)
	name 					= models.CharField(max_length = 100)
	dob						= models.DateField(max_length = 8)
	section					= models.CharField(max_length = 2, choices = section)
	year 					= models.CharField(max_length = 3, choices = year)
	#age 					= models.IntegerField()
	height_one				= models.FloatField(default = 1.0)
	weight_one				= models.FloatField(default = 0.0)
	height_two				= models.FloatField(default = 1.0)
	weight_two				= models.FloatField(default = 0.0)
	#bmi_one					= models.FloatField()
	#bmi_two					= models.FloatField()
	feedback 				= models.CharField(max_length = 500, default = 'empty feedback')
	fb_recorded 			= models.BooleanField(default = False)			

	@property	
	def age(self):
		today = date.today()
		age = today.year - self.dob.year
		if today.month < self.dob.month or today.month == self.dob.month and today.day < self.dob.day:
			age -= 1
		return age

	@property
	def bmi1(self):
		return float('{:.2f}'.format((self.weight_one)/((self.height_one)**2)))

	@property
	def bmi2(self):
		return float("{:.2f}".format((self.weight_two)/((self.height_two)**2)))
	
	def __str__(self):
		return str(self.rollno) + ', ' + str(self.name)

class faculty(models.Model):
	rollno					= models.ForeignKey(user, on_delete=models.CASCADE)
	name 					= models.CharField(max_length = 100)
	def __str__(self):
		return str(self.rollno) + ', ' + str(self.name)

class feedback(models.Model):
	rollno					= models.CharField(max_length = 12, unique = True)
	First 					= models.IntegerField(choices = feedback, blank=True, null =True)
	second 					= models.IntegerField(choices = feedback, blank=True, null =True)
	third 					= models.IntegerField(choices = feedback, blank=True, null =True)
	fourth 					= models.IntegerField(choices = feedback, blank=True, null =True)
	fifth 					= models.IntegerField(choices = feedback, blank=True, null =True)
	suggestion 				= models.CharField(max_length = 500, default = '', blank=True, null =True)

	def __str__(self):
		return str(self.rollno)