from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from spsrs.models import user, student, faculty, feedback, MyAccountManager
from spsrs.forms import UserAuthenticationForm, FeedbackForm, StudentRegistrationForm, ViewForm, Update1Form, Update2Form, FbStudentForm
import datetime
from django.contrib.auth.hashers import check_password

# Create your views here.
def home_screen_view(request):
	context = {}
	if request.user.is_authenticated and request.user.is_admin:
		return redirect('faculty/')
	else:
		if request.user.is_authenticated: 
			return redirect('student/')
		else:	
			users = user.objects.all()
			students = student.objects.all()
			facultys = faculty.objects.all()
			context['users'] = users
			context['students'] = students
			context['facultys'] = facultys
			return render(request,'home.html',context)

def login_view(request):
	context = {}
	user = request.user
	if user.is_authenticated:
		return redirect('home')
	if request.POST:
		form = UserAuthenticationForm(request.POST)
		if form.is_valid():
			rollno = request.POST['rollno']
			password = request.POST['password']
			user = authenticate(rollno = rollno, password = password)
			if user:
				login(request, user)
				if user.previous_login != None:
					return redirect('student')
				else:
					return redirect('change_password')
	else:
		form = UserAuthenticationForm()

	context['login_form'] = form
	return render(request, 'login.html', context)

def logout_view(request):
	user.objects.filter(rollno = request.user).update(previous_login=request.user.last_login)
	logout(request)
	return redirect('home')

def registration_view(request):
	if request.user.is_authenticated and request.user.is_admin:
		date_today = datetime.datetime.now().strftime('%Y')+"-"+datetime.datetime.now().strftime('%m')+'-'+datetime.datetime.now().strftime('%d')
		try:
			fb = get_object_or_404(student ,rollno = request.POST['rollno'])
			context = {'user_already_registered':True, 'user_created': False}
			context['today_date'] = date_today
			student_form = StudentRegistrationForm()
			context['registration_form'] = student_form
			return render(request, 'faculty/register.html', context)
		except:
			if request.POST:
				student_form = StudentRegistrationForm(request.POST)
				if student_form.is_valid():
					student_form.save()
					user_db = MyAccountManager.create_user(user.objects,rollno = student_form.cleaned_data['rollno'], password='Password@123')
					student_form = StudentRegistrationForm()
					context = {'user_already_registered': False, 'user_created': True, 'registration_form': student_form}
					context['today_date'] = date_today
					return render(request, 'faculty/register.html', context)
			else:
				form = StudentRegistrationForm()
				context = {'user_already_registered': False, 'user_created': False}
				context['registration_form'] = form
				context['today_date'] = date_today
				return render(request, 'faculty/register.html', context)
	else:
		return redirect('home')



def student_view(request):
	context = {}
	if request.user.is_authenticated and not (request.user.is_admin):
		stud = student.objects.filter(rollno = request.user)
		context['student'] = stud
		return render(request, 'student/home.html', context)
	else:
		return redirect('home')

def feedback_view(request):
	context = {}
	if request.user.is_authenticated and not (request.user.is_admin):
		try:
			fb = get_object_or_404(feedback,rollno = request.user)
			context = {'fb_recorded':True, 'form_submitted': False}
			return render(request, 'student/feedback.html', context)
		except:
			pass
		if request.POST:
			form = FeedbackForm(request.POST)
			if form.is_valid():
				form.save()
				context = {'fb_recorded':False, 'form_submitted': True}
				return render(request,'student/feedback.html', context)


		else:
			context = {'fb_recorded':False, 'form_submitted': False}
			form = FeedbackForm()
			context['feedback'] = form
			return render(request,'student/feedback.html', context)

	else:
		return redirect('home')

def bmi_insights_view(request):
	context = {}
	if request.user.is_authenticated and request.user.is_admin:
		if request.GET:
			query = ViewForm(request.GET)
			section = False
			year = False
			bmi = None
			try:
				section = request.GET['section']
			except:
				pass
			try:
				year    = request.GET['year']
			except:
				pass
			objects = student.objects.filter(section = section, year = year)
			try:
				bmi= request.GET['bmi']
			except:
				pass
			if bmi == None:
				query = ViewForm()
				context['query'] = query
				return render(request,'faculty/bmi_insights.html', context)
			if (bmi == '1') and (section and year):
				above = 0
				below = 0
				middle = 0
				for obj in objects:
					if float(obj.bmi1) > 25:
						above+= 1
					else:
						if float(obj.bmi1) < 18:
							below+= 1
						else:
							middle+= 1
				context['query'] = query
				context['bmis'] = [above, middle, below]
				context['status'] = 1
				context['name'] = section.upper() + ' ' + year.upper() + ' year'
				return render(request,'faculty/bmi_insights.html', context)
			elif (bmi == "2") and (section and year):
				above = 0
				below = 0
				middle = 0
				for obj in objects:
					if float(obj.bmi2) > 25:
						above+= 1
					else:
						if float(obj.bmi2) < 18:
							below+= 1
						else:
							middle+= 1
				context['query'] = query
				context['bmis'] = [above, middle, below]
				context['status'] = 1
				context['name'] = section.upper() + ' ' + year.upper() + ' year'
				return render(request,'faculty/bmi_insights.html', context)
			else:
				query = ViewForm()
				context['query'] = query
				context['status'] = 0 
				return render(request,'faculty/bmi_insights.html', context)
		else:	
			query = ViewForm()
			context['query'] = query
			return render(request,'faculty/bmi_insights.html', context)
	else:
		return redirect('home')		

def faculty_view(request):
	context = {}
	if request.user.is_authenticated and request.user.is_admin:
		if request.GET:
			query = ViewForm(request.GET)
			section = request.GET['section']
			year    = request.GET['year']
			weight_one = False
			weight_two = False
			feedback = False
			try:
				weight_one = request.GET['weight_one']
			except:
				pass
			try:
				weight_two = request.GET['weight_two']
			except:
				pass
			try:
				feedback = request.GET['feedback']
			except:
				pass
			if feedback == "True":
				obj = student.objects.filter(section = section, year = year, feedback = 'empty feedback').order_by('rollno')
			else:
				obj = student.objects.filter(section = section, year = year).order_by('rollno')
			if weight_one == "True" and weight_two == "True":
				if feedback == 'True':
					obj = student.objects.filter(section = section, year = year, weight_one = 0.0, weight_two = 0.0, feedback = 'empty feedback').order_by('rollno')
				else:	
					obj = student.objects.filter(section = section, year = year, weight_one = 0.0, weight_two = 0.0).order_by('rollno')
			else:
				if weight_one == "True":
					if feedback == 'True':
						obj = student.objects.filter(section = section, year = year, weight_one = 0.0, feedback = 'empty feedback').order_by('rollno')
					else:

						obj = student.objects.filter(section = section, year = year, weight_one = 0.0).order_by('rollno')
				if weight_two == "True":
					if feedback == 'True':
						obj = student.objects.filter(section = section, year = year, weight_two = 0.0, feedback = 'empty feedback').order_by('rollno')
					else:
						obj = student.objects.filter(section = section, year = year, weight_two = 0.0).order_by('rollno')
			context['query'] = query
			context['obj'] = obj
			context['status'] = 1
			return render(request,'faculty/home.html', context)
		else:
			query = ViewForm()
			context['query'] = query
			context['status'] = 0
			return render(request,'faculty/home.html', context)
	else:
		return redirect('home')
def update1_view(request, rollno):
	context = {}
	rollno = rollno
	if request.user.is_authenticated and request.user.is_admin:
		if request.POST:
				std_form = Update1Form(request.POST)
				if std_form.is_valid():
					height_ones = request.POST['height_one']
					weight_ones = request.POST['weight_one']
					std = student.objects.filter(rollno = rollno).update(height_one = height_ones,weight_one = weight_ones )
					return redirect('home')
				else:			
				  	context['std_form'] = std_form
		else:
			std_form = Update1Form()
			context['std_form'] = std_form
			return render(request,'faculty/update1.html', context)
	else: 
		return redirect('home')

def update2_view(request, rollno):
	context = {}
	rollno = rollno
	if request.user.is_authenticated and request.user.is_admin:
		if request.POST:
				std_form = Update2Form(request.POST)
				
				if std_form.is_valid():
					height_twos = request.POST['height_two']
					weight_twos = request.POST['weight_two']
					std = student.objects.filter(rollno = rollno).update(height_two = height_twos,weight_two = weight_twos )
					
					return redirect('home')
				else:
					
				  	context['std_form'] = std_form


		else:
			std_form = Update2Form()
			context['std_form'] = std_form
			return render(request,'faculty/update2.html', context)
	else: 
		return redirect('home')

def fb_student_view(request, rollno):
	context = {}
	rollno = rollno
	if request.user.is_authenticated and request.user.is_admin:
		if request.POST:
				std_form = FbStudentForm(request.POST)
				
				if std_form.is_valid():
					fb_students = request.POST['feedback']
					std = student.objects.filter(rollno = rollno).update(feedback = fb_students)
					
					return redirect('home')
				else:
					
				  	context['std_form'] = std_form


		else:
			std_form = FbStudentForm()
			context['std_form'] = std_form
			return render(request,'faculty/fb_student.html', context)
	else: 
		return redirect('home')

def feedback_insights_view(request):
	if request.user.is_authenticated and request.user.is_admin:
		context = {}
		feedbacks = {}
		feedbacks_1st = [0,0,0,0,0]
		feedbacks_2nd = [0,0,0,0,0]
		feedbacks_3rd = [0,0,0,0,0]
		feedbacks_4th = [0,0,0,0,0]
		feedbacks_5th = [0,0,0,0,0]

		feedbacks_1st[0] = feedback.objects.filter(First = 1).count()
		feedbacks_1st[1] = feedback.objects.filter(First = 2).count()
		feedbacks_1st[2] = feedback.objects.filter(First = 3).count()
		feedbacks_1st[3] = feedback.objects.filter(First = 4).count()
		feedbacks_1st[4] = feedback.objects.filter(First = 5).count()

		feedbacks_2nd[0] = feedback.objects.filter(second = 1).count()
		feedbacks_2nd[1] = feedback.objects.filter(second = 2).count()
		feedbacks_2nd[2] = feedback.objects.filter(second = 3).count()
		feedbacks_2nd[3] = feedback.objects.filter(second = 4).count()
		feedbacks_2nd[4] = feedback.objects.filter(second = 5).count()

		feedbacks_3rd[0] = feedback.objects.filter(third = 1).count()
		feedbacks_3rd[1] = feedback.objects.filter(third = 2).count()
		feedbacks_3rd[2] = feedback.objects.filter(third = 3).count()
		feedbacks_3rd[3] = feedback.objects.filter(third = 4).count()
		feedbacks_3rd[4] = feedback.objects.filter(third = 5).count()

		feedbacks_4th[0] = feedback.objects.filter(fourth = 1).count()
		feedbacks_4th[1] = feedback.objects.filter(fourth = 2).count()
		feedbacks_4th[2] = feedback.objects.filter(fourth = 3).count()
		feedbacks_4th[3] = feedback.objects.filter(fourth = 4).count()
		feedbacks_4th[4] = feedback.objects.filter(fourth = 5).count()

		feedbacks_5th[0] = feedback.objects.filter(fifth = 1).count()
		feedbacks_5th[1] = feedback.objects.filter(fifth = 2).count()
		feedbacks_5th[2] = feedback.objects.filter(fifth = 3).count()
		feedbacks_5th[3] = feedback.objects.filter(fifth = 4).count()
		feedbacks_5th[4] = feedback.objects.filter(fifth = 5).count()

		# feedbacks['feedbacks_1st'] = feedbacks_1st
		# feedbacks['feedbacks_2nd'] = feedbacks_2nd
		# feedbacks['feedbacks_3rd'] = feedbacks_3rd
		# feedbacks['feedbacks_4th'] = feedbacks_4th
		# feedbacks['feedbacks_5th'] = feedbacks_5th
		if request.GET:
			try:
				category = request.GET['category']
			except:
				pass
			if category == '1':
				context['feedbacks'] = feedbacks_1st
				context['status'] = 1
				context['name'] = 'First'
				return render(request,'faculty/feedback_insights.html', context)
			if category == '2':
				context['feedbacks'] = feedbacks_2nd
				context['status'] = 1
				context['name'] = 'Second'
				return render(request,'faculty/feedback_insights.html', context)
			if category == '3':
				context['feedbacks'] = feedbacks_3rd
				context['status'] = 1
				context['name'] = 'Third'
				return render(request,'faculty/feedback_insights.html', context)
			if category == '4':
				context['feedbacks'] = feedbacks_4th
				context['status'] = 1
				context['name'] = 'Fourth'
				return render(request,'faculty/feedback_insights.html', context)
			if category == '5':
				context['feedbacks'] = feedbacks_5th
				context['status'] = 1
				context['name'] = 'Fifth'
				return render(request,'faculty/feedback_insights.html', context)
			else:
				context['status'] = 0
				return render(request,'faculty/feedback_insights.html', context)

		else:	
			context['feedbacks'] = feedbacks_1st
			return render(request,'faculty/feedback_insights.html', context)

def change_password_view(request):
	context = {}
	if request.user.is_authenticated:
		if request.POST:
			rollno = request.user
			fb = get_object_or_404(user, rollno = request.user)
			if check_password(request.POST['password'], request.user.password):
				context['status'] = 1
				fb.set_password(request.POST['new_password'])
				fb.save()
				user.objects.filter(rollno = request.user).update(previous_login=request.user.last_login)
				logout(request)
				return redirect('login')
			else:
				context['status'] = 0
				context['password_mismatch'] = 1
				return render(request, 'student/change_password.html', context)
		
		else:
			context['status'] = 0
			context['password_mismatch'] = 0
			return render(request, 'student/change_password.html', context)
	else: 
		return redirect('home')