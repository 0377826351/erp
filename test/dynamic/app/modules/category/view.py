from base.helpers import HanlderFile, model_to_dict
from django.shortcuts import redirect, render
from .model import Category
from .form import CategoryForm, CategorySearchForm
from base.helpers import paginator, reverse_url
from base.views import BaseDeleteView, BaseListView, BaseView
from django.contrib import messages

class CategoryView(BaseView):
    MODULE_NAME = 'Danh mục'
    URL_NAME = 'category'
    TEMPLATE_PATH = 'category/'
    MEDIA_PATH = 'category'

    def init(self, request):
        self.MODEL = Category
        self.params['url_name'] = self.URL_NAME
        self.params['form'] = CategoryForm()
        return super().init(request)


class CategoryFormView(CategoryView):
    def init(self,request,id=None):
        self.set_template('form.html')
        return super().init(request)

    def _config_page_header(self, id=None, type=''):
        title = 'Thêm mới'
        button_back_href = reverse_url('category')
        if id:
            title = 'Cập nhật'
            instance = Category.objects.get(id=id)
            if instance: button_back_href += '?type=' + instance.type
        if type:
            button_back_href += '?type=' + type
        self.config_page_header(title, button_params=[
            {'text': 'Quay lại', 'href': button_back_href},
            {'type': 'submit', 'text': 'Lưu'}
        ]) 

    def get(self,request,id=None):
        type = self.params.get('get_data').get('type')
        parent_id = self.params.get('get_data').get('parent_id')
        self._config_page_header(id,type)
        item = self.MODEL.objects.get(id=id) if id else None
        self.params['form'] = CategoryForm(initial=model_to_dict(item) if item else {'type':type,'parent_id':parent_id})
        return render(request,self.template,self.params)

    def post(self, request, id=None):
        self._config_page_header(id)
        task = 'change' if id else 'add'
        post_data = self.params.get('post_data')
        image_file = request.FILES.get('upload_image')
        validate_image = None
        if image_file:
            validate_image = HanlderFile.validate_file_input(image_file)
            post_data['image'] = validate_image
        form = CategoryForm(post_data)
        if form.is_valid():
            instance = self.MODEL.objects.get(id=id) if id else None
            if validate_image == True and instance and instance.image: HanlderFile.delete_image(instance.image)
            if image_file: post_data['image'] = HanlderFile.upload_image(image_file, self.MEDIA_PATH).get('dir')
            result = self.MODEL.save_item(post_data, {'task': task})
            if result:
                messages.add_message(request, messages.SUCCESS, 'Thêm bản ghi thành công.' if task == 'add' else 'Cập nhật bản ghi thành công.')
                return redirect(reverse_url('category') + '?type=' + post_data.get('type'))
        self.params['form'] = form
        return render(request, self.template, self.params)


class CategoryListView(BaseListView,CategoryView): 
    def init(self, request):
        self.set_template('list.html')
        return super().init(request)
        
    def get(self, request, page=1):
        get_data = self.params.get('get_data')
        self.config_page_header('Danh sách', button_params=[
            {'type': 'outline-primary', 'text': 'Cây danh mục', 'href': reverse_url('category', url_params={'type': get_data.get('type')})},
            {'type': 'danger', 'text': 'Xoá', 'add_class': 'action-multi-items action-delete', 'attrs': {'data-bs-toggle': 'modal', 'data-bs-target': '#confirmDeleteModel'}},
            {'type': 'primary', 'text': 'Thêm', 'href': reverse_url('category.add', url_params={'type': get_data.get('type')})},
        ])
        self.params['form'] = CategorySearchForm(get_data)
        self.params = {**self.params, **paginator(self.MODEL.list_item(get_data, {'task': 'list-item'}), {'page': page, **self.params})}
        return render(request, self.template, self.params)


class CategoryNestedListView(CategoryView):
    
    def init(self, request):
        self.set_template('nested-list.html')
        return super().init(request)
        
    def get(self, request):
        type = self.params.get('get_data').get('type')
        self.config_page_header('Cây', button_params=[
            {'type': 'outline-primary', 'text': 'Danh sách', 'href': reverse_url('category.list', url_params={'type': type})},
            {'type': 'primary', 'text': 'Thêm', 'href': reverse_url('category.add', url_params={'type': type}) }
        ])
        self.params['items'] = self.MODEL.objects.filter(type=type).order_by('multi_index', 'created_at') if type else self.MODEL.objects.order_by('multi_index', 'created_at')
        return render(request, self.template, self.params)


class CategoryDeleteView(BaseDeleteView,CategoryView): pass