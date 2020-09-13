from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from django.utils.translation import ugettext as _
from centr_osvita.profiles.models import Profile, UserReport


@admin.register(UserReport)
class UserReportAdmin(admin.ModelAdmin):
    list_display = ('created',)


class DateEntranceFilter(admin.SimpleListFilter):
    title = _('Date entarence difference')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'created'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('0 - 0.5', _('from now to 0.5 year')),
            ('0.5 - 1', _('from 0.5 year to 1 Year')),
            ('1 - 1.5', _('from 1 year to 1.5 Year')),
            ('1.5 - 2', _('from 1.5 years to 2 Year')),
            ('>2', _('more than 2')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == '0 - 0.5':
            return queryset.filter(created__gte=timezone.now() - timedelta(days=6*30))
        if self.value() == '0.5 - 1':
            return queryset.filter(created__gte=timezone.now() - timedelta(days=12*30),
                                   created__lte=timezone.now() - timedelta(days=6*30))
        if self.value() == '1 - 1.5':
            return queryset.filter(created__gte=timezone.now() - timedelta(days=18*30),
                                   created__lte=timezone.now() - timedelta(days=12*30))
        if self.value() == '1.5 - 2':
            return queryset.filter(created__gte=timezone.now() - timedelta(days=24*30),
                                   created__lte=timezone.now() - timedelta(days=18*30))
        if self.value() == '>2':
            return queryset.filter(created__lte=timezone.now() - timedelta(days=24*30))


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'created', 'institution_type', 'institution_name', 'grade')
    search_fields = ('full_name',)
    list_filter = ('grade', 'institution_type', DateEntranceFilter)
    actions = ['form_report']

    def form_report(self, request, queryset):
        report = UserReport.objects.create()
        report.profiles = queryset
        report.save()
    form_report.short_description = "Form report"
