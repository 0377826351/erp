from django.shortcuts import render, redirect
from django.contrib import messages

from base.helpers import paginator, reverse_url
from base.views import BaseView, BaseListView
from .form import UserForm, UserFormSearch
from .model import User

# =========================================================================================================
class UserView(BaseView):
    MODULE_NAME = 'Người dùng'
    URL_NAME = 'user'
    TEMPLATE_PATH = 'user/'
    
    def init(self, request):
        self.MODEL = User
        self.params['url_name'] = self.URL_NAME
        return super().init(request)

# =========================================================================================================
class UserListView(BaseListView, UserView):
    def init(self, request):
        self.set_template('list.html')
        self.config_page_header('Danh sách', button_params=[{'type': 'primary', 'text': 'Thêm', 'href': reverse_url('user.add')}])
        return super().init(request)

    def get(self, request, page=1):
        self.params['form'] = UserFormSearch(self.params.get('get_data'))
        # Paginator
        self.params = {**self.params, **paginator(self.MODEL.list_item(self.params.get('get_data'), {'task': 'list-item'}), {'page': page, **self.params})}
        # End paginator
        return render(request, self.template, self.params)

    def post(self, request):
        pass

class UserFormView(UserView):
    def init(self, request, id=None):
        self.set_template('form.html')
        title = 'Cập nhật' if id else 'Thêm mới'
        self.config_page_header(title, button_params=[
            {'text': 'Quay lại', 'href': reverse_url('user')},
            {'type': 'submit', 'text': 'Lưu'}
        ])          
        return super().init(request)

    def get(self, request, id=None):
        item = self.MODEL.get_item_by_id(id) if id else None
        self.params['form'] = UserForm(item.__dict__ if item else None)
        return render(request, self.template, self.params)

    def post(self, request, id=None):
        task = 'change' if id else 'add'
        post_data = self.params.get('post_data')
        form = UserForm(post_data)
        if form.is_valid():
            result = self.MODEL.save_item(post_data, {'task': task})
            if result:
                messages.add_message(request, messages.SUCCESS, 'Thêm bản ghi thành công.' if task == 'add' else 'Cập nhật bản ghi thành công.')
                return redirect(self.URL_NAME)
        self.params['form'] = form
        return render(request, self.template, self.params)

class UserDeleteView(UserView):
    def get(self, request, id=None):
        if not id: 
            messages.add_message(request, messages.ERROR, 'Không tìm thấy bản ghi cần xoá.')
            return redirect(self.URL_NAME)
        res = self.MODEL.delete_item_by_ids([id])
        if res:
            messages.add_message(request, messages.SUCCESS, 'Xoá bản ghi thành công.')
        else:
            messages.add_message(request, messages.ERROR, 'Xoá bản ghi không thành công.')
        return redirect(self.URL_NAME)