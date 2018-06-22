from django.shortcuts import render, redirect, HttpResponse
from apps.courses.models import *
from djangounchained_flash import ErrorManager, ErrorMessage, getFromSession
import datetime

def index(request):
    if 'flash' not in request.session:
        request.session['flash']=ErrorManager().addToSession()

    context={'courses':Course.objects.all()}

    e=getFromSession(request.session['flash'])
    name_errors=e.getMessages('name')
    description_errors=e.getMessages('description')
    deletion_success=e.getMessages('delete')
    request.session['flash']=e.addToSession()
    
    context['deletion_success']=deletion_success
    context['name_errors']=name_errors
    context['description_errors']=description_errors
    return render(request, 'courses/courses.html',context)

def add(request):
    if(request.method!='POST'):
        print('Hacker alert')
        return redirect('/')

    errors=Course.objects.validate(request.POST)
    if(len(errors)):
        e=getFromSession(request.session['flash'])
        for tag,error in errors.items():
            print('Error: ',error)
            print('Tag: ',tag)
            e.addMessage(error, tag)
        request.session['flash']=e.addToSession()
        return redirect('/')

    Course.objects.create(name=request.POST['name'], description=request.POST['description'], created_at_clean=datetime.datetime.now().strftime('%b %d, %Y %I:%M%p'))
    print('Adding new course')
    return redirect('/')

def delete(request, course_id):
    course=Course.objects.get(id=course_id)
    context={'course':course}
    return render(request, 'courses/delete.html', context)

def destroy(request, course_id):
    course=Course.objects.get(id=course_id)
    course.delete()
    e=getFromSession(request.session['flash'])
    e.addMessage('Successfully deleted course', 'delete')
    request.session['flash']=e.addToSession()
    return redirect('/')

# Create your views here.
