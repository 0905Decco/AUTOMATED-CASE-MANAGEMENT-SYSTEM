from django import forms
from .models import Case, Litigant  # Import the necessary models

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['case_number', 'litigants', 'status', 'details']  # Fields to include in the form

    def __init__(self, *args, **kwargs):
        super(CaseForm, self).__init__(*args, **kwargs)
        self.fields['litigants'].queryset = Litigant.objects.all()  # Adjust queryset for litigants if necessary
