from typing import Any

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import generic
from task_api.models import TodoTask


@method_decorator(login_required, name="dispatch")
class GenericListView(generic.ListView):
    template_name = "myapp/index.html"
    context_object_name = "todo_list"

    def get_queryset(self) -> QuerySet[Any]:
        return TodoTask.objects.filter(
            completed=False, user=self.request.user
        ).order_by("updated")


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if User.objects.filter(email=email).exists():
            messages.error(request, f"A user with email {email} already exists.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, f"A user with username {username} already exists.")
        elif password1 != password2:
            messages.error(
                request, "Password and Confirmation password must be the same."
            )
        else:
            user = User.objects.create_user(
                username=username, email=email, password=password1
            )
            messages.success(request, "Your account has been created successfully.")
            login(request, user)
            return redirect("todos:index")

    return render(request, "account/signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("todos:index")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "account/login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("todos:login")


@login_required
def add(request, *args, **kwargs):
    task = request.POST.get("task")
    desc = request.POST.get("desc")

    # Validate task is not empty
    if not task or task.strip() == "":
        messages.error(request, "Task cannot be empty.")
        return redirect("todos:index")

    if desc is None:
        desc = task

    # Create a TodoTask associated with the authenticated user
    TodoTask.objects.create(user=request.user, task=task, desc=desc)

    return redirect("todos:index")


@login_required
def delete(request, *args, **kwargs):
    id = kwargs.get("todo_id")
    todo = get_object_or_404(TodoTask, pk=id)

    if todo.user != request.user:
        messages.error(request, "You are not authorized to delete this task.")
        return redirect("todos:index")

    todo.delete()
    return redirect("todos:index")


@login_required
def update(request, *args, **kwargs):
    id = kwargs.get("todo_id")
    completed = request.POST.get("completed", False)
    if completed == "on":
        completed = True
    todo = get_object_or_404(TodoTask, pk=id)

    if todo.user != request.user:
        messages.error(request, "You are not authorized to update this task.")
        return redirect("todos:index")

    todo.completed = completed
    todo.save()
    return redirect("todos:index")


@method_decorator(login_required, name="dispatch")
class CompletedTaskListView(generic.ListView):
    template_name = "myapp/completed_task.html"
    context_object_name = "todo_list"
    paginate_by = 10  # Number of tasks per page

    def get_queryset(self):
        return TodoTask.objects.filter(completed=True, user=self.request.user).order_by(
            "updated"
        )
