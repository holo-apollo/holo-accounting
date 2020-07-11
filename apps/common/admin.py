from abc import ABCMeta

from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

admin.site.unregister(Group)


class BooleanSimpleFilter(admin.SimpleListFilter, metaclass=ABCMeta):
    def lookups(self, request, model_admin):
        return (
            ('Yes', _('Yes')),
            ('No', _('No')),
        )
