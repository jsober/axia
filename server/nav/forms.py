from django import forms

from vo.nav.models import IonStorm


class IonStormForm(forms.ModelForm):
    class Meta:
        model = IonStorm
