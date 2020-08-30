import django_filters
from .models import Order
from django_filters import DateFilter


class OrderFilter(django_filters.FilterSet):
	start_date = DateFilter(field_name="date_created", lookup_expr="gte")
	class Meta:
		model = Order
		fields = '__all__'
		exclude = ['customer', 'date_created']