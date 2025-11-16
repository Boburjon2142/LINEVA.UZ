from django.contrib import messages
from django.db.models import Count, F
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from accounts.mixins import OwnerRequiredMixin
from orders.models import Order

from .forms import DesignForm
from .models import Design


class DesignListView(ListView):
    template_name = "designs/home.html"
    model = Design
    context_object_name = "designs"

    def get_queryset(self):
        return Design.objects.select_related("owner").annotate(
            order_count=Count("orders")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["orders"] = (
            Order.objects.select_related("design", "design__owner")
            .order_by("-created_at")[:6]
        )
        return context


class DesignDetailView(DetailView):
    template_name = "designs/detail.html"
    model = Design
    context_object_name = "design"

    def get_object(self, queryset=None):
        design = super().get_object(queryset)
        Design.objects.filter(pk=design.pk).update(views_count=F("views_count") + 1)
        design.refresh_from_db(fields=["views_count"])
        return design


class OwnerDesignListView(OwnerRequiredMixin, ListView):
    template_name = "designs/dashboard_list.html"
    model = Design
    context_object_name = "designs"

    def get_queryset(self):
        return Design.objects.filter(owner=self.request.user).annotate(
            order_count=Count("orders")
        )


class OwnerDesignCreateView(OwnerRequiredMixin, CreateView):
    template_name = "designs/dashboard_create.html"
    form_class = DesignForm
    success_url = reverse_lazy("owner_designs")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Yangi dizayn qo'shildi.")
        return super().form_valid(form)


class OwnerDesignUpdateView(OwnerRequiredMixin, UpdateView):
    template_name = "designs/dashboard_create.html"
    form_class = DesignForm
    model = Design
    success_url = reverse_lazy("owner_designs")

    def get_queryset(self):
        return Design.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Dizayn yangilandi.")
        return super().form_valid(form)


class OwnerDesignDeleteView(OwnerRequiredMixin, DeleteView):
    template_name = "designs/dashboard_delete.html"
    model = Design
    success_url = reverse_lazy("owner_designs")

    def get_queryset(self):
        return Design.objects.filter(owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Dizayn o'chirildi.")
        return super().delete(request, *args, **kwargs)
