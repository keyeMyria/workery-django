from django.conf.urls import include, url
from django.urls import path
from django.views.generic.base import RedirectView
from tenant_ongoing_order import views

urlpatterns = (
    # List
    path('ongoing-jobs/list/', views.RunningOrInactiveOngoingJobListView.as_view(), name='workery_tenant_ongoing_job_list'),
    path('ongoing-jobs/list/terminated', views.TerminatedOngoingJobListView.as_view(), name='workery_tenant_ongoing_job_terminated_list'),

    # Retrieve
    path('ongoing-jobs/<str:template>/detail/<int:pk>/lite/', views.OngoingJobLiteRetrieveView.as_view(), name='workery_tenant_ongoing_job_lite_retrieve'),
    path('ongoing-jobs/<str:template>/detail/<int:pk>/full/', views.OngoingJobFullRetrieveView.as_view(), name='workery_tenant_ongoing_job_full_retrieve'),
    path('ongoing-jobs/<str:template>/detail/<int:pk>/comments/', views.OngoingJobRetrieveForCommentsListAndCreateView.as_view(), name='workery_tenant_ongoing_job_retrieve_for_comments'),

    # Update
    path('ongoing-jobs/<str:template>/detail/<int:pk>/edit/', views.OngoingJobUpdateView.as_view(), name='workery_tenant_ongoing_job_update'),
)
