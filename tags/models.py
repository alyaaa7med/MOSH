from django.db import models
from django.contrib.contenttypes.models import ContentType 
from django.contrib.contenttypes.fields import GenericForeignKey 


class Tag(models.Model):
    label= models.CharField(max_length=255)

class TaggedItem(models.Model): #for generic relationship use content
    tag=models.ForeignKey(Tag,on_delete=models.CASCADE) #all  Items should be tagged , so if the tag is deleted , the item should also be deleted 
    #generic relation ,you need content object ==> to get it u need the  model and the id (which should be the primary key ) 
    content_type= models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField() #this id should be the primary key 
    content_object = GenericForeignKey()