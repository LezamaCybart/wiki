from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_title>", views.display_entry, name="display_entry"),
    path("search", views.search, name="search"),
    path("new_page", views.new_page, name="new_page"),
    path("edit_page/<str:entry_title>", views.edit_page, name="edit_page"),
    path("random", views.random_page, name="random_page")
]
