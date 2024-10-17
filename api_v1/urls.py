from django.urls import include, path

urlpatterns = [
    path("auth/", include("auth_api.urls")),
    path("scheduler/", include("scheduler.urls")),
]
