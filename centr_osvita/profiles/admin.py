from django.contrib import admin
from centr_osvita.profiles.models import Profile, UserReport


@admin.register(UserReport)
class UserReportAdmin(admin.ModelAdmin):
    list_display = ('created',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'created', 'institution_type', 'institution_name', 'grade')
    actions = ['form_report']

    def form_report(self, request, queryset):
        report = UserReport.objects.create()
        report.profiles = queryset
        report.save()
    form_report.short_description = "Form report"
