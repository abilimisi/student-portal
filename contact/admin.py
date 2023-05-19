from django.contrib import admin
from contact.models import Cancer

# Register your models here.

class CancerAdmin(admin.ModelAdmin):
    list_disp=('username','gender','calender','dateofbirth','dateoftime','email','pass1','pass2')

admin.site.register(Cancer, CancerAdmin)


