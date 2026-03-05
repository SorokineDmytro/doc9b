from accounts.decorators import role_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Space, Page
from .forms import PageForm

# List of all spaces
@role_required("reader")
def space_list_view(request):
    spaces = Space.objects.all()
    
    return render(
        request,
        'docs/space_list.html',
        {'spaces': spaces,},
    )

# Selected space details with root pages
@role_required("reader")
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
@role_required("reader")
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

@role_required("redactor")
def create_page_view(request, space_slug):
    space = get_object_or_404(Space, slug=space_slug)
    
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.space = space
            page.save()
            form.save_m2m()
            return redirect("docs:page_details", space_slug=space.slug, page_slug=page.slug)
    else:
        form = PageForm(initial={"space": space})
    
    return render(
        request,
        "docs/page_form.html",
        {"form": form, "space": space, "mode": "create"},
    )

@role_required("redactor")
def edit_page_view(request, space_slug, page_slug):
    space = get_object_or_404(Space, slug=space_slug)
    page = get_object_or_404(Page, space=space, slug=page_slug)
    
    if request.method == "POST":
        form = PageForm(request.POST, instance=page)
        if form.is_valid():
            page = form.save(commit=False)
            page.space = space
            page.save()
            form.save_m2m()
            return redirect("docs:page_details", space_slug=space.slug, page_slug=page.slug)
    else:
        form = PageForm(initial={"space": space}, instance=page)
    
    return render(
        request,
        "docs/page_form.html",
        {"form": form, "space": space, "mode": "edit"},
    )