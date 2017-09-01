import difflib

from django import forms
from company import widgets


def minify_html(html):
    return html.replace('  ', '').replace('\n', '')


def test_mutiple_choice_checkbox_with_inline_label():

    class MyTestForm(forms.Form):
        field = forms.BooleanField(
            widget=widgets.CheckboxSelectInlineLabelMultiple(
                choices=[
                    ('1', 'one'),
                    ('2', 'two'),
                    ('3', 'three'),
                ]
            )
        )

    form = MyTestForm()

    expected_html = """
    <tr>
      <th>
        <label>Field:</label>
      </th>
      <td>
        <ul id="id_field" class="form-field checkbox">
          <li>
              <input type="checkbox" name="field" value="1" id="id_field_0" class="form-field checkbox" />
              <label for="id_field_0">one</label>
          </li>
          <li>
              <input type="checkbox" name="field" value="2" id="id_field_1" class="form-field checkbox" />
              <label for="id_field_1">two</label>
          </li>
          <li>
              <input type="checkbox" name="field" value="3" id="id_field_2" class="form-field checkbox" />
              <label for="id_field_2">three</label>
          </li>
        </ul>
      </td>
    </tr>
    """

    comparitor = difflib.SequenceMatcher(
        a=minify_html(expected_html),
        b=minify_html(str(form))
    )

    # since order of HTML attributes is not guarantees,
    # we accept a weaker test
    assert comparitor.ratio() >= 0.8349705304518664
