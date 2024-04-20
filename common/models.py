from django.db import models


# Create your models here.
class BaseModelMixin(models.Model):
    idx = models.UUIDField(max_length=22)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_obsolete = models.BooleanField(default=True, db_index=True)

    class Meta:
        abstract = True
