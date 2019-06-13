from django.shortcuts import render
from django.http import JsonResponse
from .models import Post
# Create your views here.


def post(request):
    context = {'user': request.user}
    return render(request, 'post.html', context=context)

def posts(request):
    context = {'user': request.user}
    return render(request, 'posts.html', context=context)

def api_posts(request):
    posts = list(Post.objects.filter(user_id=request.user).values_list('day', 'summary', 'text', 'related_posts'))
    return JsonResponse({'dates': posts})