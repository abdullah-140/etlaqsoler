from django import forms
from .models import InstallationRequest

class RequestForm(forms.ModelForm):
    class Meta:
        model = InstallationRequest
        fields = ['address', 'required_power', 'installation_date']
        widgets = {
            'installation_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'required_power': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'address': 'العنوان الكامل',
            'required_power': 'القدرة المطلوبة (كيلوواط)',
            'installation_date': 'تاريخ التركيب المطلوب'
        }