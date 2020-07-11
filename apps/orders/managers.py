from django.db.models import F, OuterRef, Q, QuerySet, Subquery, Sum
from django.utils import timezone


class OrderQuerySet(QuerySet):
    def overdue(self):
        # not delivered and have deadline and deadline is in the past
        return self.filter(delivered_at__isnull=True, deadline__isnull=False,
                           deadline__lt=timezone.now())

    def non_overdue(self):
        return self.filter(
            Q(delivered_at__isnull=False) |  # already delivered or
            Q(deadline__isnull=True) |  # have no deadline or
            Q(deadline__gte=timezone.now())  # deadline is in the future
        )

    def annotated_with_totals(self):
        from apps.operations.models import Operation
        from apps.orders.models import OrderItem
        order_items = OrderItem.objects.filter(order=OuterRef('pk')).order_by().values('order')
        total_order_items = order_items.annotate(total=Sum('total_value')).values('total')
        operations = Operation.objects.filter(order=OuterRef('pk')).order_by().values('order')
        total_operations = operations.annotate(total=Sum('amount')).values('total')
        return self.annotate(
            prepared_total_value=Subquery(total_order_items),
            prepared_total_paid=Subquery(total_operations)
        )

    def with_amount_due(self):
        # completed, has some value and nothing paid or paid less than value
        return self.annotated_with_totals().filter(
            completed_at__isnull=False,
            prepared_total_value__isnull=False
        ).filter(
            Q(prepared_total_paid__isnull=True) |
            Q(prepared_total_paid__lt=F('prepared_total_value'))
        )

    def without_amount_due(self):
        # incomplete or has no value or paid more or equal than paid
        return self.annotated_with_totals().filter(
            Q(completed_at__isnull=True) |
            Q(prepared_total_value__isnull=True) |
            Q(prepared_total_paid__isnull=False,
              prepared_total_paid__gte=F('prepared_total_value'))
        )


OrderManager = OrderQuerySet.as_manager
