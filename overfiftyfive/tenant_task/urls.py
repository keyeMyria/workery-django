from django.conf.urls import include, url
from django.urls import path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from tenant_task import views


urlpatterns = (
    # Active List
    path('pending-tasks/', views.PendingTaskListView.as_view(), name='o55_tenant_task_list'),
    path('closed-tasks/', views.ClosedTaskListView.as_view(), name='o55_tenant_closed_task_list'),

    # Retrieve
    path('pending-tasks/<int:pk>/', views.PendingTaskRetrieveView.as_view(), name='o55_tenant_pending_task_retrieve'),

    # Assign
    path('pending-tasks/<int:pk>/activity-sheet/', views.PendingTaskRetrieveForActivitySheetView.as_view(), name='o55_tenant_pending_task_retrieve_for_activity_sheet_retrieve'),
    path('pending-tasks/<int:pk>/activity-sheet/create', views.PendingTaskRetrieveForActivitySheetAndAssignAssociateCreateView.as_view(), name='o55_tenant_pending_task_retrieve_for_activity_sheet_retrieve_and_create'),

    # Close
    path('pending-tasks/<int:pk>/close/', views.PendingTaskRetrieveAndCloseCreateView.as_view(), name='o55_tenant_pending_task_retrieve_and_close_create'),

    # Postpone
    path('pending-tasks/<int:pk>/postpone/', views.PendingTaskRetrieveAndPostponeCreateView.as_view(), name='o55_tenant_pending_task_retrieve_and_postpone_create'),

    # Unassign
    path('pending-tasks/<int:pk>/unassign/', views.PendingTaskRetrieveAndUnassignCreateView.as_view(), name='o55_tenant_pending_task_retrieve_and_unassign_create'),

    # Complete
    path('pending-tasks/<int:pk>/complete/', views.PendingTaskRetrieveAndCompleteCreateView.as_view(), name='o55_tenant_pending_task_retrieve_and_complete_create'),

)
