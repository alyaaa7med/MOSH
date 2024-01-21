from django.db import models
from uuid import uuid4
class Promotion(models.Model):
    description= models.CharField(max_length=255)
    discount= models.FloatField()
    #product_set = ... , it is the reverse relationship in many -> many 
    

class Collection(models.Model):
    title = models.CharField(max_length=255)
    # circular relationship between 2 modles, to solve it make the class in string quotes,
    # also,django will create a reverse relationship in the Product model : collection= ----  , which will clashe with the collection field in Collection model 
    featured_product= models.ForeignKey('Product', on_delete=models.SET_NULL,null=True,related_name='+')#'+' means tell django do not make the reverse relationship ,other solution:  you can change its name 
    
    def __str__(self)->str :
        return self.title 
    
class Product(models.Model):
    #sku = models.CharField(max_length=10 , primary_key =True) django will make sku the primary key not use its default which is id 
    title = models.CharField(max_length=255) # note: it will be mapped to  a varchar in database 
    slug = models.SlugField(default='-')
    description = models.TextField()
    price= models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update= models.DateTimeField(auto_now= True) # note : thier is an other auto_now_add => will add for the first time you add it
    collection=models.ForeignKey(Collection,on_delete=models.PROTECT)
    # collection = ............. , this is the reverse , that will clashes 

    # for many -> many : the reverse relationship in Promotion class will be <model_name>_set : Product_set and if you want to change it 
    # use related_name = 'products' , but remeber to have the same name in all classes use it  
    promotions=models.ManyToManyField(Promotion) 
    
    def __str__(self)->str :
        return self.title 
    
    class Meta : 
        ordering = ['title']



        

class Customer(models.Model):
    MEMBERSHIP_BRONZE= 'B'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_CHOICES=[
        (MEMBERSHIP_BRONZE,'Bronze'),
        (MEMBERSHIP_SILVER,'Silver'),
        (MEMBERSHIP_GOLD,'Gold')
    ]
    first_name= models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    email=models.EmailField(unique=True)
    phone= models.CharField(max_length=255)
    birth_date= models.DateField(null = True)
    membership=models.CharField(max_length=1,choices=MEMBERSHIP_CHOICES,default=MEMBERSHIP_BRONZE)

    #to have  more control for the database schema like renaming tables , add index  
    class Meta :
        db_table='store_customers'
        indexes = [
            models.Index(fields=['last_name','first_name'])
        ]

class Order(models.Model):
    PAYMENT_STATUS_SUCCESS='C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_PENDING ='P'
    PAYMENT_CHOICES = [
        (PAYMENT_STATUS_SUCCESS,'Complete'),
        (PAYMENT_STATUS_FAILED,'Failed'),
        (PAYMENT_STATUS_PENDING,'Pending')
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status=models.CharField(max_length=1,choices=PAYMENT_CHOICES,default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT) # you should not delete orders from database 


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT) # reverse relationship : django will make an orderitem_set in Order class 
    product= models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price= models.DecimalField(max_digits=6, decimal_places=2)

class Cart(models.Model):
    # to convert id to a477eewr-55w11-ewr to be hidden from hackers ,so redefine the primary key 
    # id = models.UUIDField(primary_key=True,default=uuid4) #note : you need change datatype as id will be more than as usual 
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
     #you should add the product only one but increase its quantity
    class Meta : 
        unique_together = [['cart','product']] # cart and product is unique together 


class Address(models.Model):
    street =models.CharField(max_length=255)
    city = models.CharField(max_length=255) 
    zip_fd=models.CharField(max_length=10)  
    # #________________________   
    # #one to one relationship |
    # #________________________|                                          # ____________
    # #i do make primary_key=True => so each customer have only an address | one to one |, 
    # #        add   cust_id                                               |____________|
    # #        xlr8  1
    # #        xyz   2  
    # # if you do not make it , then the customer will have more as django will create an id primary key for the address entity
    # #add_id  add   cust_id                 __________________
    # #1       xlr8  1                      |one to many field |
    # #2       xlr   1                      |__________________|
     
    # customer =models.OneToOneField(Customer,on_delete=models.CASCADE,primary_key=True)  
    # # note : django make the reverse relationship on its own in the Customer Entity , no need to make address =models.OneToOneField(----)  

class Review(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description  = models.TextField()
    date = models.DateField(auto_now_add=True)