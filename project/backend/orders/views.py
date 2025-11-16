from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from accounts.mixins import OwnerRequiredMixin
from designs.models import Design

from .forms import OrderCreateForm, OrderStatusForm
from .models import Order


class DesignOrderCreateView(CreateView):
    model = Order
    template_name = "orders/order_form.html"
    form_class = OrderCreateForm

    def dispatch(self, request, *args, **kwargs):
        self.design = get_object_or_404(Design, pk=self.kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.design = self.design
        messages.success(self.request, "Buyurtmangiz qabul qilindi!")
        return super().form_valid(form)

    def get_success_url(self):
        return self.design.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["design"] = self.design
        return context


class OwnerOrderListView(OwnerRequiredMixin, ListView):
    template_name = "orders/dashboard_list.html"
    model = Order
    context_object_name = "orders"

    def get_queryset(self):
        qs = (
            Order.objects.filter(design__owner=self.request.user)
            .select_related("design")
            .order_by("-created_at")
        )
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["statuses"] = Order.STATUS_CHOICES
        context["active_status"] = self.request.GET.get("status", "")
        return context


class OwnerOrderDetailView(OwnerRequiredMixin, UpdateView):
    template_name = "orders/dashboard_detail.html"
    model = Order
    form_class = OrderStatusForm
    success_url = reverse_lazy("owner_orders")
    context_object_name = "order"

    def get_queryset(self):
        return Order.objects.filter(design__owner=self.request.user).select_related(
            "design", "design__owner"
        )

    def form_valid(self, form):
        messages.success(self.request, "Buyurtma holati yangilandi.")
        return super().form_valid(form)


class PublicOrderListView(ListView):
    template_name = "orders/public_list.html"
    model = Order
    context_object_name = "orders"
    paginate_by = 12

    def get_queryset(self):
        return (
            Order.objects.select_related("design", "design__owner")
            .order_by("-created_at")
        )
