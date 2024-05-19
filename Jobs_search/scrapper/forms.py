from django import forms

class PositiveNumberOrAllField(forms.CharField):
    def to_python(self, value):
        if value.lower() == 'all':
            return value.lower()
        try:
            number = int(value)
            if number <= 0:
                raise forms.ValidationError("Please enter a positive number or 'all'.")
            return number
        except ValueError:
            raise forms.ValidationError("Please enter a valid number or 'all'.")

class ScrapForm(forms.Form):
    City = forms.CharField(label="City", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your City'}))
    Profession = forms.CharField(label="Profession", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Profession'}))
    Quantity = PositiveNumberOrAllField(label="Quantity", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your number'}),
                                        help_text="Enter a positive number or write 'all' to search for all possible options")