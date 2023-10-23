from functools import wraps
from django.http import HttpResponseRedirect
from django.contrib import messages


def anonymous_required(view_func):
    @wraps(view_func)
    def _wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "Only unauthenticated users can register")
            return HttpResponseRedirect("/")
        return view_func(request, *args, **kwargs)

    return _wrapper
