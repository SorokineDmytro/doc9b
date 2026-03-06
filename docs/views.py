from accounts.decorators import role_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Space, Page
from taggit.models import Tag
from .forms import PageForm, SpaceForm

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

@role_required("admin")
def create_space_view(request):
    if request.method == "POST":
        form = SpaceForm(request.POST)
        if form.is_valid():
            space = form.save(commit=False)
            space.space = space
            space.save()
            form.save_m2m()
            return redirect("docs:space_list")
    else:
        form = SpaceForm()
    
    return render(
        request,
        "docs/space_form.html",
        {"form": form, "mode": "create"},
    )

@role_required("redactor")
def edit_space_view(request, space_slug):
    space = get_object_or_404(Space, slug=space_slug)
    
    if request.method == "POST":
        form = SpaceForm(request.POST, instance=space)
        if form.is_valid():
            space = form.save(commit=False)
            space.save()
            form.save_m2m()
            return redirect("docs:space_details", space_slug=space_slug)
    else:
        form = SpaceForm(initial={"space": space}, instance=space)
    
    return render(
        request,
        "docs/space_form.html",
        {"form": form, "mode": "edit"},
    )

@role_required("admin")
def delete_space_view(request, space_slug):
    space = get_object_or_404(Space, slug=space_slug)

    if request.method == "POST":
        space.delete()
        return redirect("docs:space_list")
    
    return render(request, "docs/confirm_delete.html", {"space": space, "object_type": "Espace", "object_name": space.name })


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
            page.tags.set(form.cleaned_data["tags"])
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
            page.tags.set(form.cleaned_data["tags"])
            form.save_m2m()
            return redirect("docs:page_details", space_slug=space.slug, page_slug=page.slug)
    else:
        form = PageForm(initial={"space": space}, instance=page)
    
    return render(
        request,
        "docs/page_form.html",
        {"form": form, "space": space, "mode": "edit"},
    )

@role_required("redactor")
def delete_page_view(request, space_slug, page_slug):
    space = get_object_or_404(Space, slug=space_slug)
    page = get_object_or_404(Page, space=space, slug=page_slug)

    if request.method == "POST":
        page.delete()
        return redirect("docs:space_details", space_slug=space.slug)
    
    return render(request, "docs/confirm_delete.html", {"space": space, "object_type": "Page", "object_name": page.title })


@role_required("reader")
def page_list_by_tag_view(request, space_slug, tag_slug):
    space = get_object_or_404(Space, slug=space_slug)
    tag = get_object_or_404(Tag, slug=tag_slug)
    pages = (Page.objects.filter(space=space, tags=tag).order_by('order', 'title'))
    
    return render(
        request,
        "docs/page_list_by_tag.html",
        {
        "space": space,
        "tag": tag,
        "pages": pages
        }
    )
