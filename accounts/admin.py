from django.contrib import admin

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserCreationForm
from .models import MyUser, Admin, Client, Agency

# Register your models here.

class UserAdmin(BaseUserAdmin):
	add_form = UserCreationForm

	list_display = ('username', 'email', 'mobile_no', 'is_admin', 'user_type')
	list_filter = ('is_admin',)

	fieldsets = (
            (None, {'fields': ('username', 'full_name','email',
                                'mobile_no', 'user_type')}),
			('Permissions', {'fields': ('is_admin',)})
		)
	search_fields = ('username','email')
	ordering = ('username','email')

	filter_horizontal = ()


class AdminAdmin(admin.ModelAdmin):
	list_display = ['user', 'name', 'role', 'photo']

	class Meta:
		model = Admin




admin.site.register(MyUser, UserAdmin)
admin.site.register(Admin, AdminAdmin)
admin.site.register(Client)
admin.site.register(Agency)


admin.site.unregister(Group)
