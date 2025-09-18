from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.views import TokenRefreshView

from django.urls import path

from . import views


schema_view = get_schema_view(
    info=openapi.Info(title="Notes API", default_version="v1"),
    public=True,
    permission_classes=(permissions.AllowAny,)
)


urlpatterns = [
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema_swagger"),

    path("api/notes/", views.NoteListView.as_view(), name="notes"),
    path("api/notes/<int:pk>/", views.NoteDetailView.as_view(), name="note"),
    path("api/notes/create/", views.NoteCreateView.as_view(), name="note_create"),
    path("api/notes/update/<int:pk>/", views.NoteUpdateView.as_view(), name="note_update"),
    path("api/notes/delete/<int:pk>/", views.NoteDeleteView.as_view(), name="note_delete"),


    path("api/user/register/", views.UserRegisterView.as_view(), name="register"),
    path("api/user/login/", views.UserLoginView.as_view(), name="login"),
    path("api/user/refresh/", TokenRefreshView.as_view(), name="token_refresh")
]