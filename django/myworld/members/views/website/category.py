from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from ...models import Category,Article
from django.core.paginator import Paginator

def index(request, slug=None):
  list_post = []
  title = "Blog"

  template = loader.get_template('website/category/category.html')
  if (slug == None): 
    list_post = Article.objects.all()
  else:
    obj = Category.objects.get(alias_category = slug)
    title = obj.name
    list_post = Article.objects.filter(category = slug)

  paginator = Paginator(list_post,6)
  page_number = request.GET.get('page',1)
  page_obj = paginator.get_page(page_number)
  context = {
    'title': title,
    'page_obj': page_obj,
    'page_range': page_obj.paginator.get_elided_page_range(page_number,on_each_side=1,on_ends=1)
  }

  return HttpResponse(template.render(context, request))
