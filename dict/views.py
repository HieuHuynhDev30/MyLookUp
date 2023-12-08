from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import WordForm


# Create your views here.
@csrf_exempt
def lookup(request):
    search_result = {}
    if request.method == "POST":
        form = WordForm(request.POST)
        if form.is_valid():
            search_result = form.search()
            search_result['success'] = True
    else:
        form = WordForm()
        search_result['success'] = False
    return render(request, 'dict/index.html', {'form': form, 'search_result': search_result, })
