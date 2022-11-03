from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from django.utils.safestring import mark_safe
from .models import Item, Merchant, List, Support, ReferenceItem, Category


class NewListCreateForm(forms.ModelForm):
    """
    for existing members that want to create a new list
    """
    joining = forms.CharField(label='List to create', max_length=100)
    purpose = forms.CharField(label='What is this list for?', max_length=200)

    class Meta:
        model = List
        fields = ['joining', 'purpose']

    def clean(self):
        cleaned_data = super().clean()
        join = cleaned_data.get('joining', None)
        purp = cleaned_data.get('purpose', None)
        return cleaned_data

    def clean_joining(self):
        target_list = self.cleaned_data.get('joining')
        # now check that the group does not exists and create it, rather do this in the form
        qs_shop_group = List.objects.all()
        # TODO make this one step
        this_found = qs_shop_group.filter(Q(name__iexact=target_list))
        if this_found.exists():
            raise ValidationError('That list already exists, please enter another name')
        return target_list

    def clean_purpose(self):
        what_purpose = self.cleaned_data.get('purpose')
        print(f'purpose is {what_purpose}')
        if len(what_purpose) > 0:
            return what_purpose
        else:
            raise ValidationError("Purpose is required")
