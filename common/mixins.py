from django.shortcuts import redirect
from django.contrib import messages

class CustomLoginRequiredMixin:
    login_url = 'common:login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please login first")
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)
