from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType 
from django.db.models.aggregates import Count , Max , Min , Avg 
from django.db.models.functions import Concat
from django.db import transaction
from django.db.models import Value 
from store.models import Product , Order , Customer , OrderItem
from tags.models import TaggedItem


def say_hello(request):
    # prod = Product.objects.filter(pk=0).exists() #return boolean  
    query_set = Product.objects.filter(price__gt=20)
    # query_set = Product.objects.filter(collection__id=20) #filter with relationship 
    # we can filter with range  , contain , icontain =>insensitive , isnull , ... 
    query_set = Product.objects.order_by('price','-title') #assending , descending
    query_set = Product.objects.filter().all()[:5] #0 offset->4 limit 
    query_set = Product.objects.only('id','title') #optimize the query to get instances of Product not dictionary like in values() 
    query_set = Product.objects.all() # load : django will query the Product table not the related tables like Collections , Promotions ,if you order it in html program will hang 
    # preload (=means that will not load after rendering html )
    # select_related :1 prod in 1 colection
    query_set = Product.objects.select_related('collection').all() # django will query the Product table and apply join to  Collections 
    # preload + select_related as collection is 1 prod in m promotions 
    query_set = Product.objects.prefetch_related('promotions').all() # inner join
    # get the last 5 orders with their customer and include the product لاحظ ان نفس الترتيب بتاع الكويرى هو الكود
    query_set = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]  # reverse relationship is very helpful 
    # aggregate function can be applied on a column 
    prod = Product.objects.filter(collection__id=1).aggregate(count_kwarg = Count('id'))
    # database function 
    query_set = Customer.objects.annotate(full_name= Concat('first_name',Value(' '),'last_name'))

    #generic relationship 
    content_type=ContentType.objects.get_for_model(Product)
    TaggedItem.objects.select_related('tag').filter( # preload the tag table 
        content_type=content_type,
        object_id=1
    )
    # we can create object , update , delete 
     # i will skip them 
    
    # Transactions : make changes in atomic way 
     # create the parent record then child record 
    with transaction.atomic():
        order = Order()
        order.customer_id=1 
        order.save()

        item = OrderItem()
        item.order=order 
        item.product_id=1
        item.quantity=1
        item.unit_price=10
        item.save()
    # we can execute row sql database command 
    query_set = Product.objects.raw('SELECT * FROM store_product')
    

    return render(request, 'hello.html',{'name':'Alyaa','products':list(query_set)},) #convert so that the key in query_set reflects to be  the value in products 