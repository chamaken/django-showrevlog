import io, os, re
import functools, tempfile

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from file_read_backwards import FileReadBackwards

import logging
logger = logging.getLogger(__name__)


_FILEXP = re.compile(settings.SHOWREVLOG_FILEXP)
_LINEXP = re.compile(settings.SHOWREVLOG_LINEXP)
COLNAMES = [t[0] for t in sorted(_LINEXP.groupindex.items(), key=lambda x: x[1])]


def logfiles(path=settings.SHOWREVLOG_DIR):
    return sorted([f
                   for _, _, files in os.walk(path)
                   for f in files
                   if os.access(os.path.join(path, f), os.R_OK) \
                   and _FILEXP.search(f) is not None])


class Logfile(models.Model):
    """Hack object to be added to Django admin"""
    class Meta:
        managed = False
        verbose_name = _('Log file')
        verbose_name_plural = _('Log files')


class LogfileReadBackwards(FileReadBackwards):
    """
    >>> with tempfile.NamedTemporaryFile() as tmpfile:
    ...     tmpfile.write(b'\\n'.join(reversed([b'%d' % i for i in range(20)]))) and 'tempfile created'
    ...     tmpfile.flush()
    ...     with LogfileReadBackwards(tmpfile.name) as lrb:
    ...         lrb.count()
    ...         lrb[0]
    ...         lrb[11]
    ...         lrb[4:9]
    'tempfile created'
    20
    '0'
    '11'
    ['4', '5', '6', '7', '8']
    """

    def __init__(self, path, encoding="utf-8", chunk_size=io.DEFAULT_BUFFER_SIZE):
        super(LogfileReadBackwards, self).__init__(path, encoding, chunk_size)
        self._count = functools.reduce(lambda x, _: x + 1, open(path, 'rb'), 0)
        self._index = 0
        self._iter = iter(self)


    def count(self):
        return self._count


    def __getitem__(self, key):
        if isinstance(key, slice): # not efficient? but easy :-)
            return [self[i] for i in range(*key.indices(self._count))]
        elif not isinstance(key, int):
            raise TypeError('indices must be integers or slices')
        if key < 0 or key >= self._count:
            raise IndexError('index out of range')

        if key < self._index:
            self._index = 0
            self._iter = iter(self)

        skip = key - self._index
        for _ in range(skip):
            next(self._iter)

        self._index = key + 1
        return next(self._iter)


class BackwardsLogfile(LogfileReadBackwards):
    def __getitem__(self, key):
        if isinstance(key, slice):
            return [self[i] for i in range(*key.indices(self._count))]
        elif not isinstance(key, int):
            raise TypeError('indices must be integers or slices')

        return super(BackwardsLogfile, self).__getitem__(key)


    def __iter__(self):
        for line in super(BackwardsLogfile, self).__iter__():
            ret = _LINEXP.findall(line)
            if not ret:
                ret = [[''] * len(COLNAMES)]
                ret[0][0] = _('(Exception?)')
                ret[0][-1] = line

            yield ret
