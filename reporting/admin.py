from django.contrib import admin
from .models import ReportItem, Report
# Register your models here.
class ReportAdmin(admin.ModelAdmin):
    pass
class ReportItemAdmin(admin.ModelAdmin):
    pass
admin.site.register(Report, ReportAdmin)
admin.site.register(ReportItem, ReportItemAdmin)