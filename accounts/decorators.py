from functools import wraps
from django.http import HttpResponseForbidden
from django.contrib.auth.views import redirect_to_login

ROLE_ORDER = {"reader": 1, "redactor": 2, "admin": 3}

def role_required(min_role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            
            if request.user.category and request.user.category.slug in ROLE_ORDER:
                user_role = request.user.category.slug
            else:
                user_role = "reader"

            if ROLE_ORDER.get(user_role, 0) < ROLE_ORDER[min_role]:
                return HttpResponseForbidden("403 - Forbidden")
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator