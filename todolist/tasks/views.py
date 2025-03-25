from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Task

# Define the List Task
@login_required
def task_list(request):
    # Fetch all tasks from the database
    tasks = Task.objects.filter(user=request.user)  # Show only the logged-in user's tasks
    # Pass tasks to the template for rendering
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

# Define the Add Task
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')  # Get the title from the form
        description = request.POST.get('description')  # Get the description from the form
        Task.objects.create(title=title, description=description, completed=False)  # Save to the database
        return redirect('task-list')  # Redirect to the task list page
    return render(request, 'tasks/add_task.html')  # Render the form template

# Define the Edit Task
def edit_task(request, task_id):
    # Get the specific task or return a 404 error
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.title = request.POST.get('title')  # Update title
        task.description = request.POST.get('description')  # Update description
        task.completed = 'completed' in request.POST  # Update completion status
        task.save()  # Save changes to the database
        return redirect('task-list')  # Redirect to task list after saving

    return render(request, 'tasks/edit_task.html', {'task': task})  # Render the form

# Define the Delete Task
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