from django.urls import path
from .views import (
    space_list_view,
    space_details_view,
    page_details_view,
    create_page_view,
    edit_page_view,
    delete_page_view,
    page_list_by_tag_view,
    create_space_view,
    edit_space_view,
    delete_space_view,
)

app_name = "docs"

urlpatterns = [
    path("", space_list_view, name="space_list"),
    path("create/", create_space_view, name="create_space"),
    path("<slug:space_slug>/edit/", edit_space_view, name="edit_space"),
    path("<slug:space_slug>/delete/", delete_space_view, name="delete_space"),
    path("<slug:space_slug>/", space_details_view, name="space_details"),

    path(
        "<slug:space_slug>/tag/<slug:tag_slug>/",
        page_list_by_tag_view,
        name="page_list_by_tag",
    ),
    path("<slug:space_slug>/create/", create_page_view, name="create_page"),
    path("<slug:space_slug>/<slug:page_slug>/edit/", edit_page_view, name="edit_page"),
    path("<slug:space_slug>/<slug:page_slug>/delete/", delete_page_view, name="delete_page"),
    path("<slug:space_slug>/<slug:page_slug>/", page_details_view, name="page_details"),
]
