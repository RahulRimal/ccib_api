from django.db import models

from shortuuidfield import ShortUUIDField


class BaseModelMixin(models.Model):
    idx = ShortUUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_obsolete = models.BooleanField(default=False, db_index=True)

    class Meta:
        abstract = True

