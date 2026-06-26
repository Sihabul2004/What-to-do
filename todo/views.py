from django.shortcuts import render, redirect, get_object_or_404
from .models import Task


def home(request):

    if request.method == "POST":
        title = request.POST.get("title")
        due_date = request.POST.get("due_date")

        if title:
            Task.objects.create(
                title=title,
                due_date=due_date if due_date else None
            )

        return redirect("home")

    tasks = Task.objects.all().order_by("completed", "due_date")

    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(completed=True).count()
    pending_tasks = total_tasks - completed_tasks

    context = {
        "tasks": tasks,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
    }

    return render(request, "todo/home.html", context)


def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    task.completed = not task.completed
    task.save()

    return redirect("home")


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    task.delete()

    return redirect("home")
