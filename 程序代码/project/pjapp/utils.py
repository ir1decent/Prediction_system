# utils.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def login_required_decorator(view_func):
    decorated_view_func = login_required(view_func)

    def check_login_and_redirect(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('')
        return decorated_view_func(request, *args, **kwargs)

    return check_login_and_redirect
