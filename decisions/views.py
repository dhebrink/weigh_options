from django.shortcuts import render

# Create your views here.

def index(request):
    context = {
        'decision_templates': ['thing1', 'thing2']
    }
    return render(request, 'decisions/index.html', context)
