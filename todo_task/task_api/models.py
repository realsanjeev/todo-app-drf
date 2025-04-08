from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet

User = settings.AUTH_USER_MODEL


class TodoQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(public=True)

    def search(self, query, user=None):
        lookup_query = Q(task__icontains=query) | Q(desc__icontains=query)
        # see for public book
        qs = self.is_public().filter(lookup_query)
        if user is not None:
            # see query in user profile
            qs2 = self.filter(user=user).filter(lookup_query)
            # get result without repetion
            qs = (qs | qs2).distinct()
        return qs


class TodoManager(models.Manager):
    def get_queryset(self, *args, **kwargs) -> QuerySet:
        return TodoQuerySet(self.model, using=self._db)

    def search(self, query, user=None):
        return self.get_queryset().search(query, user=user)


class TodoTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    task = models.CharField(max_length=255)
    desc = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)
    completed = models.BooleanField(default=False, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True)
    public = models.BooleanField(default=False)

    objects = TodoManager()

    class Meta:
        indexes = [
            models.Index(fields=["user", "completed"]),
            models.Index(fields=["user", "updated"]),
        ]
        ordering = ["-updated"]

    def __str__(self) -> str:
        return self.task
