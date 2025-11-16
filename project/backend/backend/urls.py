from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("designs.urls")),
    path("", include("accounts.urls")),
    path("", include("orders.urls")),
    path("faq/", TemplateView.as_view(template_name="pages/faq.html"), name="faq"),
    path("guide/", TemplateView.as_view(template_name="pages/guide.html"), name="guide"),
    path("contact/", TemplateView.as_view(template_name="pages/contact.html"), name="contact"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
