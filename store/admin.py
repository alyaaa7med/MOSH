from django.contrib import admin

from . import models 

# why the cycle relationship have not been handeled ???????????????????????????
# note : you can change the list display 
admin.site.register(models.Collection)
admin.site.register(models.Product)
admin.site.register(models.Order)