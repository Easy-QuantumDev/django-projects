from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Task
from django.contrib.auth.decorators import login_required
        
@login_required
def task_list(req):
    search = req.GET.get("search",'')
    status = req.GET.get("status","")
    
    tasks = Task.objects.all()
    if search :
        tasks = tasks.filter(title__icontains=search)
    if status=='completed':
        tasks = tasks.filter(is_completed=True)
        
    elif status=='pending':
        tasks = tasks.filter(is_completed=False)

    paginator = Paginator(tasks,5)
    page_number =   req.GET.get("page")
    page_object = paginator.get_page(page_number)
           
        
            
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(is_completed=True).count()
    pending_tasks = Task.objects.filter(is_completed=False).count()
    
    
    
    return render(req,'task_list.html',context={"tasks":tasks,'total_tasks':total_tasks,"completed_tasks":completed_tasks,"pending_tasks":pending_tasks,"search":search,"page_object":page_object})


    
@login_required
def task_detail(req,pk):
    task= get_object_or_404(Task,pk=pk)
    return render(req,'task_detail.html',{'task':task})
@login_required
def create_task(req):
    if req.method=='POST':
        title = req.POST.get('title')
        description = req.POST.get('description')
        if not title:
            return render(req,'create_task.html',{'error':"Task title is required"})
        Task.objects.create(title=title,description=description,owner=req.user)
      
        messages.success(req,"Task created successfully!")
        
        return redirect('tasks:home')
    return render(req,'create_task.html')
        
        
        
   
@login_required
def update_task(req,pk):
    task = get_object_or_404(Task,pk=pk)
    if req.method=='POST':
        title = req.POST.get('title')
        description = req.POST.get('description')
        if not title:
            return render(req,'task_update.html',{'error':"Task title is required"})
        task.title=title
        task.description = description
        task.save()
        messages.success(req,"Task Update successfully!")

        return redirect("tasks:task_detail",pk=task.pk)
    return render(req,'task_detail.html')
@login_required
def delete_task(req,pk):
    task = get_object_or_404(Task,pk=pk) 
    if req.method =='POST':
        task.delete()
        messages.success(req,"Task Deleted successfully!")

        return redirect("tasks:home")
    return render(req,"task_detail.html",{'task':task})

@login_required
def task_toggle(req,pk):
    task = get_object_or_404(Task,pk=pk)
    if req.method =='POST':
        task.is_completed = not task.is_completed

        task.save()
        if task.is_completed:
            messages.success(
                req,
                'Task marked as completed!'
            )
        else:
            messages.success(
                req,
                'Task marked as pending!'
            )


        return redirect('tasks:home')
    return render(req,'task_detail.html',{'task':task})

@login_required       
def edit_task(req,pk):
    task = get_object_or_404(Task,pk=pk)
    if req.method=='POST':
        title = req.POST.get("title")    
        description = req.POST.get("description")
        if not title:
            
            return redirect("tasks:home")
            
        
        task.title=title    
        task.description=description    
        task.save()
        messages.success(req,"Task Edited successfully!")

        return redirect("tasks:home")
    return redirect("tasks:home")
    
    
# Create your views here.
