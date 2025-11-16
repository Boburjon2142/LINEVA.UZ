from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="fabric_type",
            field=models.CharField(default="Mato", max_length=120, verbose_name="Mato turi"),
            preserve_default=False,
        ),
    ]
