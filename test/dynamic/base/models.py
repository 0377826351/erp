from django.db.models import Q
from django.contrib.auth.hashers import make_password
from base.helpers import make_pass


class BaseModel():
    def __str__(self):
        return self.name
        
    @property
    @classmethod
    def auto_integer(cls):
        counter = cls.objects.count()
        return 1 if not counter else counter + 1

    @classmethod
    def get_item_by_id(cls, id):
        result = None
        try: result = cls.objects.get(id=id) 
        except Exception : pass
        return result

    @classmethod
    def save_item(cls, params={}, options={}):
        model = item = None
        if options.get('task') == 'add':
            try:
                data = {}
                m2m_fields = {}
                for field in cls._meta.get_fields():
                    value = params.get(field.name)
                    if not value: continue
                    if field.get_internal_type() == 'ForeignKey':
                        key = cls._meta.get_field(field.name).foreign_related_fields[0].name
                        data.update({field.name: field.remote_field.model.objects.get(Q(**{key: value}))})
                    elif field.get_internal_type() == 'ManyToManyField':
                        list_instances = []
                        for pk in value:
                            instance = field.remote_field.model.objects.get(pk=pk)
                            list_instances.append(instance)
                        m2m_fields.update({field.name: list_instances})
                    elif field.name in ['password']:
                        if not value: continue
                        if options.get('make_pass') == 'custom':
                            data.update({field.name: make_pass(value)})
                        else:
                            data.update({field.name: make_password(value)})
                    else:
                        data.update({field.name: value})
                model = cls(**data)
                model.save()
            except Exception as inst:
                print('[Create Record Error] ', inst)
                return None
            return model

        if options.get('task') == 'change':
            try:
                item = cls.objects.get(id=params.get('id'))
                for field in cls._meta.get_fields():
                    print(field.name)
                    if field.name == 'id' or field.name not in params: continue
                    value = params[field.name] or None
                    if field.get_internal_type() == 'ForeignKey' and value:
                        key = cls._meta.get_field(field.name).foreign_related_fields[0].name
                        value = field.remote_field.model.objects.get(Q(**{key: value}))
                    elif field.name in ['password']:
                        if not params[field.name]: continue
                        if options.get('make_pass') == 'custom':
                            value = make_pass(params[field.name])
                        else:
                            value = make_password(params[field.name])
                    setattr(item, field.name, value)
                item.save()
            except Exception as inst:
                print('[Edit Record Error] ', inst)
                return None
            return item

    @classmethod
    def delete_item_by_ids(cls, ids):
        try: 
            for id in ids: cls.objects.get(id=id).delete()
            return True
        except Exception as inst:
            print('[Delete Record Error] ', inst)
            return False
