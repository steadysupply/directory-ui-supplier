from django.forms import widgets
from django.utils.html import format_html


class PreventRenderWidget(widgets.Input):

    attrs = {}

    def render(self, name, value, attrs=None):
        return format_html('<!- not rendered ->')

    def value_from_datadict(self, data, files, name):
        return data.get(name, None)


class CheckboxSelectInlineLabelMultiple(widgets.CheckboxSelectMultiple):
    option_template_name = 'widgets/checkbox_input_option.html'

    def __init__(self, attrs=None, *args, **kwargs):
        super().__init__(attrs=attrs, *args, **kwargs)
        self.attrs['class'] = self.attrs.get('class', 'form-field checkbox')
