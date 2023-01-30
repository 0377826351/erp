from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from ...models import Article,Category

def index(request, slug, id):
  template = loader.get_template('website/singleblog/singleblog.html')
  obj = Article.objects.get(id=id)
  obj_cate = Category.objects.get(alias_category = obj.category)
  list_post = Article.objects.filter(category=obj.category)[:6]
  context = {
    'title': obj.title,
    'list_post': list_post,
    'obj': obj,
    'obj_cate': obj_cate,
  }
  return HttpResponse(template.render(context, request))