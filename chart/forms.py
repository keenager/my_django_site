from django import forms
from .models import HayulGrowth


class HayulGrowthForm(forms.ModelForm):

    class Meta:
        model = HayulGrowth
        fields = ("year_month", "height", "weight")
        labels = {
            "year_month": "연월",
            "height": "키",
            "weight": "몸무게",
        }
