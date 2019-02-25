from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import Answer, Prompt, Template, TemplateCopy

# Create your views here.

def index(request):
    decision_templates = Template.objects.filter(deleted=False)
    context = {
        'decision_templates': list(decision_templates)
    }
    return render(request, 'decisions/index.html', context)


def preview(request, template_id):
    decision_template = get_object_or_404(Template, pk=template_id)
    context = {
        'decision_template': decision_template
    }
    return render(request, 'decisions/preview.html', context)


@require_POST
def copy(request):
    template = get_object_or_404(Template, pk=request.POST.get('template_id'))
    template_copy = TemplateCopy(template=template)
    template_copy.save()
    return HttpResponseRedirect(reverse('decisions:fill_form', args=(template_copy.id,)))


def fill_form(request, copy_id):
    copy = get_object_or_404(TemplateCopy, pk=copy_id)
    context = {
        'copy': copy
    }
    return render(request, 'decisions/fill_form.html', context)


@require_POST
def save_copy(request):
    post_data = request.POST
    copy_id = post_data.get('copy_id')
    template_copy = get_object_or_404(TemplateCopy, pk=copy_id)
    template_copy.label = post_data.get('label', '')
    for prompt_id in post_data.keys():
        if not prompt_id.isdigit():
            continue
        try:
            prompt = get_object_or_404(Prompt, pk=prompt_id)
        except Http404:
            continue

        answer, was_created = Answer.objects.get_or_create(template_copy_id=copy_id, prompt_id=prompt_id)
        answer_value = post_data[prompt_id]
        answer.store_value(answer_value)

    template_copy.save()
    return HttpResponseRedirect(reverse('decisions:fill_form', args=(template_copy.id,)))
