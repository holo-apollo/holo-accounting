from django.contrib import admin

from .models import Counterparty, CounterpartyBankAlias


class CounterpartyBankAliasInline(admin.TabularInline):
    model = CounterpartyBankAlias
    fields = ['alias']
    extra = 0


@admin.register(Counterparty)
class CounterpartyAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_reviewed']
    search_fields = ['name']
    list_filter = ['is_reviewed']
    inlines = [CounterpartyBankAliasInline]
