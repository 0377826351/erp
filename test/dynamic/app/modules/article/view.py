from base.helpers import model_to_dict
from django.shortcuts import redirect, render
from .form import ArticleForm, ArticleSearchForm
from .model import Article
from base.helpers import HanlderFile, paginator, reverse_url
from base.views import BaseDeleteView, BaseListView, BaseView
from django.contrib import messages

# =========================================================================================================
class ArticleView(BaseView):
    MODULE_NAME = 'Bài viết'
    URL_NAME = 'article'
    TEMPLATE_PATH = 'article/'
    MEDIA_PATH = 'article'

    def init(self, request):
        self.MODEL = Article
        self.params['url_name'] = self.URL_NAME
        return super().init(request)

class ArticleFormView(ArticleView):
    def init(self, request, id=None):
        self.set_template('form.html')
        title = 'Cập nhật' if id else 'Thêm mới'
        self.config_page_header(title, button_params=[
            {'text': 'Quay lại', 'href': reverse_url('article')},
            {'type': 'submit', 'text': 'Lưu'}
        ])        
        return super().init(request)

    def get(self, request, id=None):
        item = self.MODEL.objects.get(id=id) if id else None
        self.params['form'] = ArticleForm(initial=model_to_dict(item) if item else {})
        return render(request, self.template, self.params)

    def post(self, request, id=None):
        task = 'change' if id else 'add'
        post_data = self.params.get('post_data')
        image_file = request.FILES.get('upload_image')
        validate_image = None
        if image_file:
            validate_image = HanlderFile.validate_file_input(image_file)
            post_data['image'] = validate_image
        form = ArticleForm(post_data)
        if form.is_valid():
            instance = self.MODEL.objects.get(id=id) if id else None
            if validate_image == True and instance and instance.image: HanlderFile.delete_image(instance.image)
            if image_file: post_data['image'] = HanlderFile.upload_image(image_file, self.MEDIA_PATH).get('dir')
            if self.MODEL.save_item(post_data, {'task': task}):
                messages.add_message(request, messages.SUCCESS, 'Thêm bản ghi thành công.' if task == 'add' else 'Cập nhật bản ghi thành công.')
                return redirect(self.URL_NAME)

        self.params['form'] = form;
        return render(request, self.template, self.params)

# =========================================================================================================
class ArticleListView(BaseListView, ArticleView):
    def init(self, request):
        self.set_template('list.html')
        self.config_page_header('Danh sách', button_params=[
            {'type': 'danger', 'text': 'Xoá', 'add_class': 'action-multi-items action-delete', 'attrs': {'data-bs-toggle': 'modal', 'data-bs-target': '#confirmDeleteModel'}},
            {'type': 'primary', 'text': 'Thêm', 'href': reverse_url('article.add')}
        ])
        return super().init(request)
        
    def get(self, request, page=1):
        get_data = self.params.get('get_data')
        title = {
            'video': 'Danh sách video',
            'page': 'Danh sách trang',
            'post': 'Danh sách bài đăng',
            None: 'Danh sách'
        }
        self.config_page_header(title[get_data.get('type')], button_params=[
            {'type': 'danger', 'text': 'Xoá', 'add_class': 'action-multi-items action-delete', 'attrs': {'data-bs-toggle': 'modal', 'data-bs-target': '#confirmDeleteModel'}},
            {'type': 'primary', 'text': 'Thêm', 'href': reverse_url('article.add')}
        ])
        self.params['form'] = ArticleSearchForm(get_data)
        self.params = {**self.params, **paginator(self.MODEL.list_item(get_data, {'task': 'list-item'}), {'page': page, **self.params})}
        return render(request, self.template, self.params)

    def post(self, request):
        return render(request, self.template, self.params)

# =========================================================================================================
class ArticleDeleteView(BaseDeleteView, ArticleView): pass