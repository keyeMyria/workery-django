from django.conf.urls import include, url
from django.urls import path
from django.views.generic.base import RedirectView
from tenant_team.views import create_view, list_view, retrieve_view, search_view, update_view


urlpatterns = (
    # Summary
    path('staff/', list_view.TeamSummaryView.as_view(), name='workery_tenant_team_summary'),

    # Create
    path('staff/confirm-creation/', create_view.TeamCreateConfirmView.as_view(), name='workery_tenant_team_confirm_create'),
    path('staff/create/', create_view.TeamCreateView.as_view(), name='workery_tenant_team_create'),

    # List
    path('staff/list/', list_view.TeamListView.as_view(), name='workery_tenant_team_list'),

    # Search
    path('staff/search/', search_view.TeamSearchView.as_view(), name='workery_tenant_team_search'),
    path('staff/search/results/', search_view.TeamSearchResultView.as_view(), name='workery_tenant_team_search_results'),

    # Retrieve
    path('staff/<str:template>/detail/<int:pk>/lite/', retrieve_view.StaffLiteRetrieveView.as_view(), name='workery_tenant_team_lite_retrieve'),
    path('staff/<str:template>/detail/<int:pk>/full/', retrieve_view.StaffFullRetrieveView.as_view(), name='workery_tenant_team_full_retrieve'),
    path('staff/<str:template>/detail/<int:pk>/comments/', retrieve_view.StaffRetrieveForCommentsListAndCreateView.as_view(), name='workery_tenant_team_retrieve_for_comment_list_and_create'),
    path('staff/<str:template>/detail/<int:pk>/redirect-from-user-id-to-staff-id/', retrieve_view.staff_redirect_from_user_id_to_staff_id, name='workery_tenant_team_retrieve_from_user_id_redirect'),

    # Update
    path('staff/<str:template>/detail/<int:pk>/edit/', update_view.TeamUpdateView.as_view(), name='workery_tenant_team_update'),
)
