from django import forms

class contactForm(forms.Form):
	name = forms.CharField(label='', required=False, max_length=100, help_text='100 characters max.', widget= forms.TextInput
                           (attrs={'placeholder':'Name', 'class':'form-control',
				   }))
	email = forms.EmailField(label='', required=True, widget= forms.EmailInput
                           (attrs={'placeholder':'Email', 'class':'form-control',
				   }))
	comment = forms.CharField(label='', required=True, widget= forms.Textarea
                           (attrs={'placeholder':'Comment', 'class':'form-control',
				   }))