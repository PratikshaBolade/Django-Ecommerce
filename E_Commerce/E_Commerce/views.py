from django.shortcuts import render,redirect
from app.models import *
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Min,Max,Sum
from cart.cart import Cart
from django.core.paginator import Page,Paginator,PageNotAnInteger,EmptyPage
from django.views.decorators.csrf import csrf_exempt
import razorpay


client = razorpay.Client(auth=("rzp_test_EMJibTgXHZwzXZ", "5PwtGFA4J2okeSJx9XLkMTbf"))

def BASE(request):
    return render(request,'base.html')

def HOME(request):
    sliders = Slider.objects.all().order_by('-id')[0:3]
    banners = BannerArea.objects.all().order_by('-id')[0:3]
    main_category = Main_Category.objects.all().order_by('-id')
    product = Product.objects.filter(section__name = 'Top Deals Of The Day')
    event = Event.objects.all()
    print(event)
    
    context={'sliders':sliders,'banners':banners,'main_category':main_category,
             'product':product,'event':event}
    return render(request,'Main/home.html',context)

def PRODUCT_DETAILS(request,id):
    product= Product.objects.filter(id=id).first()
    if product:
        product= Product.objects.filter(id=id).first()
    else:
        return redirect('404') 
            
    context={'product':product}
    return render(request,'product/product_detail.html',context)

def Error404(request):
    return render(request,'errors/404.html')


def REGISTER(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(username,email,password)
        
        if User.objects.filter(username=username).exists():
            messages.info(request,'User is Already Exists!')
            return redirect('login')
        
        if User.objects.filter(email=email).exists():
            messages.info(request,'Email is Already Exists!')
            return redirect('login')
        
        user = User(
            username = username,
            email = email
        )
        user.set_password(password)
        user.save()
        return redirect('login')
    

def LOGIN(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Email or Password is Incorrect!')
            return redirect('login')
            
                   
def LOGOUT(request):
    logout(request)
    messages.info('Logout Successfully!')
    return redirect('home')
    
@login_required(login_url='/accounts/login/')    
def PROFILE(request):
    return render(request,'profile/profile.html')    

@login_required(login_url='/accounts/login/')    
def PROFILE_UPDATE(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id
        
        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        
        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request,'Profile Successfully Updated!')
        return redirect('profile')    
      
def ABOUT(request):
    return render(request,'Main/about.html')

def CONTACT(request):
    return render(request,'Main/contact.html')

def PRODUCT(request):
    category = Category.objects.all()
    product = Product.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()
    
    colorID = request.GET.get('colorID')
    categoryID = request.GET.get('category')
    brandID = request.GET.get('brand')
    min_price = Product.objects.all().aggregate(Min('price'))
    max_price = Product.objects.all().aggregate(Max('price'))
    
    FilterPrice = request.GET.get('FilterPrice')
    if categoryID:
        product = Product.objects.filter(Categories=categoryID)
    elif brandID:
        product = Product.objects.filter(Brand=brandID)    
    elif FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        product = Product.objects.filter(price__lte = Int_FilterPrice) 
    elif colorID:
        product = Product.objects.filter(color = colorID)                  
    else:
        product = Product.objects.all()
     
    paginator = Paginator(product,8)      
    page_number = request.GET.get('page')  
    try:
        page_obj = paginator.get_page(page_number)     
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)    
             
       
    context = {'category':category, 
               'product':product, 
               'min_price':min_price,
               'max_price':max_price,
               'FilterPrice':FilterPrice,
               'color':color,
               'brand':brand,
               'page_obj':page_obj
		}
    return render(request,'product/product.html',context)



@login_required(login_url="/accounts/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def cart_detail(request):
    return render(request, 'cart/cart.html')
          
def Checkout(request):
    amount_str = request.POST.get('amount')
    amt = float(amount_str)
    amount = int(amt) * 100
    payment = client.order.create({
        'amount' : amount,
        'currency' : 'INR',
        'payment_capture' : '1'
    })
    print(payment)
    order_id = payment['id']
    context ={
        'order_id': order_id,
        'payment': payment,
    }
    return render(request,'checkout/checkout.html',context)

def PLACE_ORDER(request):
    if request.method == 'POST':
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id = uid)
        cart = request.session.get('cart')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        order_id = request.POST.get('order_id')
        payment = request.POST.get('payment')
        
        context = {'order_id':order_id}
        order = Order(
            user = user,
            firstname = firstname,
            lastname = lastname,
            country = country,
            address = address,
            city = city,
            state = state,
            postcode = postcode,
            phone = phone,
            email = email,
            payment_id = order_id,
            amount = amount
        )
        order.save()
        
        for i in cart:
            a = cart[i]['quantity']
            b = cart[i]['price']
            total = a * b
            item = OrderItem(
                user = user,
                order = order,
                product =  cart[i]['product_name'],
                image =   cart[i]['featured_image'], 
                quantity = cart[i]['quantity'],
                price =  cart[i]['price'],
                total =  total,
                
            )
            item.save()
        return render(request,'order/placeorder.html',context)
                          
def YOUR_ORDER(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id = uid)
    print(user)
    order = OrderItem.objects.filter(user = user)
    print(order)
    context ={'order':order}
    return render(request,'order/your_order.html',context)
     
   
def SEARCH(request):
    query = request.GET.get('query')
    product = Product.objects.filter(product_name__icontains=query)
    context ={'product':product}
    return render(request,'Main/search.html',context)    
   