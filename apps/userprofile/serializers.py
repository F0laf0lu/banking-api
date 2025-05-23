import base64

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from apps.common.models import ContentView
from .models import Profile

User = get_user_model()


class UUIDField(serializers.Field):
    def to_representation(self, value: str) -> str:
        return str(value)
    

class ProfileSerializer(serializers.ModelSerializer):
    id = UUIDField(read_only=True)
    first_name = serializers.CharField(source="user.first_name")
    middle_name = serializers.CharField(
        source="user.middle_name", required=False, allow_blank=True
    )
    last_name = serializers.CharField(source="user.last_name")
    username = serializers.ReadOnlyField(source="user.username")
    email = serializers.EmailField(source="user.email", read_only=True)
    full_name = serializers.ReadOnlyField(source="user.full_name")
    id_no = serializers.ReadOnlyField(source="user.id_no")
    date_joined = serializers.DateTimeField(source="user.date_joined", read_only=True)
    country = CountryField(name_only=True)
    phone_number = PhoneNumberField()
    view_count = serializers.SerializerMethodField()


    class Meta:
        model = Profile
        fields = [
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "username",
            "id_no",
            "email",
            "full_name",
            "date_joined",
            "gender",
            "date_of_birth",
            "marital_status",
            "phone_number",
            "address",
            "city",
            "country",
            "employment_status",
            "employer_name",
            "annual_income",
            "date_of_employment",
            "employer_address",
            "employer_city",
            "employer_state",
            "created_at",
            "updated_at",
            "view_count"
        ]

        read_only_fields = [
            "user",
            "id",
            "username",
            "email",
            "created_at",
            "updated_at",
        ]
    

    def get_view_count(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return ContentView.objects.filter(
            content_type=content_type, object_id=obj.id
        ).count()
    
    def update(self, instance: Profile, validated_data: dict) -> Profile:
        user_data = validated_data.pop("user", {})

        if user_data:
            for attr, value in user_data.items():
                if attr not in ["email", "username"]:
                    setattr(instance.user, attr, value)
            instance.user.save()
        instance.save()
        return instance


class ProfileListSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField(source="user.full_name")
    username = serializers.ReadOnlyField(source="user.username")
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "full_name",
            "username",
            "gender",
            "email",
            "phone_number",
        ]