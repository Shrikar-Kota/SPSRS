"""system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from spsrs.views import home_screen_view, login_view, logout_view, registration_view, student_view, feedback_view, faculty_view, update1_view, update2_view, fb_student_view, feedback_insights_view,bmi_insights_view,change_password_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_screen_view, name = 'home'),
    path('login/',login_view, name = 'login'),
    path('logout/',logout_view, name = 'logout'),
    path('faculty/register/',registration_view, name = 'register'),
    path('student/',student_view, name = 'student'),
    path('student/feedback/',feedback_view, name = 'feedback'),
    path('student/password_change/',change_password_view, name = 'change_password'),
    path('faculty/',faculty_view, name = 'faculty'),

    path('faculty/update1/<rollno>', update1_view, name = 'update1'),
    path('faculty/update2/<rollno>', update2_view, name = 'update2'),
    path('faculty/fb_student/<rollno>', fb_student_view, name = 'fb_student'),
    path('faculty/feedback_insights', feedback_insights_view, name = 'feedback_insights'),
    path('faculty/bmi_insights', bmi_insights_view, name = 'bmi_insights'),
]
