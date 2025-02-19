from django import forms
from product_app.models import Maxsulot, Kategoriya
from django.utils.translation import gettext as _

class ProductForm(forms.ModelForm):
    kategoriya = forms.ModelChoiceField(
        queryset=Kategoriya.objects.all(),
        empty_label=_("Kategoriya tanlang"),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    class Meta:
        model = Maxsulot
        fields = ['kategoriya', "nomi", "rasm", "razmer", "count"]
