from django.contrib import admin
from .models import *


class Product_Images(admin.TabularInline):
    model = Product_Image

class Additional_Informations(admin.TabularInline):
    model = Additional_Information

class Product_Admin(admin.ModelAdmin):
    inlines =(Product_Images,Additional_Informations)
    list_display=('product_name','price','Categories','color','section')
    list_editable= ('Categories','section','color')

class OrderItemTabularInline(admin.TabularInline):
    model = OrderItem
    
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemTabularInline]
    list_display=['firstname','phone','email','payment_id','paid','date']       
    search_fields =['firstname','email','payment_id']
    
    
admin.site.register(Slider)
admin.site.register(BannerArea)
admin.site.register(Main_Category)
admin.site.register(Category)
admin.site.register(Sub_Categories)
admin.site.register(Section)
admin.site.register(Product,Product_Admin)
admin.site.register(Product_Image)
admin.site.register(Additional_Information)
admin.site.register(Color)
admin.site.register(Brand)
admin.site.register(Event)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)