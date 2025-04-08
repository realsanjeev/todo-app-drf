from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path("auth/", obtain_auth_token, name="authentication"),
    path("search/", views.todo_search_view, name="search"),
    # crud operation
    path("", views.todo_create_retrieve_view, name="create"),
    path("<int:pk>/", views.todo_detail_retrieve_view, name="todo-detail"),
    path("<int:pk>/update/", views.todo_update_view, name="update"),
    path("<int:pk>/delete/", views.todo_delete_view, name="delete"),
]
