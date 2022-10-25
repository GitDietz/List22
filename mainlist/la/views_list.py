from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db import DatabaseError
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, Http404, redirect

from datetime import date
import logging
log = logging.getLogger("info_logger")
from .forms import NewListCreateForm
    # ItemForm, MerchantForm, ListGroupForm, UsersGroupsForm, NewGroupCreateForm, SupportLogForm
from .models import Item, Merchant, List, Support
# from listapp.utils import *
# Views related to the lists


################################# GROUP #################################
# @login_required
def user_lists(request):
    """
    lists associated with a user - as member or manager
    :param request:
    :return:
    """
    log.info(f'user = {request.user.username}')
    managed_list = List.objects.managed_by(request.user)
    member_list = List.objects.member_of(request.user)
    notice = ''
    context = {
        'title': 'Group List',
        'managed_list': managed_list,
        'member_list': member_list,
        'notice': notice,
    }
    return render(request, 'user_lists.html', context)


# @login_required
def list_detail(request, pk=None, list_obj=None):
    log.info(f'user = {request.user.username}| id = {pk}')
    if pk:
        list_obj = get_object_or_404(List, pk=pk)

    if request.method == "POST":
        form = NewListCreateForm(request.POST, instance=list_obj)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.name = form.cleaned_data['joining']
            new_list.purpose = form.cleaned_data['purpose']
            new_list.manager = request.user
            new_list.save()
            new_list.members.add(request.user)
            new_list.leaders.add(request.user)

            return HttpResponseRedirect(reverse('lists:user_list'))
        else:
            log.info(f'Form errors: {form.errors}')
    else:
        form = NewListCreateForm(instance=list_obj)  # will be none if new

    template_name = 'list.html'
    log.info(f'Outside Post section')
    context = {
        'title': 'Create or Update List',
        'form': form,
        'notice': '',
    }
    return render(request, template_name, context)
