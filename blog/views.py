from django.shortcuts import render, get_object_or_404
from .models import Post, Categorie


def index(request):
    categories = Categorie.objects.all()
    posts = Post.objects.order_by('-views')[:6]
    return render(request, 'blog/index.html', {'categories': categories, 'posts': posts})

def post_list(request):
    posts = Post.objects.all().order_by('-id')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.views += 1
    post.save()
    return render(request, 'blog/post_detail.html', {'post': post})

def category_posts(request, slug):
    category = get_object_or_404(Categorie, slug=slug)
    posts = Post.objects.filter(category_id=category)
    return render(request, 'blog/category_posts.html', {'category': category, 'posts': posts})