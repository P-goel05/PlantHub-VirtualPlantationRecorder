from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PlantTree(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null= True )
    tree_name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255)
    planted_date = models.DateField()
    height = models.FloatField(help_text="Height of the tree in meters")
    tree_type = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tree_name} planted at {self.location}"
    
class Nursery(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    is_partnered = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class NurseryPlant(models.Model):
    nursery = models.ForeignKey(Nursery, on_delete=models.CASCADE)
    plant_type = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return self.plant_type

class NurseryTool(models.Model):
    nursery = models.ForeignKey(Nursery, on_delete=models.CASCADE)
    tool_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.tool_name
