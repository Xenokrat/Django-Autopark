import re

from rest_framework import serializers

from auto.models import Driver, Enterprise, Vehicle


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
            "mileage",
            "year",
            "color",
            "purchase_date",
        )

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
