import os, csv

from django.conf import settings
from django.contrib.admin.views.main import PAGE_VAR
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.utils.safestring import mark_safe

from . import models

import logging
logger = logging.getLogger(__name__)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def index(request, template_name):
    """Lists Log Files in settings directory"""
    files = [(str(i), s) for i, s in enumerate(models.logfiles())]
    return render(request, template_name, {'files': files})


class PageForAdmin(object):
    """Dirty hack to be a django.admin.views.main.ChangeList
    """
    def __init__(self, page, page_num):
        self._page = page
        self.page_num = page_num
        self.show_all = False
        self.can_show_all = False
        self.multi_page = page.paginator.count > page_num


    def get_query_string(self, s):
        # s: {PAGE_VAR: i}
        return mark_safe('?p=%(p)s' % s)


    def __getattr__(self, attr):
        return getattr(self._page, attr)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def show(request, logfile_id, template_name):
    try: page_num = int(request.GET.get(PAGE_VAR, '0'))
    except ValueError: page_num = 0

    logfiles = models.logfiles()
    try: fname = logfiles[int(logfile_id)]
    except Exception: return HttpResponseBadRequest()

    paginator = Paginator(
        models.BackwardsLogfile(os.path.join(settings.SHOWREVLOG_DIR, fname)),
        settings.SHOWREVLOG_PER_PAGE)
    page = paginator.page(page_num + 1)
    context = {
        'header': models.COLNAMES,
        'fname': fname,
        'fid': logfile_id,
        'page': PageForAdmin(page, page_num),
    }
    return render(request, template_name, context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def as_csv(request, logfile_id):
    logfiles = models.logfiles()
    try: fname = logfiles[int(logfile_id)]
    except Exception: return HttpResponseBadRequest()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % fname
    writer = csv.writer(response)
    writer.writerow(models.COLNAMES)
    with models.BackwardsLogfile(os.path.join(settings.SHOWREVLOG_DIR, fname)) as blf:
        for l in blf:
            writer.writerow(*l)

    return response
