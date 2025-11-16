from typing import Any

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Count, Sum
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, UpdateView

from designs.models import Design
from orders.models import Order

from .forms import (
    OwnerAtelierForm,
    OwnerLoginForm,
    OwnerProfileForm,
    OwnerRegistrationForm,
)
from .models import CustomUser
from .mixins import OwnerRequiredMixin


class OwnerRegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = OwnerRegistrationForm
    success_url = reverse_lazy("owner_dashboard")

    def form_valid(self, form):
        user: CustomUser = form.save(commit=False)
        user.role = CustomUser.ROLE_OWNER
        user.save()
        login(self.request, user)
        messages.success(self.request, "Profil muvaffaqiyatli yaratildi.")
        return super().form_valid(form)


class OwnerLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = OwnerLoginForm

    def form_valid(self, form):
        messages.success(self.request, "Qaytganingiz bilan tabriklaymiz!")
        return super().form_valid(form)


class OwnerLogoutView(LogoutView):
    next_page = reverse_lazy("landing")
    http_method_names = ["get", "post"]


class OwnerDashboardView(OwnerRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        owner = self.request.user
        designs = Design.objects.filter(owner=owner)
        orders = Order.objects.filter(design__owner=owner)
        context["total_designs"] = designs.count()
        context["total_orders"] = orders.count()
        context["recent_orders"] = orders.select_related("design")[:5]
        context["design_stats"] = designs.annotate(
            order_count=Count("orders"),
        )
        status_map = dict(Order.STATUS_CHOICES)
        status_data = orders.values("status").annotate(count=Count("id")).order_by()
        context["orders_by_status"] = [
            {"status": status_map.get(item["status"], item["status"]), "count": item["count"]}
            for item in status_data
        ]
        context["total_views"] = designs.aggregate(total=Sum("views_count"))[
            "total"
        ] or 0
        return context


class OwnerProfileUpdateView(OwnerRequiredMixin, UpdateView):
    template_name = "accounts/profile_form.html"
    form_class = OwnerProfileForm
    success_url = reverse_lazy("owner_profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Profil yangilandi.")
        return super().form_valid(form)


class OwnerAtelierUpdateView(OwnerRequiredMixin, UpdateView):
    template_name = "accounts/atelier_form.html"
    form_class = OwnerAtelierForm
    success_url = reverse_lazy("owner_atelier")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Atelye ma'lumotlari yangilandi.")
        return super().form_valid(form)
