import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from base.helpers import querydict_to_dict


class BaseView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        self.params = self.config_params()

        if request.GET:
            self.params['get_data'] = {**self.params['get_data'], **querydict_to_dict(request.GET)}
                
        if request.POST: 
            self.params['post_data'] = {**self.params['post_data'], **querydict_to_dict(request.POST)}
            self.params['post_data'].update({'updated_by': request.user.id})
            if not self.params['post_data'].get('id'): self.params['post_data'].update({'created_by': request.user.id})
        self.init(request)
        return super().dispatch(request, *args, **kwargs)

    def init(self, request):
        pass

    def set_template(self, html_file):
        self.template = self.TEMPLATE_PATH + html_file

    def set_page_title(self, title):
        pass
        
    def config_params(self):
        return {
            'get_data': {},
            'post_data': {}
        }
    
    def config_page_header(self, title="Title", module_name=None, button_params=[]):
        """ title = 'page title' """
        title = '%s - %s' % (self.MODULE_NAME, title) if not module_name else '%s - %s' % (module_name, title)
        self.params['config_page_header'] = {'title': title, 'button_params': button_params}

class BaseListView(BaseView):
    def config_params(self):
        return {
            'pagination': {
                'per_page_options': [20,50,100,200,500],
                'on_each_side': 2,
                'on_ends': 1,
            },
            'get_data': {
                'per_page': 20
            },
            'post_data': {}
        }

class BaseDeleteView(BaseView):

    def init(self, request):
        return super().init(request)

    def post(self, request):
        items_delete = json.loads(request.body).get('items_delete') or request.POST.get('items_delete')
        if not items_delete:
            return JsonResponse({'status': 'error', 'message': 'Có lỗi xảy ra!'})
        ret = self.MODEL.delete_item_by_ids(items_delete)
        if not ret:
            return JsonResponse({'status': 'error', 'message': 'Có lỗi xảy ra!'})
        return JsonResponse({'status': 'success', 'message': 'Xoá %s bản ghi thành công!' % len(items_delete)})