from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q,Sum


@login_required(login_url='/login/')
def recipe(request):
    if request.method=='POST':
        data=request.POST
        r_name=data.get('r_name')
        r_description=data.get('r_description')
        r_img=request.FILES.get('r_img')

        MyRecipes.objects.create(
            r_name=r_name,
            r_description=r_description,
            r_img=r_img,
        )

    queryset=MyRecipes.objects.all()
    
    if request.GET.get('search'):
        queryset=queryset.filter(r_name__icontains=request.GET.get('search'))
    

    context={"queryset":queryset}    
    return render(request,'recipes.html',context)

@login_required(login_url='/login/')
def delete_reciepe(request,id):
    queryset = MyRecipes.objects.get(id=id)
    queryset.delete()
    return redirect('/recipe/')

@login_required(login_url='/login/')
def update_reciepe(request,id):
    queryset = MyRecipes.objects.get(id=id)
    if request.method=='POST':
        data=request.POST
        r_name=data.get('r_name')
        r_description=data.get('r_description')
        r_img=request.FILES.get('r_img')
        queryset.r_name=r_name
        queryset.r_description=r_description
        if r_img:
            queryset.r_img=r_img

        queryset.save() 
        return redirect('/recipe/')

    context={"recipes":queryset}
    return render(request,'update_reciepe.html',context)

def login_user(request):
    
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request,'Invalid username')
            return redirect('/login/')
        user=authenticate(username=username,password=password)
        if user is None:
            messages.error(request,'invalid password')
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/recipe/')
    return render(request,'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')

def register(request):
    if request.method=='POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=User.objects.filter(username=username)
        if user.exists():
            messages.info(request,'username already taken')
            return redirect('/register/')

        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password)
        user.save()
        messages.info(request,'account created successfully')
        return redirect('/register/')
    return render(request,'register.html')



def get_student(request):
    queryset=Student.objects.all()

    if request.GET.get('search'):
        search=request.GET.get('search')
        queryset=queryset.filter(
            Q(student_name__icontains=search) |
            Q(department__department__icontains=search)|
            Q(student_id__student_id__icontains=search)|
            Q(student_age__icontains=search)|
            Q(student_email__icontains=search)
        )

    paginator = Paginator(queryset, 10)  # Show 10 contacts per page.
    page_number = request.GET.get("page",1)
    page_obj = paginator.get_page(page_number)


    return render(request,'students.html',{'queryset':page_obj})


def see_marks(request,student_id):
    queryset=SubjectMarks.objects.filter(student__student_id__student_id=student_id)
    total_marks=queryset.aggregate(total_marks=Sum('marks'))
    return render(request,'see_marks.html',{'queryset':queryset ,'total_marks':total_marks,})
