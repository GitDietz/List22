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
# from .forms import ItemForm, MerchantForm, ListGroupForm, UsersGroupsForm, NewGroupCreateForm, SupportLogForm
from .models import Item, Merchant, List, Support
# from listapp.utils import *
# Views related to the lists


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
