# Create the register instance by initializing it with the Library instance.
from django.template.defaulttags import register
from django import template
register = template.Library()
from ..models import Article
from django.contrib.auth.models import User
from urllib import parse

@register.inclusion_tag('website/templatetags/post.html')
def show_post(page_obj):
    return {'page_obj': page_obj}

@register.inclusion_tag('admin/templatetags/noti.html')
def noti(noti):
    print(noti)
    icon = {
        'danger':'ban',
        'info':'info',
        'warning':'exclamation-triangle',
        'success':'check',
    }
    return {'noti': noti, 'icon': icon}

@register.filter(name="keyvalue")
def keyvalue(dict, key):    
    return dict[key]

@register.filter(name='url')
def append_url(url,i):
    rep_list=['page',i]
    queries = url
    print(queries)

    if len(rep_list) > 1:
        rep_key = rep_list[0]
        rep_val = rep_list[1]
    
        if 'http' in url:
            queries = parse.urlsplit(url).query

        dict_params = dict(parse.parse_qsl(queries))
        dict_params.update({rep_key: rep_val})

        queries_list = []

        for (k, v) in dict_params.items():
            queries_list.append('%s=%s' % (k, v))

        base_url_list = url.split('?')
        base_url = base_url_list[0]
        
        if len(base_url_list) <= 1:
            base_url = ''
        
        queries_str = '&'.join(queries_list)
        print('%s?%s' % (base_url, queries_str))
        
        return '%s?%s' % (base_url, queries_str)

    return url
