from django.db import models
from django import forms

# Example Models
PART_CHOICES = (
        ('GPU','GPU'),
        ('RAM','RAM'),
        ('MB','Motherboard'),
        ('CL','Cooler'),
        ('CPU','CPU'),
        )

class PCBrand(models.Model):
    brand_name = models.CharField(max_length=30,primary_key=True)

    def __str__(self):
        return self.brand_name

class PCPart(models.Model):
    part_type = models.CharField(max_length=5,choices=PART_CHOICES,default='GPU')
    name = models.CharField(max_length=30,primary_key=True)
    brand = models.ManyToManyField(PCBrand)

# Used to automatically generate form inputs in template
class PCBrandForm(forms.ModelForm):
    class Meta:
        model = PCBrand
        fields = ['brand_name']

class PCPartForm(forms.ModelForm):
    class Meta:
        model = PCPart
        fields = ['part_type','brand']
