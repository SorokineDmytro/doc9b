from django.urls import path
from .views import space_list_view, space_details_view, page_details_view

urlpatterns = [
    path("", space_list_view),
    path("<slug:space_slug>", space_details_view),
    path("<slug:space_slug>/<slug:page_slug>", page_details_view),
]