from django.db import models

from designs.models import Design


class Order(models.Model):
    STATUS_NEW = "new"
    STATUS_CONFIRMED = "confirmed"
    STATUS_SEWING = "sewing"
    STATUS_FINISHING = "finishing"
    STATUS_DONE = "done"

    STATUS_CHOICES = [
        (STATUS_NEW, "Yangi"),
        (STATUS_CONFIRMED, "Tasdiqlandi"),
        (STATUS_SEWING, "Tikish jarayonida"),
        (STATUS_FINISHING, "Yakunlanmoqda"),
        (STATUS_DONE, "Tayyor"),
    ]

    PROGRESS_MAP = {
        STATUS_NEW: 10,
        STATUS_CONFIRMED: 30,
        STATUS_SEWING: 60,
        STATUS_FINISHING: 85,
        STATUS_DONE: 100,
    }

    design = models.ForeignKey(
        Design,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    customer_name = models.CharField("Mijoz ismi", max_length=255)
    customer_phone = models.CharField("Telefon", max_length=30)
    size_chest = models.DecimalField("Ko'krak (sm)", max_digits=5, decimal_places=2)
    size_waist = models.DecimalField("Bel (sm)", max_digits=5, decimal_places=2)
    size_height = models.DecimalField("Bo'y (sm)", max_digits=5, decimal_places=2)
    fabric_type = models.CharField("Mato turi", max_length=120)
    notes = models.TextField("Qo'shimcha talablar", blank=True)
    due_days = models.PositiveIntegerField("Muddat (kun)", default=7)
    status = models.CharField(
        "Holat",
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"

    def __str__(self) -> str:
        return f"{self.customer_name} → {self.design.title}"

    @property
    def progress(self) -> int:
        return self.PROGRESS_MAP.get(self.status, 0)
