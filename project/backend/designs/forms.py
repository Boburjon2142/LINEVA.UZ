from django import forms

from .models import Design


class DesignForm(forms.ModelForm):
    class Meta:
        model = Design
        fields = ["title", "description", "price", "image"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{css} form-control".strip()
