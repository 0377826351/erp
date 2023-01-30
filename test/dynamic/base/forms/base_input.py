from django import forms

class BaseWidget(forms.Widget):
    default_class = 'form-control'

    def __init__(self, config={}, attrs=None):
        attrs = {} if attrs is None else attrs.copy()
        attrs['class'] = attrs['class'] + ' ' + self.default_class if 'class' in attrs else self.default_class

        self.config = {'box_class': 'col-12 col-md-4 col-xl-3', **config}
        super().__init__(attrs)
    
    def use_required_attribute(self, initial: None): 
        return False

class BaseTextInput(BaseWidget, forms.TextInput):
    pass

class BaseTextarea(BaseWidget, forms.Textarea):
    pass

class BaseNumberInput(BaseWidget, forms.NumberInput):
    pass

class BaseHiddenInput(BaseWidget, forms.HiddenInput):
    pass

class BasePasswordInput(BaseWidget, forms.PasswordInput):
    pass

class BaseFileInput(BaseWidget, forms.ClearableFileInput):
    pass

class BaseToggle(BaseWidget, forms.CheckboxInput):
    default_class = 'form-control'
    template_name = "form_control/toggle_input.html"
    pass

class BaseSelect(BaseWidget, forms.Select):
    default_class = 'form-control select2'
    pass


class BaseSelectMultiple(BaseWidget, forms.SelectMultiple):
    default_class = 'form-control select2'

    def __init__(self, config={}, attrs=None):
        attrs = {} if attrs is None else attrs.copy()
        attrs['class'] = attrs['class'] + ' ' + self.default_class if 'class' in attrs else self.default_class
        attrs['multiple'] = 1

        self.config = {'box_class': 'col-12 col-md-4 col-xl-3', **config}
        super().__init__(attrs)
    pass

class BaseBoolean(BaseWidget, forms.CheckboxInput):
    default_class = 'form-check-input'
    pass

class BaseCheckbox(BaseWidget, forms.CheckboxSelectMultiple):
    template_name = "form_control/multiple_input.html"
    default_class = 'form-check-input'
    pass

class BaseRadio(BaseWidget, forms.RadioSelect):
    template_name = "form_control/multiple_input.html"
    default_class = 'form-check-input'
    pass

class BaseImage(BaseWidget, forms.TextInput):
    default_class = "img-thumbnail rounded"
    template_name = "form_control/image.html"

class BaseAlbumImage(BaseWidget, forms.TextInput):
    default_class = "img-thumbnail rounded"
    template_name = "form_control/album_image.html"

class BaseVideo(BaseWidget, forms.TextInput):
    default_class = ""
    template_name = "form_control/video.html"
