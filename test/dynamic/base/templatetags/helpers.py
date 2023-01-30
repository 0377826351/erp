from django.conf import settings
from django.template.defaulttags import register
from django.utils.safestring import mark_safe

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter()
def filter_get_name(value, arg):
    if arg == "first_name": return value.split(" ")[-1]
    if arg == "last_name": return ' '.join(value.split(" ")[:-1])
    return value

@register.filter()
def filter_dir(value):
    return dir(value)

@register.filter
def get_fields_form(form):
    res = {}
    for f in form:
        res[f.name] = f.label
    return res

@register.filter()
def active_render(value):
    xhtml = '<span class="badge bg-success bg-gradient text-light">Hoạt động</span>' if value else '<span class="badge bg-danger bg-gradient text-light">Ngừng hoạt động</span>'
    return mark_safe(xhtml)

@register.filter()
def get_src_image(value):
    return settings.MEDIA_URL + 'images/full/' + value if value else settings.MEDIA_URL + 'images/full/others/default_avatar.png'

@register.filter()
def get_src_video(value):
    return settings.MEDIA_URL + 'files/' + value if value else ''   

@register.filter
def get_string_as_list(value): # Only one argument.
    """Evaluate a string if it contains []"""
    if not value:
        return eval("['Empty']")
    if '[' and ']' in value:
        return eval(value)
