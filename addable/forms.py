from django import forms

class Addable(forms.Select):
    template_name='addable/addable.html'

    class Media:
        js = ('addable/addable.js',)


class AddableMultiple(forms.SelectMultiple):
    template_name='addable/addable.html'

    class Media:
        js = ('addable/addable.js',)

class AdditionalInfo(forms.CheckboxSelectMultiple):
    template_name = 'addable/additional_info.html'
    input_type = 'hidden'





