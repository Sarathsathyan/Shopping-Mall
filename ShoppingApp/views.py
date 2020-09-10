import re
from django.shortcuts import render

from django.contrib.auth import login,logout,authenticate
from django.contrib import auth
from django.contrib import messages
from email_validator import validate_email, EmailNotValidError
from django.shortcuts import render,redirect
from django.contrib.auth.models import User

from .models import CompanyInfo
# Create your views here.

def index(request):
    return render(request,'main_pages/index.html')

def register(request):
    if request.method =='POST':
        firstname = request.POST['fname']
        lastname = request.POST['lname']
        email = request.POST['email']
        print(firstname)
        username = request.POST['email']
        password = request.POST['pass1']
        conform = request.POST['pass2']
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'That email is being used')
            return redirect('register')
        if firstname.isdigit():
            messages.error(request, 'Firstname cannot have numbers')

            return redirect('register')
        if lastname.isdigit():
            messages.error(request, 'Lastname cannot have numbers')
            return redirect('register')
        if regex.search(firstname):
            messages.error(request, 'firstname cannot have special characters')
            return redirect('register')
        if regex.search(lastname):
            messages.error(request, 'lastname cannot have special characters')
            return redirect('register')
        try:
            v = validate_email(email)
            val_email = v["email"]
        except EmailNotValidError as e:
            messages.error(request, 'Invalid Email ID')
            return redirect('register')
        if password != conform:
            messages.error(request,'Password mismatch')
            return redirect('register')
        try:
            User.objects.create_user(username=username, email=email, first_name=firstname, last_name=lastname,
                                     password=password)

        except:
            usr = User.objects.get(username=email)
            usr.delete()
            messages.error(request, 'Some error occured !')
            return redirect('register')
    return render(request,'main_pages/Register.html')


def userlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass1']
        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            try:
                if request.user.is_active:
                    messages.success(request,"Login success")
                    return redirect('index')
            except:
                messages.error(request,"Login failed")
                return redirect('login')
        else:
            messages.error(request,"Login failed")
    return render(request,'main_pages/login.html')

def user_logout(request):
    auth.logout(request)
    return render(request,'main_pages/logout.html')



def ProfileEdit(request):
    user = request.user
    if request.method == 'POST':
        c_name = request.POST['c_name']
        c_location = request.POST['c_location']
        c_state = request.POST['stt']
        c_district = request.POST['district']
        c_num = request.POST['contact']
        user_pic = request.FILES.get('uploadfile')
        data = CompanyInfo(shop_id_id=user.pk,shop_name=c_name,shop_loc=c_location,shop_state=c_state,shop_des=c_district,user_image=user_pic,phone=c_num)
        data.save()
        messages.success(request,"Profile Updated")

    return render(request,'client_pages/profileEdit.html')

def AddProduct(request):
    return render(request,'client_pages/addProduct.html')