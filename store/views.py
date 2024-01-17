from django.shortcuts import render
from django.http import HttpResponse 
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from .models import Product , Collection
from .serializers import ProductSerializer
from django.shortcuts import get_object_or_404

#view function take request and return response 
@api_view()
def product_list(request) :
    query_set = Product.objects.all()
    serializer= ProductSerializer(query_set, many = True,context={'request':'request'})
    return Response(serializer.data)  

@api_view()
def product_detail(request,id ) :
    product = get_object_or_404(Product,pk=id)
    serializer = ProductSerializer(product) #convert object to dictionary , here we instantiating the serializer
    return Response(serializer.data) #get the dictionary 

@api_view()
def collection_detail(request,pk ) : #here it will be pk not id as it is for the serializing relationship
    collection = get_object_or_404(Collection,pk=id)
    serializer = ProductSerializer(collection) #convert object to dictionary 
    return Response(serializer.data) #get the dictionary 

