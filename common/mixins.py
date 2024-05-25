from shortuuidfield import ShortUUIDField
from typing import Any, Dict

from rest_framework.fields import get_attribute
from django_filters.rest_framework import DjangoFilterBackend

from django.core.exceptions import ObjectDoesNotExist

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


class BaseApiMixin:
    lookup_field = "idx"
    filter_backends = [DjangoFilterBackend]

    class Meta:
        abstract = True


class DetailRelatedField(serializers.RelatedField):
    """
    A custom related field for representing detailed related data.
    """

    def __init__(self, model: Any, **kwargs: Dict[str, Any]) -> None:
        """
        Initializes the BDetailRelatedField.
        Args:
        - model: The related model.
        - **kwargs: Additional keyword arguments.
        Keyword Args:
        - read_only: Indicates if the field is read-only.
        - lookup: The lookup field.
        - is_method: Indicates if the representation attribute is a method.
        - representation: The representation attribute.
        - source: The related object source.
        """

        if kwargs.get("write_only"):
            self.queryset = model.objects.all()
        else:
            kwargs["read_only"] = True
        self.lookup = kwargs.pop("lookup", None) or "idx"
        self.is_method = kwargs.pop("is_method", False)
        try:
            self.representation_attribute = kwargs.pop("representation")
            # If no source is present then it means that the value is directly accessible from the object.
            # Here source means the related object.
            # Also if source is absent then give representation as source to parent class as source is required
            # for the Related Field.
            """
            Example: if representation="user.name" then no need for source. but if representation="name" then
            need to pass source as "user"
            """
            self.no_source = False
            if not kwargs.get("source"):
                self.no_source = True
                kwargs["source"] = self.representation_attribute
        except KeyError:
            raise Exception("Please provide the representation attribute")
        super().__init__(**kwargs)

    def to_representation(self, obj: Any) -> Any:
        """
        Returns the serialized representation of the object.

        Args:
        - obj: The object to be serialized.

        Returns:
        - The serialized representation of the object.
        """
        if self.no_source:
            return obj
        if self.is_method:
            try:
                return get_attribute(obj, self.representation_attribute)()
            except AttributeError:
                return getattr(obj, self.representation_attribute)()
        return getattr(obj, self.representation_attribute)

    from typing import Any, TypeVar

    ModelType = TypeVar("ModelType")

    def to_internal_value(self, data: Any) -> ModelType:
        """
        Converts the external representation of data to the internal value.

        Args:
        - data: The external representation of the data.

        Returns:
        - The internal value of the data.
        """
        try:
            return self.queryset.get(**{self.lookup: data})
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Object does not exist")
