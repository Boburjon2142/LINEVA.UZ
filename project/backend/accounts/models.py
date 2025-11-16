from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_OWNER = "owner"
    ROLE_CHOICES = [
        (ROLE_OWNER, "Atelye egasi"),
    ]

    full_name = models.CharField("To'liq ism", max_length=255, blank=True)
    atelier_name = models.CharField("Atelye nomi", max_length=255, blank=True)
    atelier_address = models.CharField("Manzil", max_length=255, blank=True)
    phone = models.CharField("Telefon", max_length=30, blank=True)
    role = models.CharField(
        "Rol",
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_OWNER,
    )
    avatar = models.ImageField("Avatar", upload_to="avatars/", blank=True, null=True)

    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

    def __str__(self) -> str:
        return self.full_name or self.username

    @property
    def is_owner(self) -> bool:
        return self.role == self.ROLE_OWNER
