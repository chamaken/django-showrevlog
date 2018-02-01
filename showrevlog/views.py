import os, csv

from django.conf import settings
from django.contrib import admin
from django.contrib.admin.views.main import PAGE_VAR
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from . import models

import logging
logger = logging.getLogger(__name__)


@login_required(login_url=reverse_lazy('admin:login'))
@user_passes_test(lambda u: u.is_superuser)
def index(request, template_name):
    """Lists Log Files in settings directory"""
    files = [(str(i), s) for i, s in enumerate(models.logfiles())]
    return render(request, template_name, {
        'files': files,
        'site_title': admin.site.site_title,
        'site_header': admin.site.site_header,
    })


class PageForAdmin(object):
    """Dirty hack to be a django.admin.views.main.ChangeList
    """
    def __init__(self, page, page_num):
        self._page = page
        self.page_num = page_num
        self.show_all = False
        self.can_show_all = False
        self.multi_page = page.paginator.count > page.paginator.per_page
        self.result_count = page.paginator.count
        self.opts = {
            'verbose_name': _('Line'),
            'verbose_name_plural': _('Lines'),
        }


    def get_query_string(self, s):
        # s: {PAGE_VAR: i}
        return mark_safe('?p=%(p)s' % s)


    def __getattr__(self, attr):
        return getattr(self._page, attr)


@login_required(login_url=reverse_lazy('admin:login'))
@user_passes_test(lambda u: u.is_superuser)
def show(request, logfile_id, template_name):
    try: page_num = int(request.GET.get(PAGE_VAR, '0'))
    except ValueError: page_num = 0

    logfiles = models.logfiles()
    try: fname = logfiles[int(logfile_id)]
    except Exception: return HttpResponseBadRequest()

    paginator = Paginator(
        models.BackwardsLogfile(fname),
        settings.SHOWREVLOG_PER_PAGE)
    page = paginator.page(page_num + 1)
    context = {
        'header': models.COLNAMES,
        'fname': fname,
        'fid': logfile_id,
        'page': PageForAdmin(page, page_num),
        'site_title': admin.site.site_title,
        'site_header': admin.site.site_header,
    }
    return render(request, template_name, context)


@login_required(login_url=reverse_lazy('admin:login'))
@user_passes_test(lambda u: u.is_superuser)
def as_csv(request, logfile_id):
    logfiles = models.logfiles()
    try: fname = logfiles[int(logfile_id)]
    except Exception: return HttpResponseBadRequest()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % fname
    writer = csv.writer(response)
    writer.writerow(models.COLNAMES)
    with models.BackwardsLogfile(fname) as blf:
        for l in blf:
            writer.writerow(*l)

    return response
