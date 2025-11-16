from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class OwnerRequiredMixin(LoginRequiredMixin):
    """Owner roliga ega foydalanuvchilar uchun mixin."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not getattr(request.user, "is_owner", False):
            messages.error(request, "Bu bo'lim faqat atelye egalari uchun.")
            return redirect("landing")
        return super().dispatch(request, *args, **kwargs)
