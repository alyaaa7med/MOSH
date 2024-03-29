from decimal import Decimal 
from rest_framework import serializers 
from .models import Product , Collection , Review , Cart , CartItem

#external representation for the Product model  ,which may differ from the internal (model )

class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length= 255 )


# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length= 255 )
#     unit_price = serializers.DecimalField(max_digits=6,decimal_places=2, source = 'price')# django will look for the same field name in Product model 
#     price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')# define a method here and it will return a value to this field 
#     # serializing the id of the related collection in product 
#     collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all())
#     # serializing the string representation  of the related collection in product 
#     collection = serializers.StringRelatedField()
#     # serializing nested relationship  
#     collection = CollectionSerializer()
#     # serializing the hyperlink  to the relationship 
#     collection = serializers.HyperlinkedRelatedField(
#         query_set=Collection.objects.all(),
#         view_name= 'collection-detail')




#     def calculate_tax (self , prod:Product):
#         return prod.price * Decimal(1.2) 


class ProductSerializer(serializers.ModelSerializer): # extend model serializer to minimize the code 
    model = Product 
    fields= ['id','title','price','price_with_tax','collection']
    # here only add fields not in the product model class ^_^
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')# define a method here and it will return a value to this field 
    # if you do not write that ,then it will serialize the id of collection
    collection = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name= 'collection-detail')

    def calculate_tax (self , prod:Product):
        return prod.price * Decimal(1.2) 
    
    # example to override the validate method in the serializer 
    # def validate(self, data) :
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError('Password does not match ')
    #     return data 


class ReviewSerializer(serializers.ModelSerializer): 
    class Meta :
        model = Review 
        fields= ['id','name','description','date','product']


class CartItemSerializer (serializers.ModelSerializer):
    class Meta :
        model = CartItem 
        fileds = ['id','product','quantity'] # will return the id of the product , to return the product itself u should redefine the product 
class CartSerializer (serializers.ModelSerializer):

    class Meta :
        items = CartItemSerializer(many = True )
        total_price = serializers.SerializerMethodField()

    def get_total_price(self,cart):
        return sum ([item.quantity * item.quantity.unit_price for item in cart.items.all() ]) 
    class Meta : 
        model = Cart
        # fields = ['id','items']  # no need to return the created_at # items : will return the id of items 
        fields = ['id','items','total_price']
