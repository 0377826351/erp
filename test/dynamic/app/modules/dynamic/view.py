from django.shortcuts import render, redirect
from django.contrib import messages

from base.helpers import paginator, reverse_url
from base.views import BaseDeleteView, BaseView, BaseListView
from .form import DynamicForm, DynamicFormSearch
from .model import Dynamic

# =========================================================================================================
class DynamicView(BaseView):
    MODULE_NAME = 'Dynamic'
    URL_NAME = 'dynamic'
    TEMPLATE_PATH = 'dynamic/'
    
    def init(self, request):
        self.MODEL = Dynamic
        self.params['url_name'] = self.URL_NAME
        return super().init(request)

    def set_template(self, html_file):
        self.template = self.TEMPLATE_PATH + html_file

    def set_page_title(self, title):
        self.params['page_title'] = '%s - %s' % (self.MODULE_NAME, title)

# =========================================================================================================
class DynamicListView(BaseListView, DynamicView):
    def init(self, request):
        self.set_template('list.html')
        self.config_page_header('Danh sách', button_params=[
            {'type': 'danger', 'text': 'Xoá', 'add_class': 'action-multi-items action-delete', 'attrs': {'data-bs-toggle': 'modal', 'data-bs-target': '#confirmDeleteModel'}},
            {'type': 'primary', 'text': 'Thêm', 'href': reverse_url('dynamic.add')}
        ])
        return super().init(request)

    def get(self, request, page=1):
        self.params['form'] = DynamicFormSearch(self.params.get('get_data'))
        
        # Paginator
        self.params = {**self.params, **paginator(self.MODEL.list_item(self.params.get('get_data'), {'task': 'list-item'}), {'page': page, **self.params})}
        # End paginator
        return render(request, self.template, self.params)

    def post(self, request):
        pass

class DynamicFormView(DynamicView):
    def init(self, request, id=None):
        self.set_template('form.html')
        title = 'Cập nhật' if id else 'Thêm mới'
        self.config_page_header(title, button_params=[
            {'text': 'Quay lại', 'href': reverse_url('dynamic')},
            {'type': 'submit', 'text': 'Lưu'}
        ])        
        return super().init(request)

    def get(self, request, id=None):
        item = self.MODEL.get_item_by_id(id) if id else None
        self.params['form'] = DynamicForm(item.__dict__ if item else None)
        return render(request, self.template, self.params)

    def post(self, request, id=None):
        task = 'change' if id else 'add'
        post_data = self.params.get('post_data') or None
        form = DynamicForm(post_data)
        if form.is_valid():
            result = self.MODEL.save_item(post_data, {'task': task})
            if result:
                messages.add_message(request, messages.SUCCESS, 'Thêm bản ghi thành công.' if task == 'add' else 'Cập nhật bản ghi thành công.')
                return redirect(self.URL_NAME)
        self.params['form'] = form;
        return render(request, self.template, self.params)

class DynamicDeleteView(BaseDeleteView, DynamicView): pass
