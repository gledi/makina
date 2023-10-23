import json
from http import HTTPStatus

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.utils.translation import gettext as _

from .models import Post


def get_posts(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.filter(is_published=True).all()
    return render(
        request,
        "blog/post_list.html",
        context={"posts": posts},
    )


def get_post_details(request: HttpRequest, pk: int) -> HttpResponse:
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponseNotFound("Post not found")

    key = f"post_{post.pk}_views"
    request.session[key] = request.session.get(key, 0) + 1

    return render(
        request,
        "blog/post_detail.html",
        context={"post": post},
    )


def manage_posts(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.all()
    return render(request, "blog/post_manage.html", context={"posts": posts})


@csrf_exempt
def publish_post(request: HttpRequest) -> HttpResponse:
    cmd = json.loads(request.body)
    try:
        post = Post.objects.get(pk=cmd["postId"])
    except Post.DoesNotExist:
        return JsonResponse(
            {"message": _("Post does not exist")}, status=HTTPStatus.NOT_FOUND
        )

    post.is_published = True
    post.published_on = timezone.now()
    post.save()

    return JsonResponse({"message": _("Post has been published successfully")})
