from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.contrib import messages
from base.helpers import HanlderFile, paginator, reverse_url
from base.views import BaseDeleteView, BaseView, BaseListView
from .form import DocumentForm, DocumentFormSearch
from .model import Document

# =========================================================================================================
class DocumentView(BaseView):
    MODULE_NAME = 'Document'
    URL_NAME = 'document'
    TEMPLATE_PATH = 'document/'
    MEDIA_PATH = 'document'
    
    def init(self, request):
        self.MODEL = Document
        self.params['url_name'] = self.URL_NAME
        return super().init(request)

# =========================================================================================================
class DocumentListView(BaseListView, DocumentView):
    def init(self, request):
        self.set_template('list.html')
        self.config_page_header('Danh sách', button_params=[
            {'type': 'danger', 'text': 'Xoá', 'add_class': 'action-multi-items action-delete', 'attrs': {'data-bs-toggle': 'modal', 'data-bs-target': '#confirmDeleteModel'}},
            {'type': 'primary', 'text': 'Thêm', 'href': reverse_url('document.add')}
        ])
        return super().init(request)

    def get(self, request, page=1):
        self.params['form'] = DocumentFormSearch(self.params.get('get_data'))
        # Paginator
        self.params = {**self.params, **paginator(self.MODEL.list_item(self.params.get('get_data'), {'task': 'list-item'}), {'page': page, **self.params})}
        # End paginator
        return render(request, self.template, self.params)

    def post(self, request):
        pass
    
# =========================================================================================================
class DocumentFormView(DocumentView):
    def init(self, request, id=None):
        self.set_template('form.html')
        title = 'Cập nhật' if id else 'Thêm mới'
        self.config_page_header(title, button_params=[
            {'text': 'Quay lại', 'href': reverse_url('document')},
            {'type': 'submit', 'text': 'Lưu'}
        ])
        return super().init(request)

    def get(self, request, id=None):
        if id:
            item = self.MODEL.get_item_by_id(id) if id else None
            self.params['form'] = DocumentForm({'id': id, **model_to_dict(item)})
        else:
            self.params['form'] = DocumentForm()
        return render(request, self.template, self.params)

    def post(self, request, id=None):
        task = 'change' if id else 'add'
        post_data = self.params.get('post_data')
        image_file = request.FILES.get('upload_image')
        validate_image = None
        if image_file:
            validate_image = HanlderFile.validate_file_input(image_file)
            post_data['image'] = validate_image
        form = DocumentForm(post_data)
        if form.is_valid():
            instance = self.MODEL.objects.get(id=id) if id else None
            if validate_image == True and instance and instance.image: HanlderFile.delete_image(instance.image)
            if image_file: post_data['image'] = HanlderFile.upload_image(image_file, self.MEDIA_PATH).get('dir')
            result = self.MODEL.save_item(post_data, {'task': task})
            if result:
                messages.add_message(request, messages.SUCCESS, 'Thêm bản ghi thành công.' if task == 'add' else 'Cập nhật bản ghi thành công.')
                return redirect(self.URL_NAME)
        self.params['form'] = form;
        return render(request, self.template, self.params)

class DocumentDeleteView(BaseDeleteView, DocumentView): pass