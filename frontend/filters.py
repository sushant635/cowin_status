import django_filters
from .models import Employeeprofile


class EmployeeFilter(django_filters.FilterSet):
    class Meta:
        models = Employeeprofile

        fields = [
            'employee_branch',
            'employee_department',
            'gender'
            ]

