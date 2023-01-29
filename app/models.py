from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# RiverBasin
class RiverBasin(models.Model):
    name = models.CharField(max_length=120)
   
    def __str__(self):
        return str(self.name)

# Model for data storage this is for grounwater data (Change name to location)
class Location(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    basin = models.ForeignKey(RiverBasin, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    # This is participants relation. For example one user can participate in many location
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-updated', '-created']

    def get_absolute_uls(self):
        return reversed('location:detail', kwargs={'pk', self.pk})

    def __str__(self):
        return str(self.name)

# Model for storing data
class Data(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    # This is for file users many to many relation. Example one user can upload many fiiles
    contributors = models.ManyToManyField(User, related_name='contributors', blank=True)
    location_files = models.ManyToManyField(Location, related_name='location_files', null=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    # Directory for files
    dir = models.FileField(upload_to='csv')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated', '-created']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    # For deleting file on local machine
    def delete(self, *args, **kwargs):
        self.dir.delete()
        super().delete(*args, **kwargs)

    def get_absolute_uls(self):
        return reversed('graph:detail', kwargs={'pk', self.pk})

    def __str__(self):
        return str(self.name)

# Nisi jos razradio
# Model for storing and making graphs from data. It uses groundwater levels 
class Graph(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Change location to File
    data = models.ForeignKey(Data, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    # Directory of files
    dir = models.ImageField(upload_to='graphs')
    description = models.TextField(max_length=500, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    # For deleting file on local machine
    def delete(self, *args, **kwargs):
        self.dir.delete()
        super().delete(*args, **kwargs)

    def get_absolute_uls(self):
        return reversed('graph:detail', kwargs={'pk', self.pk})

    def __str__(self):
        return str(self.name)

