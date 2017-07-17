from django import forms


class SeoFriendlyChoiceField(forms.ChoiceField):

    @staticmethod
    def to_human_friendly(value):
        return value.replace('_', '-').lower()

    @staticmethod
    def to_machine_friendly(value):
        return value.replace('-', '_').upper()

    def __init__(self, *, choices=(), **kwargs):
        choices = [
            (label, self.to_human_friendly(value)) for label, value, in choices
        ]
        super().__init__(choices=choices, **kwargs)

    def to_python(self, value):
        value = super().to_python(value)
        return self.to_machine_friendly(value)
