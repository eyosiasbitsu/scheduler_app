from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Schedule
from .serializers import ScheduleSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]  # Require authentication for all CRUD operations

    # CREATE Schedule with Swagger documentation
    @swagger_auto_schema(
        operation_description="Create a new schedule with time slots for each day of the week.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "schedule": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={
                        "monday": [
                            {"start": "08:00", "stop": "10:00", "ids": [1, 2]},
                            {"start": "10:30", "stop": "12:00", "ids": [3, 4]},
                        ],
                    },
                )
            },
        ),
        responses={
            201: openapi.Response(
                description="Schedule created successfully",
                examples={
                    "application/json": {
                        "id": 1,
                        "schedule": {
                            "monday": [
                                {"start": "08:00", "stop": "10:00", "ids": [1, 2]},
                                {"start": "10:30", "stop": "12:00", "ids": [3, 4]},
                            ],
                            "tuesday": [{"start": "09:00", "stop": "11:00", "ids": [5, 6]}],
                        },
                    }
                },
            ),
            400: openapi.Response(
                description="Invalid input",
                examples={"application/json": {"schedule": {"funday": ["Invalid day: funday"]}}},
            ),
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    # LIST all schedules
    @swagger_auto_schema(
        operation_description="Get all schedules, with details for each day of the week.",
        responses={
            200: openapi.Response(
                description="List of schedules",
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "schedule": {
                                "monday": [
                                    {"start": "08:00", "stop": "10:00", "ids": [1, 2]},
                                    {"start": "10:30", "stop": "12:00", "ids": [3, 4]},
                                ]
                            },
                        }
                    ]
                },
            )
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # RETRIEVE a specific schedule
    @swagger_auto_schema(
        operation_description="Retrieve a specific schedule by its ID.",
        responses={
            200: openapi.Response(
                description="Details of the schedule",
                examples={
                    "application/json": {
                        "id": 1,
                        "schedule": {
                            "monday": [
                                {"start": "08:00", "stop": "10:00", "ids": [1, 2]},
                                {"start": "10:30", "stop": "12:00", "ids": [3, 4]},
                            ]
                        },
                    }
                },
            ),
            404: openapi.Response(
                description="Schedule not found", examples={"application/json": {"detail": "Not found."}}
            ),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # UPDATE a specific schedule
    @swagger_auto_schema(
        operation_description="Update a specific schedule by its ID.",
        request_body=ScheduleSerializer,
        responses={
            200: openapi.Response(
                description="Schedule updated successfully",
                examples={
                    "application/json": {
                        "id": 1,
                        "schedule": {"tuesday": [{"start": "09:00", "stop": "11:00", "ids": [5, 6]}]},
                    }
                },
            ),
            400: openapi.Response(
                description="Invalid input",
                examples={"application/json": {"schedule": {"monday": ["Missing 'start' field"]}}},
            ),
            404: openapi.Response(
                description="Schedule not found", examples={"application/json": {"detail": "Not found."}}
            ),
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # DELETE a specific schedule
    @swagger_auto_schema(
        operation_description="Delete a specific schedule by its ID.",
        responses={
            204: openapi.Response(description="Schedule deleted successfully", examples={"application/json": None}),
            404: openapi.Response(
                description="Schedule not found", examples={"application/json": {"detail": "Not found."}}
            ),
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
