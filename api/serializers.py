import re

import pytz
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework_gis.fields import GeometryField
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from auto.models import AutoRide, Driver, Enterprise, GPSData, Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = (
            "model",
            "registration_number",
            "VIN",
            "current_driver",
            "enterprise",
            "cost",
            "mileage" "year",
            "color",
            "purchase_date",
        )

    def to_representation(self, instance):
        # tz = timezone.get_current_timezone_name()
        # if tz:
        #     self.fields["purchase_date"] = serializers.DateTimeField(default_timezone=pytz.timezone(tz))
        # else:
        self.fields["purchase_date"] = serializers.DateTimeField(
            default_timezone=pytz.timezone(instance.enterprise.timezone)
        )
        return super().to_representation(instance)

    def validate(self, data):
        regex = "^\w*$"
        VIN = data["VIN"]
        if len(VIN) != 17 or not re.search(regex, VIN):
            raise serializers.ValidationError(
                "Идентификатор VIN должен состоять из 17 символов, включая только буквы и цифры"
            )
        reg_number = data["registration_number"]
        if not re.search(regex, reg_number):
            raise ValidationError("Номер регистрации должен состоять только из цифр и букв")

        return data


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = (
            "first_name",
            "second_name",
            "salary",
            "driving_experience",
            "enterprise",
            "vehicle",
        )


class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = (
            "name",
            "city",
        )


class GPSDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPSData
        fields = ("id", "vehicle", "point", "timestamp")

    def to_representation(self, instance):
        self.fields["timestamp"] = serializers.DateTimeField(
            default_timezone=pytz.timezone(instance.vehicle.enterprise.timezone)
        )
        return super().to_representation(instance)


class GPSDataSerializerGEOJson(GeoFeatureModelSerializer):
    class Meta:
        model = GPSData
        geo_field = "point"
        fields = ("id", "vehicle", "timestamp")

    def to_representation(self, instance):
        self.fields["timestamp"] = serializers.DateTimeField(
            default_timezone=pytz.timezone(instance.vehicle.enterprise.timezone)
        )
        self.fields["point"] = GeometryField()


class AutoRidesSerializer(serializers.ModelSerializer):
    start_address = serializers.SerializerMethodField()
    end_address = serializers.SerializerMethodField()

    def get_start_address(self, obj):
        return str(obj.get_start_address())

    def get_end_address(self, obj):
        return str(obj.get_end_address())

    class Meta:
        model = AutoRide
        fields = (
            "id",
            "vehicle",
            "start_date",
            "end_date",
            "start_address",
            "end_address",
        )

    def to_representation(self, instance):
        self.fields["start_date"] = serializers.DateTimeField(
            default_timezone=pytz.timezone(instance.vehicle.enterprise.timezone)
        )
        self.fields["end_date"] = serializers.DateTimeField(
            default_timezone=pytz.timezone(instance.vehicle.enterprise.timezone)
        )
        self.fields["start_point"] = GeometryField()
        self.fields["end_point"] = GeometryField()
        return super().to_representation(instance)
