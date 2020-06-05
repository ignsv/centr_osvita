from django.contrib.auth.mixins import AccessMixin


class IsStaffRequiredMixin(AccessMixin):
    """
    CBV mixin which verifies that the current user is staff.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super(IsStaffRequiredMixin, self).dispatch(request, *args, **kwargs)
