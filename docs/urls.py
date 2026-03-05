from django.urls import path
from .views import space_list_view, space_details_view, page_details_view, create_page_view, edit_page_view

app_name = "docs"

urlpatterns = [
    path("", space_list_view, name="space_list"),
    path("<slug:space_slug>", space_details_view, name="space_details"),
    path("<slug:space_slug>/<slug:page_slug>", page_details_view, name="page_details"),
    path("<slug:space_slug>/create/", create_page_view, name="create_page"),
    path("<space_slug>/<page_slug>/edit/", edit_page_view, name="edit_page"),
]