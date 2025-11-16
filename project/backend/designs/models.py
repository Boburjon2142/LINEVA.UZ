from decimal import Decimal

from django.conf import settings
from django.db import models
from django.urls import reverse


class Design(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="designs",
    )
    title = models.CharField("Nomi", max_length=255)
    description = models.TextField("Tavsif")
    image = models.ImageField("Rasm", upload_to="designs/")
    price = models.DecimalField(
        "Narx (so'm)",
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Dizayn"
        verbose_name_plural = "Dizaynlar"

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("design_detail", args=[self.pk])
