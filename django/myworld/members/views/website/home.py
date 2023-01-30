from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
from ...models import Article,Category
from django.core.paginator import Paginator

def index(request):
  searched = request.GET.get('q')
  print(searched)
  if not searched:
    template = loader.get_template('website/home/index.html')
    return HttpResponse(template.render({'title': 'Trang chủ'}, request))
  else:
    page_obj = Article.objects.filter(title__icontains = searched)
    template = loader.get_template('website/category/category.html')

    paginator = Paginator(page_obj,2)
    page_number = request.GET.get('page',1)

    page_obj = paginator.get_page(page_number)

    context = {
      'title': 'Tìm Kiếm',
      'page_obj': page_obj,
      'page_range': page_obj.paginator.get_elided_page_range(page_number,on_each_side=1,on_ends=1)
    }

    return HttpResponse(template.render(context, request))