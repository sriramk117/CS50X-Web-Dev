from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<title>", views.go_to_entry, name="entry"),
    path("search", views.search, name="search"),
    path("create", views.create_new_page, name="create"),
    path("edit/<title>", views.edit_page, name="edit"),
    path("random", views.random_page, name="random")
]
