# !/usr/bin/env python
# _*_ coding: utf-8 _*_

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.http import Http404


class StaffRequiredMixin(object):

    @classmethod
    def as_view(self, *args, **kwargs):
        view = super(StaffRequiredMixin, self).as_view(*args, **kwargs)
        # return login_required(view)
        return staff_member_required(view)

    @method_decorator(login_required)
    def dispath(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super(StaffRequiredMixin, self).dispath(*args, **kwargs)
        else:
            return Http404


class LoginRequiredMixin(object):

    @classmethod
    def as_view(self, *args, **kwargs):
        view = super(LoginRequiredMixin, self).as_view(*args, **kwargs)
        return login_required(view)

    @method_decorator(login_required)
    def dispath(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispath(*args, **kwargs)
