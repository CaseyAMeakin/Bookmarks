from django.db import models
from django.contrib.auth.models import User
import string

# Create your models here.


class Bookmark(models.Model):
    url = models.CharField(max_length=2000) #bookmark URL
    url_desc = models.CharField(max_length=500) #description of URL
    url_keywords = models.TextField() #comma separated keywords
    url_ip   = models.GenericIPAddressField() #IP of URL when bookmarked
    pub_date = models.DateTimeField('date published') #time that the URL was bookmarked
    accessCount = models.IntegerField(default=0) # total number of time accessed
    user = models.CharField(max_length=100) #user that created this entry
    def __str__(self):
        return self.url + ':' + self.url_desc

    def sorted_by_count(self):
        return self.accessinfo_set.order_by('accessCount')

    def sorted_by_count_reverse(self):
        return self.accessinfo_set.order_by('-accessCount')        


class AccessInfo(models.Model):
    bookmark = models.ForeignKey(Bookmark)
    accessIP = models.GenericIPAddressField() #IP address of user who accessed this bookmark
    accessCount = models.IntegerField(default=0)  # number of times bookmark was accessed by this IP
    
    def __str__(self):
        return self.accessIP + ':count=' + str(self.accessCount)
        
