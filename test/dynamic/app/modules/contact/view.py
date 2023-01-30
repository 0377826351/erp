from django.shortcuts import render, redirect
from django.contrib import messages

from base.helpers import paginator, reverse_url
from base.views import BaseDeleteView, BaseView, BaseListView
from .form import ContactForm, ContactFormSearch
from .model import Contact

# =========================================================================================================
class ContactView(BaseView):
    MODULE_NAME = 'Contact'
    URL_NAME = 'contact'
    TEMPLATE_PATH = 'contact/'
    
    def init(self, request):
        self.MODEL = Contact
        self.params['url_name'] = self.URL_NAME
        return super().init(request)

# =========================================================================================================
class ContactListView(BaseListView, ContactView):
    def init(self, request):
        self.set_template('list.html')
        self.config_page_header('Danh sách', button_params=[
            {'type': 'danger', 'text': 'Xoá', 'add_class': 'action-multi-items action-delete', 'attrs': {'data-bs-toggle': 'modal', 'data-bs-target': '#confirmDeleteModel'}},
            {'type': 'primary', 'text': 'Thêm', 'href': reverse_url('contact.add')}
        ])
        return super().init(request)

    def get(self, request, page=1):
        self.params['form'] = ContactFormSearch(self.params.get('get_data'))
        print(self.params)
        # Paginator
        self.params = {**self.params, **paginator(self.MODEL.list_item(self.params.get('get_data'), {'task': 'list-item'}), {'page': page, **self.params})}
        # End paginator
        return render(request, self.template, self.params)

    def post(self, request):
        pass

class ContactFormView(ContactView):
    def init(self, request):
        self.set_template('form.html')
        self.config_page_header('Tạo mới',button_params = [
            {'type':'submit','text':'Lưu'},
            {'text':'Quay Lại','href':reverse_url('contact')}
        ])
        return super().init(request)

    def get(self, request,id=None):
        item = self.MODEL.get_item_by_id(id) if id else None
        self.params['form'] = ContactForm(item.__dict__ if item else None)
        return render(request, self.template, self.params)

    def post(self, request,id=None):
        task = "change" if id else 'add'
        post_data = self.params.get("post_data") or None
        form =ContactForm(post_data)
        if form.is_valid():
            result = self.MODEL.save_item(post_data, {'task': task, 'make_pass': 'custom'})
            print(result)
            if result:
                messages.add_message(request,messages.SUCCESS,"Thêm bản ghi thành công" if task == 'add' else "Cập nhật bản ghi thành công")
                return redirect(self.URL_NAME)
            self.params['errors'] = form.errors
            self.params['form'] = form
        return render(request, self.template, self.params)
 
# =========================================================================================================
class ContactDeleteView(BaseDeleteView, ContactView): pass
