import re
from django.shortcuts import render

from django.contrib.auth import login,logout,authenticate
from django.contrib import auth
from django.contrib import messages
from email_validator import validate_email, EmailNotValidError
from django.shortcuts import render,redirect
from django.contrib.auth.models import User

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from ShoppingMachine.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, EmailMessage

from .models import CompanyInfo,ProductDetail,RoleDetail,CareerCategory,Category_role,UserReviews


# Create your views here.

def index(request):
    products = ProductDetail.objects.all()
    context ={
        'products':products,
    }
    return render(request,'main_pages/index.html',context)

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
                if request.user.is_staff and request.user.is_superuser:
                    messages.success(request,"Welcome Admin")
                    return redirect('admindash')
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
    user = request.user


    if request.method == 'POST':
        cmp_name = request.POST['cmp_name']
        img1 = request.FILES.get('img1')
        img2 = request.FILES.get('img2')
        img3 = request.FILES.get('img3')
        print(img1)
        pro_name = request.POST['pro_name']
        pro_description = request.POST['descrip']
        pro_price = request.POST['price']
        data = ProductDetail(cmp_name=cmp_name,pro_image1=img1,pro_image2=img2,pro_image3=img3,
                             pro_name=pro_name,pro_description=pro_description,pro_price=pro_price)
        data.save()
        messages.success(request,"Submitted successfully")

    comp_list = CompanyInfo.objects.all()
    context={
        'comp_list':comp_list
    }
    return render(request,'client_pages/addProduct.html',context)

def ProductList(request,id):
    print(id)
    products = ProductDetail.objects.all()
    context ={
        'products':products
    }
    return render(request,'client_pages/productList.html',context)

def SingleProduct(request,id):

    product_info = ProductDetail.objects.get(id = id)
    context={
        'pro_info':product_info,
    }
    print(product_info.pro_image1)
    return render(request,'client_pages/single_product.html',context)

def Contact(request):
    return render(request,'main_pages/contact.html')

# User section
def ViewProduct(request,id):
    user = request.user
    if request.method == 'POST':
        if 'review_sub' in request.POST:
            review = request.POST['review']
            print(user.email)
            data = UserReviews(product_id_id=id,user_name=user.first_name,user_email=user.email,review=review)
            data.save()
            messages.success(request,"Submitted successfully")
    product = ProductDetail.objects.get(id=id)
    context ={
        'product':product
    }
    return render(request,'main_pages/product_info.html',context)



# Admin Section

def AdminRole(request):
    if request.user.is_staff and request.user.is_superuser:
        if request.method=='POST':
            # When we Press Create Role Button
            if 'create' in request.POST:
                # Assigning Unique Id To each role
                user_role=request.POST['role']
                if user_role=="Sub Admin":
                    role_user_id="SUB"+str(100+(RoleDetail.objects.filter(user_role="SUB").count()+1))
                elif user_role=="Client":
                    role_user_id="CLIENT"+str(200+(RoleDetail.objects.filter(user_role="Client").count()+1))

                else:
                    role_user_id=000

                user_firstname = request.POST['fname']
                user_lastname = request.POST['lname']
                role_user_name=request.POST['email']
                role_user_email=request.POST['email']
                regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
                if User.objects.filter(email=role_user_email).exists():
                    messages.error(request, 'The email already exists')
                    return redirect('adminrolecreation')
                if User.objects.filter(username=role_user_name).exists():
                    messages.error(request, 'That username is being used')
                    return redirect('adminrolecreation')
                if user_firstname.isdigit():
                    messages.error(request, 'Firstname cannot have numbers')
                    return redirect('adminrolecreation')
                if regex.search(user_firstname):
                    messages.error(request, 'Firstname cannot have special characters')
                    return redirect('adminrolecreation')
                if user_lastname.isdigit():
                    messages.error(request, 'Lastname cannot have numbers')
                    return redirect('adminrolecreation')
                if regex.search(user_lastname):
                    messages.error(request, 'Lastname cannot have special characters')
                    return redirect('adminrolecreation')

                role_user_password=request.POST['password']
                mail_subject = "[Activate Account] Ecart - Ecart Admin Team"
                current_site = get_current_site(request)
                message = render_to_string('main_pages/user_info.html', {
                    'user': role_user_email,
                    'firstname': user_firstname,
                    'lastname': user_lastname,
                    'domain': current_site.domain,
                    'pass': role_user_password,
                })
                email = EmailMessage(mail_subject, message, from_email=EMAIL_HOST_USER, to=[role_user_email])
                email.send()
                try:

                    user=User.objects.create_user(username = role_user_name,email= role_user_email,first_name= user_firstname,
                                                    last_name = user_lastname,password = role_user_password)
                    if user_role == "Sub Admin":
                        user.is_staff = True
                    elif user_role == "Client":
                        user.is_staff = False
                        user.is_superuser = True
                    user.save()
                    u_id = User.objects.get(username=role_user_name)
                    role = RoleDetail(user_id=u_id, role_user_id=role_user_id, user_role=user_role, role_user_name=role_user_name,
                                      role_user_email=role_user_email, role_user_password=role_user_password)
                    role.save()

                except:
                    messages.error(request,"Some error occured")
                    return redirect("adminrolecreation")
                # Saving the role input in the model
                messages.success(request,"Email has been sent successfully")
                return redirect("admindash")

            # When we press Remove Button
            if 'delete' in request.POST:
                del_id=request.POST['del_id']

                if RoleDetail.objects.filter(role_user_id=del_id).exists():
                    main_id_1 =RoleDetail.objects.get(role_user_id=del_id)
                    main_id = main_id_1.user_id_id
                    roled=RoleDetail.objects.get(role_user_id=del_id).delete()
                    # Delete from the user table
                    user_del = User.objects.get(id=main_id).delete()
                    messages.success(request,"Deleted success")
                else:
                    messages.error(request,"Some error occured")
                return redirect('admindash')

            if 'roleSort' in request.POST:
                role = request.POST['roleSort']
                if role == 'ALL':
                    roled=RoleDetail.objects.all()
                else:
                    roled = RoleDetail.objects.filter(user_role=role)

                context ={
                    'roles':roled
                }
                return render(request, 'admin_section/role_creation.html', context)


        roles=RoleDetail.objects.order_by("-role_create_date")
        context={
            'roles':roles
        }
        return render(request,'admin_section/role_creation.html',context)
    else:
        messages.error(request,"Wrong URL")
        return redirect('logout')

    return render(request,'admin_section/role_creation.html')


def Category(request):
    if request.method=='POST':
        if 'category_submit' in request.POST:
            cag_name=request.POST['cagname']

            if CareerCategory.objects.filter(category=cag_name).exists():
                messages.error(request, 'The Category already exists')
                return redirect('category-create')

            if CareerCategory.objects.filter(category=cag_name.upper()).exists():
                messages.error(request, 'The Category already exists')
                return redirect('category-create')

            if CareerCategory.objects.filter(category=cag_name.lower()).exists():
                messages.error(request, 'The Category already exists')
                return redirect('category-create')

            if CareerCategory.objects.filter(category=cag_name.capitalize()).exists():
                messages.error(request, 'The Category already exists')
                return redirect('category-create')


            category_id=CareerCategory.objects.all().count()+1
            cag_obj=CareerCategory(category_id=category_id,category=cag_name)
            cag_obj.save()

            return redirect('category-create')


        if 'cfp_submit' in request.POST:
            cfp_category=request.POST['cat_cag']
            cfp_role=request.POST['cat_sub']

            cfp_id=Category_role.objects.all().count()+1
            cfp_obj=Category_role(cat_id=cfp_id,cat_category=cfp_category,cat_sub=cfp_role)
            cfp_obj.save()
            messages.success(request, "Added to Category")
            return redirect('category-create')


    category_list=CareerCategory.objects.all()

    cfp_list=Category_role.objects.order_by("-cat_create_date")

    context={
        'category_list':category_list,
        'cfp_list':cfp_list,
    }
    return render(request,'admin_section/category-create.html',context)

def category_edit(request,id):
    category_id=id
    datas=CareerCategory.objects.get(category_id=category_id)
    name=datas.category

    if request.method=="POST":
        if 'category_submit' in request.POST:
            category=request.POST['category_name']

            datas=CareerCategory.objects.get(category_id=category_id)

            datas.category=category
            datas.save()

            Category_role.objects.filter(cat_category=name).update(cat_category=category)
            return redirect('category-create')

    context={
        'datas':datas,
    }
    return render(request,'admin_section/category-edit.html',context)

def SubEdit(request,id):
    cfp_id=id
    print(cfp_id)
    datas=Category_role.objects.get(id=cfp_id)

    if request.method=="POST":
        if 'cfp_submit' in request.POST:
            cfp_category=request.POST['cfp_cag']
            cfp_role=request.POST['cfp_role']

            datas=Category_role.objects.get(cat_id=cfp_id)
            datas.cat_category=cfp_category
            datas.cat_sub=cfp_role
            datas.save()

            return redirect('category-create')

        if 'cfp_delete' in request.POST:
            delete_id=request.POST['delete_id']
            obj=Category_role.objects.filter(cat_id=delete_id)
            obj.delete()

            return redirect('category-create')


    category_list=CareerCategory.objects.all()

    role_str=datas.cat_sub
    role_list=role_str.split('_')
    context={
        'datas':datas,
        'role_list':role_list,
        'category_list':category_list,
    }

    return render(request,'admin_section/sub-category-edit.html',context)

def AdminProducts(request):
    pro_detail = ProductDetail.objects.all()

    if request.method == 'POST':
        if 'delete' in request.POST:
            del_id = request.POST['del_id']
            if ProductDetail.objects.filter(id=del_id).exists():

                roled = ProductDetail.objects.get(id=del_id).delete()

                messages.success(request, "Deleted success")
            else:
                messages.error(request, "Some error occured")
            return redirect('productDetails')


    context ={
        'pro_detail':pro_detail,
    }

    return render(request,'admin_section/product-detail.html',context)

def AdminAddProduct(request):

    if request.method == 'POST':
        pro_category = request.POST['category']
        pro_sub = request.POST['sub_cat']
        pro_name = request.POST['pro_name']
        pro_description = request.POST['descrip']
        img1 = request.FILES.get('img1')
        pro_price = request.POST['pro_price']
        pro_rating = request.POST['rating']

        data = ProductDetail(pro_name = pro_name,pro_category=pro_category,pro_sub=pro_sub,
                             pro_description=pro_description,pro_image=img1,pro_rating=pro_rating,
                             pro_price=pro_price)
        data.save()
        messages.success(request,"Submitted successfully")
    category_list=CareerCategory.objects.all()

    cfp_list=Category_role.objects.order_by("-cat_create_date")
    context={
        'category_list':category_list,
        'cfp_list':cfp_list,
    }


    return render(request,'admin_section/add-product.html',context)

def ProductReview(request,id):
    data = ProductDetail.objects.get(id=id)
    reviews = UserReviews.objects.filter(product_id_id=data.pk)
    context ={
        'reviews':reviews,
        'data' : data,
    }
    return render(request,'admin_section/product_review_detail.html',context)

def CustomerReviewInfo(request,id):

    data = UserReviews.objects.get(id = id)
    context ={
        'data':data
    }
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        msg = request.POST['message']


        mail_subject = "Clarification for the review"
        message = f'Hi,{data.user_name} thanks for your valuable feedback, {msg}'
        email = EmailMessage(mail_subject, message, from_email=EMAIL_HOST_USER, to=[email, ])
        email.send()
        messages.success(request,"Email send successfully")
    return render(request,'admin_section/customer_review_info.html',context)


def OrderSummary(request,id):
    print(id)
    return render(request,'main_pages/order_summary.html')