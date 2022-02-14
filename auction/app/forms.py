from django import forms
from .models import Shoes



class MakeAnOffer(forms.Form):
	offer = forms.FloatField(label='offer($)', widget=forms.TextInput(attrs={'class': 'white-text'}))
	def clean(self):
		cleaned_data = super().clean()
		offer = self.cleaned_data.get('offer')
		if offer< 0:
			raise forms.ValidationError('')  # display messages.error instead

		return cleaned_data
