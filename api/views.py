from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from auto.models import Driver, Enterprise, Vehicle

from .serializers import DriverSerializer, EnterpriseSerializer, VehicleSerializer


@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def vehicle_list(request):
    if not (hasattr(request.user, "manager") or request.user.is_superuser):
        return Response({"message": "Пользователь не является менеджером"}, status=403)

    if request.method == "GET":
        if request.user.is_superuser:
            vehicles = Vehicle.objects.all()
        else:
            vehicles = Vehicle.objects.filter(enterprise__in=request.user.manager.enterprise.all())
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid():
            # TODO: validate vehicle from accessible enterprise
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def vehicle_detail(request, pk: int):
    if not (hasattr(request.user, "manager") or request.user.is_superuser):
        return Response({"message": "Пользователь не является менеджером"}, status=403)

    try:
        vehicle = Vehicle.objects.get(pk=pk)
    except Vehicle.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = VehicleSerializer(vehicle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        vehicle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def driver_list(request):
    if not (hasattr(request.user, "manager") or request.user.is_superuser):
        return Response({"message": "Пользователь не является менеджером"}, status=403)

    if request.method == "GET":
        if request.user.is_superuser:
            drivers = Driver.objects.all()
        else:
            drivers = Driver.objects.filter(enterprise__in=request.user.manager.enterprise.all())
        serializer = DriverSerializer(drivers, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = DriverSerializer(data=request.data)
        if serializer.is_valid():
            # TODO: validate vehicle from accessible enterprise
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def driver_detail(request, pk: int):
    if not (hasattr(request.user, "manager") or request.user.is_superuser):
        return Response({"message": "Пользователь не является менеджером"}, status=403)

    try:
        driver = Driver.objects.get(pk=pk)
    except Driver.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = DriverSerializer(driver)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = DriverSerializer(driver, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        driver.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def enterprise_list(request):
    if not hasattr(request.user, "manager"):
        return Response({"detail": "Пользователь не является менеджером"}, status=403)

    if request.user.is_superuser:
        enterprises = Enterprise.objects.all()
    else:
        enterprises = request.user.manager.enterprise.all()

    serializer = EnterpriseSerializer(enterprises, many=True)
    return Response(serializer.data)


def enterprise_detail(request):
    pass
