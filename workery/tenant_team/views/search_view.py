# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from shared_foundation.mixins import (
    ExtraRequestProcessingMixin,
    WorkeryTemplateView,
    WorkeryListView,
    WorkeryDetailView
)
from tenant_api.filters.staff import StaffFilter
from tenant_foundation.models import Staff


#--------#
# SEARCH #
#--------#


class TeamSearchView(LoginRequiredMixin, WorkeryTemplateView):
    template_name = 'tenant_team/search/search_view.html'
    menu_id = "team"


class TeamSearchResultView(LoginRequiredMixin, WorkeryListView):
    context_object_name = 'staff_list'
    queryset = Staff.objects.order_by('-created')
    template_name = 'tenant_team/search/result_view.html'
    paginate_by = 100
    menu_id = "team"
    skip_parameters_array = ['page']

    def get_queryset(self):
        """
        Override the default queryset to allow dynamic filtering with
        GET parameterss using the 'django-filter' library.
        """
        queryset = None  # The queryset we will be returning.
        keyword = self.request.GET.get('keyword', None)
        if keyword:
            queryset = Staff.objects.full_text_search(keyword)
        else:
            queryset = super(TeamListView, self).get_queryset()
        queryset = queryset.order_by('last_name', 'given_name')

        # The following code will use the 'django-filter'
        filter = StaffFilter(self.request.GET, queryset=queryset)
        queryset = filter.qs
        queryset = queryset.prefetch_related(
            'owner',
        )
        return queryset
