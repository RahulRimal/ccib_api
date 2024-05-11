from shortuuidfield import ShortUUIDField

from rest_framework import serializers

class BaseModelSerializerMixin(serializers.ModelSerializer):
    idx = ShortUUIDField()

    class Meta:

        exclude = ("id", "modified_at", "is_obsolete")
        extra_kwargs = {
            "created_at": {"read_only": True},
            "modified_at": {"read_only": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for field_name, field in self.fields.items():
            if isinstance(field, serializers.PrimaryKeyRelatedField):
                related_instance = getattr(instance, field_name)
                if not related_instance:
                    continue
                representation[field_name] = getattr(
                    related_instance, "idx", related_instance.id
                )
            if isinstance(field, serializers.ManyRelatedField):
                related_instances = getattr(instance, field_name).all()
                representation[field_name] = [
                    getattr(related_instance, "idx", related_instance.id)
                    for related_instance in related_instances
                ]
        return representation


class BaseApiMixin():
    lookup_field = "idx"

    class Meta:
        abstract = True



