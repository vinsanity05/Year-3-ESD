from dataclasses import field
from logging import Filter
from .models import *
import django_filters 
from django_filters import DateFilter, DateRangeFilter
from django_filters.widgets import RangeWidget

class transactionFilters(django_filters.FilterSet):
    #start_date = DateFilter(field_name="date", lookup_expr="gte")
    date = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))
    #end_date = DateFilter(field_name='date', lookup_expr="lte")
    date_range = DateRangeFilter(field_name='date')
    class Meta:
        model = Transaction
        fields = '__all__'
        exclude = ['date', 'representative', 'amount', 'booking']

class validate(django_filters.FilterSet):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['user', 'balance']


class settleFilters(django_filters.FilterSet):
    date_range = DateRangeFilter(field_name='date')
    class Meta:
        model = Transaction
        fields = '__all__'
        exclude = ['date', 'representative', 'amount', 'booking', 'account']