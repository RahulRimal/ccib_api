from django_filters import FilterSet
from django.db import models

from django_filters.filterset import ModelChoiceFilter, remote_queryset, FILTER_FOR_DBFIELD_DEFAULTS
from django_filters.rest_framework import DjangoFilterBackend



FILTER_FOR_DBFIELD_DEFAULTS[models.OneToOneField] = {
	'filter_class': ModelChoiceFilter,
	'extra': lambda f: {
		'queryset': remote_queryset(f),
		'to_field_name': "idx",
	}
}

FILTER_FOR_DBFIELD_DEFAULTS[models.ForeignKey] = {
	'filter_class': ModelChoiceFilter,
	'extra': lambda f: {
		'queryset': remote_queryset(f),
		'to_field_name': "idx",
	}
}


class CCIBFilterSet(FilterSet):
    FILTER_DEFAULTS = FILTER_FOR_DBFIELD_DEFAULTS


class IdxFilterBackend(DjangoFilterBackend):
    filterset_base = CCIBFilterSet


