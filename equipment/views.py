from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .models import Equipment, Task, Update
from .forms import EquipmentForm, TaskForm, UpdateForm, TaskEditForm

# ... imports ...

def landing(request):
    return render(request, 'landing.html')

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.headers.get('HX-Request'):
        return render(request, 'equipment/partials/task_detail_view.html', {'task': task})
    return render(request, 'equipment/task_detail.html', {'task': task})

def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            # Sync status/completed if needed, though form handles fields directly. 
            # Logic from toggle_task: 'done' if completed else 'todo' (if status not manually set?)
            # The form includes both, so we trust the user or add custom logic.
            # Let's trust the user's manual input for now, but maybe ensure consistency if they conflict?
            # E.g. if status is done, completed should be true.
            if task.status == 'done':
                task.completed = True
            elif task.status in ['todo', 'in_progress'] and task.completed:
                # If marked completed but status is todo/in_progress, what wins?
                # Let's say status updates win.
                task.completed = False 
            
            task.save()
            return render(request, 'equipment/partials/task_detail_view.html', {'task': task})
    else:
        form = TaskEditForm(instance=task)
    
    return render(request, 'equipment/partials/task_form.html', {'form': form, 'task': task})

def dashboard(request):
    equipment_list = Equipment.objects.all().order_by('-created_at')
    return render(request, 'equipment/dashboard.html', {'equipment_list': equipment_list})

def equipment_detail(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    tasks = equipment.tasks.all().order_by('completed', 'due_date')
    updates = equipment.updates.all().order_by('-timestamp')
    task_form = TaskForm()
    update_form = UpdateForm()
    
    return render(request, 'equipment/detail.html', {
        'equipment': equipment,
        'tasks': tasks,
        'updates': updates,
        'task_form': task_form,
        'update_form': update_form,
    })

def add_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES)
        if form.is_valid():
            equipment = form.save()
            return redirect('equipment_detail', pk=equipment.pk)
    else:
        form = EquipmentForm()
    return render(request, 'equipment/form.html', {'form': form, 'title': 'Add Equipment'})

@require_POST
def add_task(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    form = TaskForm(request.POST)
    if form.is_valid():
        task = form.save(commit=False)
        task.equipment = equipment
        # If recurring, set next_due_date to due_date (or today if not set)
        if task.recurrence:
            if task.due_date:
                task.next_due_date = task.due_date
            else:
                from django.utils import timezone
                task.next_due_date = timezone.now().date()
        task.save()
        tasks = equipment.tasks.all().order_by('completed', 'due_date')
        return render(request, 'equipment/partials/task_list.html', {'tasks': tasks, 'equipment': equipment})
    return HttpResponse("Error", status=400)

@require_POST
def toggle_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.status = 'done' if task.completed else 'todo'
    task.save()
    tasks = task.equipment.tasks.all().order_by('completed', 'due_date')
    return render(request, 'equipment/partials/task_list.html', {'tasks': tasks, 'equipment': task.equipment})

@require_POST
def add_update(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    form = UpdateForm(request.POST)
    if form.is_valid():
        update = form.save(commit=False)
        update.equipment = equipment
        update.save()
        updates = equipment.updates.all().order_by('-timestamp')
        return render(request, 'equipment/partials/update_list.html', {'updates': updates})
    return HttpResponse("Error", status=400)

from django.utils import timezone

def kanban_board(request):
    tasks = Task.objects.all().select_related('equipment').order_by('due_date')
    return render(request, 'equipment/kanban.html', {
        'icebox_tasks': tasks.filter(status='icebox'),
        'todo_tasks': tasks.filter(status='todo'),
        'in_progress_tasks': tasks.filter(status='in_progress'),
        'done_tasks': tasks.filter(status='done'),
        'today': timezone.now().date(),
    })

@require_POST
def update_task_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    # Get status from form data or query params
    new_status = request.POST.get('status')
    
    if new_status in ['icebox', 'todo', 'in_progress', 'done']:
        task.status = new_status
        task.completed = (new_status == 'done')
        task.save()
        return HttpResponse("Updated")
    
    return HttpResponse("Invalid Status", status=400)

@require_POST
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    equipment = task.equipment
    task.delete()
    
    # If request is standard/no-HTMX (or from detail page needing redirect), redirect to equipment page
    # But user asked for task list too. 
    # If HTMX, we can return the updated partial task list IF we are on the equipment page.
    # If we are on the task detail page, we should redirect to equipment page.
    # We can distinguish by looking at headers or a query param. Or just always return HTMX list if HTMX.
    # But wait, if we are on the task detail page, and satisfy HTMX, the page won't redirect, it might try to swap content.
    # The header HX-Redirect can force a redirect.
    
    if request.headers.get('HX-Request'):
        # Check where we came from? Or if 'from_detail' is in POST data?
        if request.GET.get('redirect'):
            response = HttpResponse("")
            response['HX-Redirect'] = request.GET.get('redirect')
            return response
            
        # Default behavior for task list: return updated list
        tasks = equipment.tasks.all().order_by('completed', 'due_date')
        return render(request, 'equipment/partials/task_list.html', {'tasks': tasks, 'equipment': equipment})

    return redirect('equipment_detail', pk=equipment.pk)

@require_POST
def delete_equipment(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    equipment.delete()
    return redirect('dashboard')
