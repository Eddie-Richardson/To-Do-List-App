from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Case, When
from django.core.paginator import Paginator
from django.contrib.auth import logout
from .models import Task

# Define the List Task
@login_required
def task_list(request):
    # Get filter and sorting parameters from the query string
    priority = request.GET.get('priority')
    status = request.GET.get('status')
    sort_by = request.GET.get('sort')
    page_number = request.GET.get('page')  # Get the current page number

    # Start with tasks belonging to the logged-in user
    tasks = Task.objects.filter(user=request.user)

    # Apply priority filter
    if priority:
        tasks = tasks.filter(priority=priority)
    if priority not in ['High', 'Medium', 'Low', None]:
        tasks = tasks.filter(priority='Medium')  # Default fallback

    # Apply completion status filter
    if status == 'completed':
        tasks = tasks.filter(completed=True)
    elif status == 'incomplete':
        tasks = tasks.filter(completed=False)

    # Apply sorting
    if sort_by == 'title':
        tasks = tasks.order_by('title')
    elif sort_by == 'priority':
        tasks = tasks.order_by(
            Case(
                When(priority='High', then=1),
                When(priority='Medium', then=2),
                When(priority='Low', then=3),
            )
        )
    if not sort_by:
        tasks = tasks.order_by('id')  # Default sorting by creation date

    # Add pagination logic (10 tasks per page)
    paginator = Paginator(tasks, 10)
    tasks = paginator.get_page(page_number)

    # Pass tasks and pagination information to the template
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


# Define the Add Task
@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')  # Get the title from the form
        description = request.POST.get('description')  # Get the description from the form
        priority = request.POST.get('priority')  # Get priority from the form
        Task.objects.create(user=request.user, title=title, description=description, completed=False, priority=priority)  # Save to the database
        return redirect('task-list')  # Redirect to the task list page
    return render(request, 'tasks/add_task.html')  # Render the form template

# Define the Edit Task
@login_required
def edit_task(request, task_id):
    # Get the specific task or return a 404 error
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.title = request.POST.get('title')  # Update title
        task.description = request.POST.get('description')  # Update description
        task.priority = request.POST.get('priority')  # Update priority
        task.completed = 'completed' in request.POST  # Update completion status
        task.save()  # Save changes to the database
        return redirect('task-list')  # Redirect to task list after saving

    return render(request, 'tasks/edit_task.html', {'task': task})  # Render the form

# Define the Delete Task
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.delete()  # Delete the task from the database
        return redirect('task-list')  # Redirect to the task list after deleting

    return render(request, 'tasks/delete_task.html', {'task': task})  # Confirm deletion

# Define User Registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            return redirect('login')  # Redirect to the login page
    else:
        form = UserCreationForm()  # Show an empty registration form
    return render(request, 'tasks/register.html', {'form': form})

# Define User Profile
@login_required
def profile(request):
    return render(request, 'tasks/profile.html', {'user': request.user})

# Custom Logout for Debugging Built in Logout
def custom_logout(request):
    logout(request)  # Log the user out
    return redirect('/login/')  # Redirect to the login page
