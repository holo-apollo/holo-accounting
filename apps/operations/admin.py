from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from admin_auto_filters.filters import AutocompleteFilter

from .models import Operation


class CounterpartyFilter(AutocompleteFilter):
    title = _('Counterparty')
    field_name = 'counterparty'


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ['counterparty', 'amount', 'time', 'is_reviewed']
    list_filter = [CounterpartyFilter, 'is_reviewed']
    readonly_fields = ['bank_id']
    raw_id_fields = ['order']
    autocomplete_fields = ['counterparty']

    # bug in django-admin-autocomplete-filter
    class Media:
        pass
