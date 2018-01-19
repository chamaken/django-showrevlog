from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ShowRevLogConfig(AppConfig):
    name = 'showrevlog'
    verbose_name = _('Show logfile in reverse order')
