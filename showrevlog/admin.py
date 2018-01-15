from django.contrib import admin
from .models import Logfile


class LogfileAdmin(admin.ModelAdmin):
    def has_add_permission(self, request): return False
    def has_change_permission(self, request): return False
    # def has_delete_permission(self, request): return False

admin.site.register(Logfile, LogfileAdmin)
