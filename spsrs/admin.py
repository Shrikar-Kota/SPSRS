from django.contrib import admin
from spsrs.models import user, student, faculty, feedback

# Register your models here.
class UserAdmin(admin.ModelAdmin):
	list_display = ('rollno', 'date_joined', 'last_login')
	search_fields = ('rollno',)
	readonly_fields = ('date_joined', 'last_login')
	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

admin.site.register(user, UserAdmin)
admin.site.register(student)
admin.site.register(faculty)
admin.site.register(feedback)