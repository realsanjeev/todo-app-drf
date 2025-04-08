from rest_framework import authentication, generics, permissions
from task_api.authentication import TokenAuthentication
from task_api.models import TodoTask
from task_api.serializer import TodoSerializer


class TodoCreateListAPIView(generics.ListCreateAPIView):
    queryset = TodoTask.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    authentication_classes = [authentication.SessionAuthentication, TokenAuthentication]
    serializer_class = TodoSerializer

    def get_queryset(self):
        """Filter tasks to only show the authenticated user's tasks."""
        return TodoTask.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        task = serializer.validated_data.get("task")
        desc = serializer.validated_data.get("desc")
        if desc is None:
            desc = task
        serializer.save(user=self.request.user, desc=desc)


class TodoDetailAPIView(generics.RetrieveAPIView):
    queryset = TodoTask.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    authentication_classes = [authentication.SessionAuthentication, TokenAuthentication]
    lookup_field = "pk"
    serializer_class = TodoSerializer

    def get_queryset(self):
        """Filter tasks to only show the authenticated user's tasks."""
        return TodoTask.objects.filter(user=self.request.user)


class TodoUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = TodoTask.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    authentication_classes = [authentication.SessionAuthentication, TokenAuthentication]
    serializer_class = TodoSerializer
    lookup_field = "pk"

    def get_queryset(self):
        """Filter tasks to only show the authenticated user's tasks."""
        return TodoTask.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        task = serializer.validated_data.get("task")
        desc = serializer.validated_data.get("desc")
        if desc is None:
            desc = task
        serializer.save(user=self.request.user, desc=desc)


class TodoDeleteAPIView(generics.RetrieveDestroyAPIView):
    queryset = TodoTask.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    authentication_classes = [authentication.SessionAuthentication, TokenAuthentication]
    serializer_class = TodoSerializer

    def get_queryset(self):
        """Filter tasks to only show the authenticated user's tasks."""
        return TodoTask.objects.filter(user=self.request.user)


todo_create_retrieve_view = TodoCreateListAPIView.as_view()
todo_detail_retrieve_view = TodoDetailAPIView.as_view()
todo_update_view = TodoUpdateAPIView.as_view()
todo_delete_view = TodoDeleteAPIView.as_view()


class SearchTodoAPIView(generics.ListAPIView):
    queryset = TodoTask.objects.all()
    serializer_class = TodoSerializer

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get("q")
        results = TodoTask.objects.none()
        if q is not None:
            user = None
            if self.request.user.is_authenticated:
                user = self.request.user
            results = qs.search(q, user=user)
        return results


todo_search_view = SearchTodoAPIView.as_view()
