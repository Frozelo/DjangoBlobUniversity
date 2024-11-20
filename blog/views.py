import json
import logging

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from .models import Post, Categorie


def index(request):
    categories = Categorie.objects.all()
    posts = Post.objects.order_by('-views')[:6]
    return render(request, 'blog/index.html', {'categories': categories, 'posts': posts, 'now': now()})

def post_list(request):
    posts = Post.objects.all().order_by('-id')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.views += 1
    post.save()
    return render(request, 'blog/blog-post.html', {'post': post})

def category_posts(request, slug):
    category = get_object_or_404(Categorie, slug=slug)
    posts = Post.objects.filter(category_id=category)
    return render(request, 'blog/blog-list.html', {'category': category, 'posts': posts})


@csrf_exempt
def update_time_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Received data:", data)

            post_id = data.get("post_id")
            time_spent = data.get("view_time")

            if post_id is None or time_spent is None:
                return JsonResponse({
                    'status': 'failed',
                    'error': 'Missing post_id or view_time'
                }, status=400)

            post = get_object_or_404(Post, id=post_id)
            current_read = float(post.read_time)
            time_spent = float(time_spent)

            new_read_time = (current_read + time_spent) / 2

            post.read_time = new_read_time
            post.save()

            return JsonResponse({
                'status': 'success',
                'new_read_time': new_read_time
            })

        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'failed',
                'error': 'Invalid JSON'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'failed',
                'error': str(e)
            }, status=500)

    return JsonResponse({
        'status': 'failed',
        'error': 'Only POST method is allowed'
    }, status=405)