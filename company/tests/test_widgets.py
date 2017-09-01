from bs4 import BeautifulSoup
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
              <input type="checkbox" name="field"
                value="1" id="id_field_0" class="form-field checkbox" />
              <label for="id_field_0">one</label>
          </li>
          <li>
              <input type="checkbox" name="field"
                value="2" id="id_field_1" class="form-field checkbox" />
              <label for="id_field_1">two</label>
          </li>
          <li>
              <input type="checkbox" name="field"
                value="3" id="id_field_2" class="form-field checkbox" />
              <label for="id_field_2">three</label>
          </li>
        </ul>
      </td>
    </tr>
    """

    soup_left = BeautifulSoup(minify_html(expected_html), 'html.parser')
    soup_right = BeautifulSoup(minify_html(str(form)), 'html.parser')
    assert soup_left == soup_right
