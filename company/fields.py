from django import forms


class SeoFriendlyChoiceField(forms.ChoiceField):
    def to_python(self, value):
        value = super().to_python(value)
        return value.replace('-', '_').upper()
