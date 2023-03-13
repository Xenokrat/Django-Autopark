from rest_framework import status
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from auto.models import Driver, Enterprise, GPSData, Vehicle

from .serializers import (DriverSerializer, EnterpriseSerializer,
                          GPSDataSerializer, VehicleSerializer)


@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def vehicle_list(request):
    paginator = PageNumberPagination()
    paginator.page_size = 30

    if not (hasattr(request.user, "manager") or request.user.is_superuser):
        return Response({"message": "Forbidden"}, status=403)

    if request.method == "GET":
        if request.user.is_superuser:
            vehicles = Vehicle.objects.all()
        else:
            vehicles = Vehicle.objects.filter(enterprise__in=request.user.manager.enterprise.all())
        result_page = paginator.paginate_queryset(vehicles, request)
        serializer = VehicleSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

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
    paginator = PageNumberPagination()
    paginator.page_size = 30

    if not (hasattr(request.user, "manager") or request.user.is_superuser):
        return Response({"message": "Пользователь не является менеджером"}, status=403)

    if request.method == "GET":
        if request.user.is_superuser:
            drivers = Driver.objects.all()
        else:
            drivers = Driver.objects.filter(enterprise__in=request.user.manager.enterprise.all())

        result_page = paginator.paginate_queryset(drivers, request)
        serializer = DriverSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

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


@api_view(["GET"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def gps_data_set(request):
    if not (hasattr(request.user, "manager") or request.user.is_superuser):
        return Response({"detail": "Нет доступа"}, status=403)

    vehicle_id = request.query_params.get("vehicle_id")
    start_time = request.query_params.get("start_time")
    end_time = request.query_params.get("end_time")

    if not request.user.is_superuser and hasattr(request.user, "manager"):
        vehicle_enterpirse = Vehicle.objects.get(pk=vehicle_id).enterprise
        manager_enterprises = request.user.manager.enterprise.all()

        if vehicle_enterpirse not in manager_enterprises:
            return Response({"detail": "Нет доступа"}, status=403)

    gps_data = GPSData.objects.filter(
        vehicle_id=vehicle_id,
        timestamp__range=(start_time, end_time),
    )

    serializer = GPSDataSerializer(gps_data, many=True)
    return Response(serializer.data)
