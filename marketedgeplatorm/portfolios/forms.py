from django.forms import ModelForm
from django import forms
from .models import Portfolio

class PortfolioForm(ModelForm):
    class Meta:
        model = Portfolio
        fields = ['name', 'description', 'portfolio_type', 'tags']

        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(PortfolioForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})