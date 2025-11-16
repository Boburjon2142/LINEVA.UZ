from django.urls import path

from . import views

urlpatterns = [
    path("", views.DesignListView.as_view(), name="landing"),
    path("design/<int:pk>/", views.DesignDetailView.as_view(), name="design_detail"),
    path(
        "owner/dashboard/designs/",
        views.OwnerDesignListView.as_view(),
        name="owner_designs",
    ),
    path(
        "owner/dashboard/designs/create/",
        views.OwnerDesignCreateView.as_view(),
        name="owner_design_create",
    ),
    path(
        "owner/dashboard/designs/<int:pk>/edit/",
        views.OwnerDesignUpdateView.as_view(),
        name="owner_design_edit",
    ),
    path(
        "owner/dashboard/designs/<int:pk>/delete/",
        views.OwnerDesignDeleteView.as_view(),
        name="owner_design_delete",
    ),
]
