from django.core.urlresolvers import reverse

from ui import context_processors
from enrolment.forms import AnonymousSubscribeForm, LeadGenerationForm


def test_feature_flags_installed(settings):
    processors = settings.TEMPLATES[0]['OPTIONS']['context_processors']

    assert 'ui.context_processors.feature_flags' in processors


def test_feature_returns_expected_features(rf, settings):

    settings.FEATURE_MORE_INDUSTRIES_BUTTON_ENABLED = True
    settings.FEATURE_COMPANY_SEARCH_VIEW_ENABLED = False
    request = rf.get('/')
    actual = context_processors.feature_flags(request)

    assert actual == {
        'features': {
            'FEATURE_MORE_INDUSTRIES_BUTTON_ENABLED': True,
            'FEATURE_COMPANY_SEARCH_VIEW_ENABLED': False,
        },
    }


def test_subscribe_form_installed(settings):
    processors = settings.TEMPLATES[0]['OPTIONS']['context_processors']

    assert 'ui.context_processors.subscribe_form' in processors


def test_subscribe_form_exposes_form_details(rf):
    request = rf.get(reverse('index'))

    actual = context_processors.subscribe_form(request)

    assert isinstance(actual['subscribe']['form'], AnonymousSubscribeForm)


def test_analytics(rf, settings):
    settings.GOOGLE_TAG_MANAGER_ID = '123'
    settings.GOOGLE_TAG_MANAGER_ENV = '&thing=1'
    settings.UTM_COOKIE_DOMAIN = '.thing.com'

    actual = context_processors.analytics(None)

    assert actual == {
        'analytics': {
            'GOOGLE_TAG_MANAGER_ID': '123',
            'GOOGLE_TAG_MANAGER_ENV': '&thing=1',
            'UTM_COOKIE_DOMAIN': '.thing.com',
        }
    }


def test_analytics_installed(settings):
    processors = settings.TEMPLATES[0]['OPTIONS']['context_processors']

    assert 'ui.context_processors.analytics' in processors


def test_lead_generation_form_installed(settings):
    processors = settings.TEMPLATES[0]['OPTIONS']['context_processors']

    assert 'ui.context_processors.lead_generation_form' in processors


def test_lead_generation_form_exposes_form_details(rf):
    request = rf.get(reverse('index'))

    actual = context_processors.lead_generation_form(request)

    assert isinstance(actual['lead_generation']['form'], LeadGenerationForm)
