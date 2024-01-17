from decimal import Decimal 
from rest_framework import serializers 
from .models import Product , Collection 

#external representation for the Product model  ,which may differ from the internal (model )

class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length= 255 )


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length= 255 )
    unit_price = serializers.DecimalField(max_digits=6,decimal_places=2, source = 'price')# django will look for the same field name in Product model 
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')# define a method here and it will return a value to this field 
    # serializing the id of the related collection in product 
    collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all())
    # serializing the string representation  of the related collection in product 
    collection = serializers.StringRelatedField()
    # serializing nested relationship  
    collection = CollectionSerializer()
    # serializing the hyperlink  to the relationship 
    collection = serializers.HyperlinkedRelatedField(
        query_set=Collection.objects.all(),
        view_name= 'collection-detail')




    def calculate_tax (self , prod:Product):
        return prod.price * Decimal(1.2) 
