#!/usr/bin/env python3
""" Implementing filtering functionalities """

import django_filters


class CustomerFilter:
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')