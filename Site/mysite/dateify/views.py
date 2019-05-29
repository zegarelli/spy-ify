from django.shortcuts import render
from django.http import JsonResponse
from .models import Date
# Create your views here.


def betsy(request):
    context = {'user': request.user}
    return render(request, 'relationship.html', context=context)

def dates(request):
    dates = list(Date.objects.all().values_list('day', 'text'))
    return JsonResponse({'dates': dates})