from django.shortcuts import render
from django.http import HttpResponse 
from django_filters.rest_framework import DjangoFilterBackend 
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.filters import SearchFilter , OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from .models import Product , Collection , Review , CartItem , Cart
from .serializers import ProductSerializer , ReviewSerializer , CartSerializer , CartItemSerializer

#view function take request and return response 
@api_view(['GET','POST']) #get need serialization , post need deserialization
def product_list(request) :
    if request.method=='GET':
        query_set = Product.objects.all()
        serializer= ProductSerializer(query_set, many = True,context={'request':'request'})
        return Response(serializer.data)  
    elif request.method=='POST':
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data() # this validation is at the object level , (for comparing 2 fields you should override this method in the serializer )
            serializer.save()
            return Response('ok')
        # note : end point accept data , return data with status code 
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])
def product_detail(request,id ) :
    product = get_object_or_404(Product,pk=id)
    if request.method=='GET':
        serializer = ProductSerializer(product) #convert object to dictionary , here we instantiating the serializer
        return Response(serializer.data) #get the dictionary to the client 
    
    elif request.method=='PUT':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    elif request.method=='DELETE':
        # before we delete , we should check that it is not referenced by any foreign key
        if product.orderitem_set.count()>0:
            return Response({'error':'object can not be deleted'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete() 
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def collection_detail(request,pk ) : #here it will be pk not id as it is for the serializing relationship
    collection = get_object_or_404(Collection,pk=id)
    serializer = ProductSerializer(collection) #convert object to dictionary 
    return Response(serializer.data) #get the dictionary 

#for viewset , filtering , but is not completed vid: 29
class ProdcutViewSet(ModelViewSet):
    serializer_class = ProductSerializer

    # i should override this method ,as i will use filter method
    def get_queryset(self):
        queryset = Product.objects.all()
        collection_id = self.request.query_params['collection_id']

        if collection_id is not None :
            queryset = queryset.filter(collection_id=collection_id)
        return queryset
    
#ModelViewSet ==> CRUD 
class ProdcutViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    # filterset_class = ProductFilter # i do not create this file 
    search_fields= ['title','description']
    ordering_fields = ['price','last_update']
    # pagination_class= PageNumberPagination #local pagination

class CartViewSet (ModelViewSet): # no need for all the CRUD , u can customize the ModelViewSet 
    queryset = Cart.objects.all()
    serializer_class=CartSerializer 

class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer 
     
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])  
   
class ReviewClass(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
