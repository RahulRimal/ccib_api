from common.filterbackend import IdxFilterBackend

class BaseApiMixin:
    lookup_field = "idx"
    filter_backends = [IdxFilterBackend]

    class Meta:
        abstract = True