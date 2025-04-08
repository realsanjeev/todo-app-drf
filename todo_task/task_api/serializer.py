from rest_framework import serializers, validators
from task_api.models import TodoTask


class TodoSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    view_url = serializers.HyperlinkedIdentityField("todo-detail", lookup_field="pk")
    description = serializers.CharField(source="desc", required=False)

    class Meta:
        model = TodoTask
        fields = [
            "user",
            "task",
            "description",
            "completed",
            "public",
            "timestamp",
            "updated",
            "view_url",
        ]

    def validate_task(self, value):
        request = self.context.get("request")
        user = request.user
        if len(value) < 4:
            raise validators.ValidationError(
                f"task: `{value}`; length too short to take it as task"
            )
        qs = TodoTask.objects.filter(user=user, task__iexact=value)
        if qs.exists():
            raise serializers.ValidationError(
                f"Task with task: `{value}` already exists"
            )
        return value
