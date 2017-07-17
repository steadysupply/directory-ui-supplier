from django import forms


class SeoFriendlyChoiceField(forms.ChoiceField):
    """
    The field value is exposed in the URL when then form is submitted.
    `sector=FOOD_AND_DRINK`, for example, would not look great visually, and
    there are SEO implications. Functionality added to this field allows the
    url to show `food-and-drink`, and it will be converted to `FOOD_AND_DRINK`

    """

    def to_python(self, value):
        value = super().to_python(value)
        return value.replace('-', '_').upper()
