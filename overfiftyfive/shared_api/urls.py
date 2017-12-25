from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import serializers, viewsets, routers
from rest_framework.urlpatterns import format_suffix_patterns
from shared_api.views.login_view import LoginAPIView
from shared_api.views.logout_view import LogoutAPIView
from shared_api.views.send_reset_password_email_views import SendResetPasswordEmailAPIView
# from shared_api.views.register_user_view import RegisterUserAPIView
# from shared_api.views.register_university_view import RegisterUniversityAPIView


urlpatterns = [
    # # Authentication.
    url(r'^api/login$', LoginAPIView.as_view(), name='o55_login_api_endpoint'),
    url(r'^api/logout$', LogoutAPIView.as_view(), name='o55_logout_api_endpoint'),
    # url(r'^api/reset-password$', resetpassword_views.ResetPasswordAPIView.as_view(), name='o55_reset_password_api_endpoint'),
    url(r'^api/send-reset-password-email$', SendResetPasswordEmailAPIView.as_view(), name='o55_send_reset_password_email_api_endpoint'),
]


urlpatterns = format_suffix_patterns(urlpatterns)