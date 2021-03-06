from django.conf import settings
from django.core.paginator import EmptyPage, Paginator
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.functional import cached_property
from django.views.generic import RedirectView, TemplateView
from django.views.generic.edit import FormView

from api_client import api_client
from company import forms, helpers


class SubmitFormOnGetMixin:

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        data = self.request.GET or {}
        if data:
            kwargs['data'] = data
        return kwargs

    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CompanySearchView(SubmitFormOnGetMixin, FormView):
    template_name = 'company-search-results-list.html'
    form_class = forms.CompanySearchForm
    page_size = 10

    def dispatch(self, *args, **kwargs):
        if not settings.FEATURE_COMPANY_SEARCH_VIEW_ENABLED:
            raise Http404()
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            active_view_name='public-company-profiles-list',
            **kwargs,
        )

    def form_valid(self, form):
        results, count = self.get_results_and_count(form)
        try:
            paginator = Paginator(range(count), self.page_size)
            pagination = paginator.page(form.cleaned_data['page'])
        except EmptyPage:
            return self.handle_empty_page(form)
        else:
            context = self.get_context_data(
                results=results,
                pagination=pagination,
                form=form,
            )
            return TemplateResponse(self.request, self.template_name, context)

    def get_results_and_count(self, form):
        response = api_client.company.search(
            term=form.cleaned_data['term'],
            page=form.cleaned_data['page'],
            sectors=form.cleaned_data['sectors'],
            size=self.page_size,
        )
        response.raise_for_status()
        formatted = helpers.get_results_from_search_response(response)
        return formatted['results'], formatted['hits']['total']

    @staticmethod
    def handle_empty_page(form):
        url = '{url}?term={term}'.format(
            url=reverse('company-search'),
            term=form.cleaned_data['term']
        )
        return redirect(url)


class PublishedProfileListView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        sectors = self.request.GET.get('sectors')
        if sectors:
            return '{url}?sector={sector}'.format(
                url=reverse('company-search'), sector=sectors
            )
        return reverse('company-search')


class PublishedProfileDetailView(TemplateView):
    template_name = 'company-profile-detail.html'

    @cached_property
    def company(self):
        return helpers.get_company_profile(self.kwargs['company_number'])

    def get_canonical_url(self):
        kwargs = {
            'company_number': self.company['number'],
            'slug': self.company['slug'],
        }
        return reverse('public-company-profiles-detail', kwargs=kwargs)

    def get(self, *args, **kwargs):
        if self.kwargs.get('slug') != self.company['slug']:
            return redirect(to=self.get_canonical_url(), permanent=True)
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        social = {
            'title': (
                'International trade profile: {0}'.format(self.company['name'])
            ),
            'description': self.company['summary'],
            'image': self.company['logo'],
        }
        return super().get_context_data(
            show_description='verbose' in self.request.GET,
            company=self.company,
            social=social,
            **kwargs
        )


class CaseStudyDetailView(TemplateView):
    template_name = 'supplier-case-study-detail.html'

    @cached_property
    def case_study(self):
        return helpers.get_case_study(self.kwargs['id'])

    def get_canonical_url(self):
        kwargs = {
            'id': self.case_study['pk'],
            'slug': self.case_study['slug'],
        }
        return reverse('case-study-details', kwargs=kwargs)

    def get(self, *args, **kwargs):
        if self.kwargs.get('slug') != self.case_study['slug']:
            return redirect(to=self.get_canonical_url(), permanent=True)
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        social = {
            'title': 'Project: {title}'.format(title=self.case_study['title']),
            'description': self.case_study['description'],
            'image': self.case_study['image_one'],
        }
        return super().get_context_data(
            case_study=self.case_study,
            social=social,
            **kwargs
        )


class ContactCompanyView(FormView):
    template_name = 'company-contact-form.html'
    success_template_name = 'company-contact-success.html'
    failure_template_name = 'company-contact-error.html'
    form_class = forms.ContactCompanyForm

    def form_valid(self, form):
        data = self.serialize_form_data(
            cleaned_data=form.cleaned_data,
            company_number=self.kwargs['company_number'],
        )
        response = api_client.company.send_email(data)
        if response.ok:
            template = self.success_template_name
        else:
            template = self.failure_template_name
        context = self.get_context_data()
        return TemplateResponse(self.request, template, context)

    @staticmethod
    def serialize_form_data(cleaned_data, company_number):
        return forms.serialize_contact_company_form(
            cleaned_data,
            company_number,
        )

    def get_context_data(self, **kwargs):
        company = helpers.get_company_profile(self.kwargs['company_number'])
        return super().get_context_data(company=company, **kwargs)
