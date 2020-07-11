from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from admin_auto_filters.filters import AutocompleteFilter

from apps.common.admin import BooleanSimpleFilter
from apps.operations.models import Operation
from .models import Order, OrderItem


class CounterpartyFilter(AutocompleteFilter):
    title = _('counterparty')
    field_name = 'counterparty'


class IsCompletedFilter(BooleanSimpleFilter):
    title = _('completed')
    parameter_name = 'is_completed'

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(completed_at__isnull=False)
        if value == 'No':
            return queryset.filter(completed_at__isnull=True)


class IsDeliveredFilter(BooleanSimpleFilter):
    title = _('delivered')
    parameter_name = 'is_delivered'

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(delivered_at__isnull=False)
        if value == 'No':
            return queryset.filter(delivered_at__isnull=True)


class IsOverdueFilter(BooleanSimpleFilter):
    title = _('overdue')
    parameter_name = 'is_overdue'

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.overdue()
        if value == 'No':
            return queryset.non_overdue()


class AmountDueFilter(BooleanSimpleFilter):
    title = _('having amount due')
    parameter_name = 'has_amount_due'

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.with_amount_due()
        if value == 'No':
            return queryset.without_amount_due()


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['product', 'product_quantity', 'total_value']
    autocomplete_fields = ['product']
    extra = 1


class OperationInline(admin.TabularInline):
    model = Operation
    fields = ['amount', 'time', 'is_reviewed']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['counterparty', 'created_at', 'completed_at', 'delivered_at', 'deadline',
                    'time_overdue', 'total_value', 'total_paid', 'amount_due']
    list_filter = [CounterpartyFilter, IsCompletedFilter, IsDeliveredFilter, IsOverdueFilter,
                   AmountDueFilter]
    autocomplete_fields = ['counterparty']
    inlines = [OrderItemInline, OperationInline]
    readonly_fields = ['time_overdue', 'total_value', 'total_paid', 'amount_due']

    # bug in django-admin-autocomplete-filter
    class Media:
        pass
