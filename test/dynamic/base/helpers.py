import os
import random
import string
import time
import hashlib
import logging
from PIL import Image, ImageOps
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from django.apps import apps
from django import urls


logger = logging.getLogger(__name__)

# ==================================================================================================================
class HanlderFile:
    def get_file_extension_allow(type):
        CONST = {
            'images': {
                'image/jpg': 'jpg', 
                'image/png': 'png', 
                'image/jpeg': 'jpeg',
                'image/gif': 'gif'
            },
            'files': {
                # audio
                'audio/mpeg': 'mp3',
                # video
                'video/mp4': 'mp4', 
                'video/mov': 'mov', 
                'video/wmv': 'wmv', 
                'video/avi': 'avi', 
                # word
                # pdf
                # ....
            },
        }
        CONST.update({'all': {**CONST['images'], **CONST['files']}})
        return CONST[type]

    def gen_file_name(extension):
        MIN_RANDOM = 0
        MAX_RANDOM = 99999999999
        file_name = '{random_number}_{timestamp}.{extension}'.format(random_number=random.randint(MIN_RANDOM,MAX_RANDOM), timestamp=int(time.time()), extension=extension)
        return file_name

    def validate_file_input(file, type='all', required=False, max_size=0):
        if type not in ('images', 'files', 'all'):
            return 'Type params not valid!'
        extension_allow = HanlderFile.get_file_extension_allow(type)
        # Check:
        if not file and required:
            return 'File rỗng'
        if file.content_type not in extension_allow.keys():
            return 'File %s không hợn lệ. Chỉ cho phép định dạng %s' % (file.name, ', '.join(extension_allow.values()))
        if max_size > 0 and file.size > max_size:
            return 'Dung lượng file lơn hơn %s bytes!' % max_size
        return True

    def validate_multi_file_input(list_files, required=False, max_size=0):
        for file in list_files:
            message = HanlderFile.validate_file_input(file, required=required, max_size=max_size)
            if message != True: return message
        return True

    def upload_image(file, parent_folder, allow_size={'small': True, 'medium': True, 'large': True, 'full': True}, type='crop'):
        # Config
        SIZE_CONFIG = {
            'small': (150, 150), 
            'medium': (300, 300),
            'large': (600, 600),
            'full': None
        }
        EXTENSION_ALLOW = HanlderFile.get_file_extension_allow('images')

        # Validate
        if type not in ('crop', 'resize'):
            raise Exception("Type muse be `crop` or `resize`!")

        # Upload image:
        extension = EXTENSION_ALLOW[file.content_type]
        image_name = HanlderFile.gen_file_name(extension)
        for key in SIZE_CONFIG:
            if not allow_size.get(key): continue
            size = SIZE_CONFIG[key]
            try:
                location = 'media/images/%s/%s' % (key, parent_folder)
                if not os.path.exists(location): os.makedirs(location)
                img = Image.open(file)
                img = ImageOps.exif_transpose(img) # chống xoay ảnh
                if key != 'full':
                    if type == 'crop':
                        img = ImageOps.fit(img, size, Image.ANTIALIAS)
                    if type == 'resize':
                        img = img.resize(size)
                img.convert('RGB')
                location += '/' + image_name
                img.save(location, extension)
            except Exception as e:
                message.update({'error': str(e)})
                return message
        message = {'dir': parent_folder + '/' + image_name}
        return message

    def upload_file(file, parent_folder):
        EXTENSION_ALLOW = HanlderFile.get_file_extension_allow('files')
        location = 'media/files/%s' % parent_folder
        try:
            fs = FileSystemStorage(location=location)
            extension = EXTENSION_ALLOW[file.content_type]
            file_name = HanlderFile.gen_file_name(extension)
            fs.save(file_name, file)
            file_name = '%s/%s' % (parent_folder, file_name)
            message = {'dir': file_name}
        except Exception as e:
            logger.error(e)
            return {'error': str(e)}
        return message

    def upload_multi_file(list_file, parent_folder):
        # Upload:
        image_extension = HanlderFile.get_file_extension_allow('images')
        file_extension = HanlderFile.get_file_extension_allow('files')
        image_dir_list = []
        file_dir_list = []
        try:
            for file in list_file:
                if image_extension.get(file.content_type):
                    message_img_upload = HanlderFile.upload_image(file, parent_folder)
                    image_dir_list.append(message_img_upload['dir'])
                if file_extension.get(file.content_type):
                    message_file_upload = HanlderFile.upload_file(file, parent_folder)
                    file_dir_list.append(message_file_upload['dir'])
        except Exception as e:
            logger.error(str(e))
            return {'error': 'Lỗi hệ thống %s' % e}

        message = {'dir': {}}
        if not image_dir_list and not file_dir_list: return {'error': 'File trống!'}
        if image_dir_list: message['dir'].update({'images': image_dir_list})
        if file_dir_list: message['dir'].update({'files': file_dir_list})
        return message
            
    def delete_file(file_dir):
        try:
            if os.path.exists(file_dir):
                os.remove(file_dir)
            return True
        except Exception as e:
            logger.error(str(e))
            return False

    def delete_image(image_name, options=['full', 'large', 'medium', 'small']):
        if not options:
            return False
        for item in options:
            file_dir = "media/images/{}/{}".format(item, image_name)
            if os.path.exists(file_dir):
                try:
                    HanlderFile.delete_file(file_dir)
                except Exception as e:
                    logger.error(str(e))
                    return False
            else:
                return False
        return True

# ==================================================    O T H E R   ==================================================
def reverse_url(url_name, args=[], url_params={}):
    url = urls.reverse(url_name, args=args)
    if url_params:
        params = ''
        for key in url_params:
            value = url_params[key]
            params += '?{}={}'.format(key, value)
        url += params
    return url

def is_path(path):
    return path and '/' in path

def make_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

def paginator(queryset, params):
    page = params.get('page')
    get_data = params.get('get_data')
    pagination = params.get('pagination')
    items = Paginator(queryset, get_data.get('per_page', 20))
    if page > items.num_pages: page = items.num_pages
    return {
        'items': items.get_page(page),
        'page_range': items.get_elided_page_range(number=page, on_each_side=pagination.get('on_each_side'), on_ends=pagination.get('on_ends'))
    }

def uuid():
    return str(int(time.time())) + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(12))

def dict_to_list_tuple(dict, addition=None):
    ret = list(dict.items())
    if addition and isinstance(addition, list):
        for item in addition:
            if isinstance(item, tuple) and len(item) == 2:
                ret.append(item)
    return ret

def querydict_to_dict(querydict):
    if not querydict: 
        return querydict
    data = dict(querydict)
    for key in data:
        if len(data[key]) == 1: data[key] = data[key][0]
    return data

def model_to_dict(instance, fields=None, exclude=None, get_editable=True):
    from itertools import chain
    """
    Return a dict containing the data in ``instance`` suitable for passing as
    a Form's ``initial`` keyword argument.

    ``fields`` is an optional list of field names. If provided, return only the
    named.

    ``exclude`` is an optional list of field names. If provided, exclude the
    named from the returned dict, even if they are listed in the ``fields``
    argument.
    """
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        if not getattr(f, "editable", False) and not get_editable:
            continue
        if fields is not None and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        data[f.name] = f.value_from_object(instance)
    return data