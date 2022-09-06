"""from django.urls import path
from api.views import user_views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    # overview api
    path('', user_views.api_user_overview,
         name='api_user_overview'),

    # auth
    path('token/', user_views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),

    # registration
    path('registration/', user_views.RegisterView.as_view(),
         name='registration'),
    path('registration/email-verify/', user_views.EmailVerify.as_view(),
         name='email-verify'),

    # password reset without auth
    path('request-reset-password/',
         user_views.RequestEmailResetPassword.as_view(),
         name='request-reset-password'),
    path('password-reset/<uidb64>/<token>/',
         user_views.PasswordTokenCheckAPI.as_view(),
         name='password-reset-confirm'),
    path('password_reset_complete/',
         user_views.SetNewPasswordApi.as_view(),
         name='password_reset_complete'),

    # update user profile
    path('profile/update/', user_views.update_user_profile, name="user-profile-update"),

]
"""