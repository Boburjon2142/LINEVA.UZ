from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser


class StyledFormMixin:
    def _apply_styles(self):
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                continue
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{css} form-control".strip()


class OwnerRegistrationForm(StyledFormMixin, UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "full_name",
            "atelier_name",
            "atelier_address",
            "phone",
            "password1",
            "password2",
        ]
        widgets = {
            "atelier_address": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_styles()


class OwnerLoginForm(StyledFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_styles()

    def confirm_login_allowed(self, user):
        if not user.is_active or not getattr(user, "is_owner", False):
            raise forms.ValidationError(
                "Faqat atelye egalari tizimga kira oladi.", code="inactive"
            )


class OwnerProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["full_name", "email", "phone", "avatar"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_styles()


class OwnerAtelierForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["atelier_name", "atelier_address"]
        widgets = {
            "atelier_address": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_styles()
