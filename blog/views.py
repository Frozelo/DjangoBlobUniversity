import json
import logging

from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now

from .documents import PostDocument
from .models import Post, Categorie, Tag


def index(request):
    categories = Categorie.objects.all()
    tags = Tag.objects.all()
    tag_slugs = request.GET.getlist('tags')
    query = request.GET.get('q', '')

    # Base queryset
    if query:
        s = PostDocument.search().query("multi_match", query=query, fields=['title', 'description', 'content'])
        posts = s.to_queryset()
    else:
        posts = Post.objects.all()

    # Filter by tags if any
    if tag_slugs:
        selected_tags = Tag.objects.filter(slug__in=tag_slugs)
        if selected_tags.exists():
            posts = posts.filter(tags__in=selected_tags).distinct()

    # Order the posts
    posts = posts.order_by('-views')

    # Set up pagination
    paginator = Paginator(posts, 6)  # Show 6 posts per page
    page = request.GET.get('page')

    try:
        paginated_posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated_posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results.
        paginated_posts = paginator.page(paginator.num_pages)

    context = {
        'categories': categories,
        'tags': tags,
        'posts': paginated_posts,  # Use paginated posts
        'now': now(),
        'query': query,
        'page_obj': paginated_posts,  # For pagination controls
        'paginator': paginator,
        'is_paginated': paginated_posts.has_other_pages(),
    }

    return render(request, 'blog/index.html', context)


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.views += 1
    post.save()
    return render(request, 'blog/blog-post.html', {'post': post})


def category_posts(request, slug):
    category = get_object_or_404(Categorie, slug=slug)
    posts = Post.objects.filter(category_id=category)
    tags = Tag.objects.filter(post__in=posts).distinct()
    return render(request, 'blog/blog-list.html', {'category': category, 'posts': posts, 'tags': tags})


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


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Post, Tag


def filter_posts_by_tags(request):
    tag_slugs = request.GET.getlist('tags')

    if not tag_slugs:
        return JsonResponse({'status': 'failed', 'error': 'No tags provided'}, status=400)

    # Находим теги, переданные в URL
    tags = Tag.objects.filter(slug__in=tag_slugs)

    if not tags.exists():
        return JsonResponse({'status': 'failed', 'error': 'No matching tags found'}, status=404)

    # Фильтруем посты, которые содержат хотя бы один из выбранных тегов
    posts = Post.objects.filter(tags__in=tags).distinct()

    # Сортировка
    sort_by = request.GET.get('sort_by', 'created_at')
    if sort_by not in ['created_at', 'views']:
        sort_by = 'created_at'
    posts = posts.order_by(f'-{sort_by}')

    # Подготовка данных для ответа
    results = [
        {
            'id': post.id,
            'title': post.title,
            'slug': post.slug,
            'description': post.description,
            'views': post.views,
            'thumbnail': post.thumbnail.url if post.thumbnail else None,
            'created_at': post.created_at.isoformat(),
            'updated_at': post.updated_at.isoformat(),
            'read_time': post.read_time,
        }
        for post in posts
    ]

    return JsonResponse({'status': 'success', 'posts': results}, safe=False)
