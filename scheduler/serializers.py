from rest_framework import serializers

from .models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = ["id", "schedule"]

    def validate_schedule(self, value):

        days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

        for day, slots in value.items():
            if day not in days_of_week:
                raise serializers.ValidationError(f"Invalid day: {day}")

            for slot in slots:
                if "start" not in slot or "stop" not in slot or "ids" not in slot:
                    raise serializers.ValidationError("Each time slot must contain 'start', 'stop', and 'ids' fields.")

        return value
