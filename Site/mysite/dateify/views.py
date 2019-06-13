from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from .models import Post

from .forms import PostForm

def post(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PostForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/posts/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PostForm()

    return render(request, 'post.html', {'form': form})

def posts(request):
    context = {'user': request.user}
    return render(request, 'posts.html', context=context)

def api_posts(request):
    posts = list(Post.objects.filter(user_id=request.user).values_list('day', 'summary', 'text', 'related_posts'))
    return JsonResponse({'dates': posts})