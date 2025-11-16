from django.urls import path

from . import views

urlpatterns = [
    path("orders/", views.PublicOrderListView.as_view(), name="orders_public"),
    path("design/<int:pk>/order/", views.DesignOrderCreateView.as_view(), name="design_order"),
    path(
        "owner/dashboard/orders/",
        views.OwnerOrderListView.as_view(),
        name="owner_orders",
    ),
    path(
        "owner/dashboard/orders/<int:pk>/",
        views.OwnerOrderDetailView.as_view(),
        name="owner_order_detail",
    ),
]
