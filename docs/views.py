from django.shortcuts import render, get_object_or_404
from .models import Space, Page

# List of all spaces
def space_list_view(request):
    spaces = Space.objects.all()
    
    return render(
        request,
        'docs/space_list.html',
        {'spaces': spaces,},
    )

# Selected space details with root pages
def space_details_view(request, space_slug):
    space = get_object_or_404(Space, slug=space_slug)
    root_pages = (
        Page.objects.filter(space=space, parent__isnull=True).order_by('order', 'title')
    )

    return render(
        request,
        'docs/space_details.html',
        {
            'space': space,
            'root_pages': root_pages,
        }
    )

# Selected page details with breadcrumbs for navigation
def page_details_view(request, space_slug, page_slug):
    space = get_object_or_404(Space, slug=space_slug)
    page = get_object_or_404(Page, space=space, slug=page_slug)

    children = page.children.all().order_by('order', 'title')

    breadcrumbs = []
    current_page = page
    # recursion test
    while current_page is not None:
        breadcrumbs.append(current_page)
        current_page = current_page.parent
    # return a list order to be parent -> children
    breadcrumbs.reverse()

    return render(
        request,
        'docs/page_details.html',
        {
            'space': space,
            'page': page,
            'children': children,
            'breadcrumbs': breadcrumbs,
        }    
    )
