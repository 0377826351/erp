from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from ...models import Question

def index(request):
  template = loader.get_template('website/hoidap/hoidap.html')
  list_questions = Question.objects.all()
  print(list_questions)
  context = {
    'title': 'Câu Hỏi Thường Gặp',
    'list_questions': list_questions,
  }
  return HttpResponse(template.render(context, request))