from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.inclusion_tag('block/page_header.html')
def render_page_header(config_page_header={}):
    title = config_page_header.get('title')
    button_params = config_page_header.get('button_params')
    button_html = ""

    for button in button_params:
        id = button.get('id', '')
        if id: id = ' id="%s"' % id 
        type = button.get('type', 'secondary')
        text = button.get('text', 'Nút')
        icon = '<i class="%s"></i> ' % button.get('icon_class') if button.get('icon_class') else ''
        add_class = button.get('add_class', '')
        href = button.get('href', '#')
        if add_class: add_class = ' ' + add_class
        tag_class = "btn btn-{}{}".format(type, add_class)
        tag_attrs = ""
        attrs = button.get('attrs')

        if attrs:
            for key in attrs:
                tag_attrs += '{}="{}"'.format(key, attrs[key])
            tag_attrs = " " + tag_attrs

        if type == 'submit':
            button_html += '<button{} type="submit" class="btn btn-primary" {}>{}{}</button>'.format(id, tag_attrs, icon, text)
            continue
        if type == 'reset':
            button_html += '<button{} type="reset" class="btn btn-secondary" {}>{}{}</button>'.format(id, tag_attrs, icon, text)
            continue

        # Other:
        button_html += '<a{id} class="{tag_class}" href="{href}" {tag_attrs}>{text}</a>'.format(id=id, tag_class=tag_class, href=href, text=text, tag_attrs=tag_attrs)
    return { 'page_title': title, 'button_html': mark_safe(button_html) }

@register.inclusion_tag('block/filter_box.html')
def render_filter_box(form, button_filter=True, button_delete=True):
    return {'form': form, 'button_filter': button_filter, 'button_delete': button_delete}

@register.inclusion_tag('block/pagination.html')
def pagination_tag(items, page_range, get_data, pagination, url_name):
    print(items,page_range,get_data, pagination, url_name)
    return { 'items': items, 'page_range': page_range, 'get_data': get_data, 'pagination': pagination, 'url_name': url_name }

@register.inclusion_tag('block/confirm_dialog.html')
def render_confirm_dialog(id="confirmModel", type="", label="", message="", text_confirm="Đổng ý", text_cancel="Huỷ", href_confirm="."):
    if type == "delete":
        label = "Xoá bản ghi" 
        message = "Bản ghi này sẽ bị xoá vĩnh viễn. Bạn có muốn tiếp tục thực hiện hành động này?"
        
    return {'id': id, 'label': label, 'message': message, 'text_confirm': text_confirm, 'text_cancel': text_cancel, 'href_confirm': href_confirm}
