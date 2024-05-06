import datetime
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User


class Slider(models.Model):
    DISCOUNT_DEAL =(
        ('HOT_DEALS','HOT_DEALS'),
        ('NEW_ARRIVALS','NEW_ARRIVALS')
    )
    Image=models.ImageField(upload_to='media/slider_image')
    Discount_Deal=models.CharField(choices=DISCOUNT_DEAL,max_length=100)
    SALE =models.IntegerField()
    Brand_Name=models.CharField(max_length=200)
    Discount=models.IntegerField()
    Link=models.CharField(max_length=200)

    def __str__(self):
        return self.Brand_Name
    
class BannerArea(models.Model):
    image = models.ImageField(upload_to='media/banner_img')
    Discount_Deal=models.CharField(max_length=100)
    Quote=models.CharField(max_length=100)
    Discount=models.IntegerField()
    Link=models.CharField(max_length=200,null=True)
     
    def __str__(self) -> str:
        return self.Quote   
    
class Main_Category(models.Model):
    name=models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.name  
    
class Category(models.Model):
    main_category = models.ForeignKey(Main_Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.name + "--" + self.main_category.name  
    
class Sub_Categories(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE) 
    name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.category.main_category.name + " -- " + self.category.name + " -- " + self.name
    
class Section(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.name
    
class Color(models.Model):
    code = models.CharField(max_length=100)    
    
    def __str__(self) -> str:
        return self.code
 
class Brand(models.Model):
    name = models.CharField(max_length=100)    
    
    def __str__(self) -> str:
        return self.name
    
class Product(models.Model):
    total_quantity = models.IntegerField()
    Availability = models.IntegerField()
    featured_image = models.CharField(max_length=100)     
    product_name = models.CharField(max_length=100) 
    Brand = models.ForeignKey(Brand,on_delete=models.CASCADE,null=True)
    price = models.IntegerField()
    Discount = models.IntegerField()
    tax = models.IntegerField(blank=True,null=True)
    delivery_charge = models.IntegerField(blank=True, null=True)
    Product_Information = RichTextField(null=True)
    model_name = models.CharField(max_length=100)
    Categories = models.ForeignKey(Category,on_delete=models.CASCADE)
    color = models.ForeignKey(Color,on_delete=models.CASCADE,null=True)
    Tags = models.CharField(max_length=100)
    Description = RichTextField(null=True)
    section = models.ForeignKey(Section,on_delete=models.DO_NOTHING)
    
    def __str__(self) -> str:
        return self.product_name
    
    
class Product_Image(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE) 
    Image_url = models.CharField(max_length=200)
    
class Additional_Information(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)  
    specification = models.CharField(max_length=100)           
    detail = models.CharField(max_length=200)
    
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postcode = models.IntegerField()
    phone = models.IntegerField()
    email = models.EmailField(max_length=100)
    payment_id = models.CharField(max_length=300,blank=True,null=True)
    paid = models.BooleanField(default=False,null=True)
    date = models.DateField(default=datetime.datetime.today)
    amount = models.CharField(max_length=100,blank=True)
    
    def __str__(self) -> str:
        return self.user.username
    
class OrderItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    product = models.CharField(max_length=200)
    image = models.ImageField(upload_to='assets/img/')    
    quantity = models.IntegerField()
    price = models.IntegerField()
    total = models.IntegerField()
    
    def __str__(self) -> str:
        return self.order.user.username
    
class Event(models.Model):
    event_name = models.CharField(max_length=200)
    event_date = models.DateTimeField()
    
    def __str__(self) -> str:
        return self.event_name
    

    