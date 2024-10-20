from django.urls import path
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

# Remove protected lock icons by overriding security at the endpoint level
token_obtain_pair_view = swagger_auto_schema(method="post", security=[])(TokenObtainPairView.as_view())
token_refresh_view = swagger_auto_schema(method="post", security=[])(TokenRefreshView.as_view())
signup_view = swagger_auto_schema(method="post", security=[])(views.SignupView.as_view())  # Add for signup

urlpatterns = [
    path("signup/", signup_view, name="signup"),  # Use unprotected signup
    path("login/", token_obtain_pair_view, name="token_obtain_pair"),
    path("refresh_token/", token_refresh_view, name="token_refresh"),
]
