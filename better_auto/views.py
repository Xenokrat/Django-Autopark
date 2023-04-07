from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import BetterVehicleSerializer
from .service import VehicleService

vehicle_service = VehicleService()


@api_view(["GET"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def vehicle_list(request):
    paginator = PageNumberPagination()
    paginator.page_size = 30

    if not (hasattr(request.user, "manager") or request.user.is_superuser):
        return Response({"message": "Forbidden"}, status=403)

    vehicles_data = vehicle_service.get_all_vehicles()
    serializer = BetterVehicleSerializer(vehicles_data, many=True)
    return Response(
        serializer.data,
    )


@api_view(["GET"])
def vehicle_detail(request, id: int):
    if not (hasattr(request.user, "manager") or request.user.is_superuser):
        return Response({"message": "Forbidden"}, status=403)
    vehicle_data = vehicle_service.get_vehicle_by_id(id)
    if vehicle_data is None:
        return Response(status=404)
    serializer = BetterVehicleSerializer(vehicle_data)
    return Response(serializer.data)
