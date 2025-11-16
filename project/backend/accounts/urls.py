from django.urls import path

from . import views

urlpatterns = [
    path("owner/login/", views.OwnerLoginView.as_view(), name="owner_login"),
    path("owner/logout/", views.OwnerLogoutView.as_view(), name="owner_logout"),
    path("owner/register/", views.OwnerRegisterView.as_view(), name="owner_register"),
    path("owner/dashboard/", views.OwnerDashboardView.as_view(), name="owner_dashboard"),
    path(
        "owner/dashboard/profile/",
        views.OwnerProfileUpdateView.as_view(),
        name="owner_profile",
    ),
    path(
        "owner/dashboard/atelier/",
        views.OwnerAtelierUpdateView.as_view(),
        name="owner_atelier",
    ),
]
