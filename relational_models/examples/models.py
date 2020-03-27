from django.db import models

# Example: Explicit Primary Key
class ProgrammingLanguage(models.Model):
  PARADIGM_CHOICES = (
      ("FR","Functional"),
      ("IM","Imperative"),
      ("MX","Mixed"),
  )

  name = models.CharField(max_length=30,primary_key=True)
  paradigm = models.CharField(max_length=10,
                              choices=PARADIGM_CHOICES,
                              default="IM")
  is_oo = models.BooleanField()

# Example: Implicit Primary Key
class TestModel(models.Model):
   # id   = models.AutoField(primary_key=True)
     # automatically generated (not necessary to add)
   name = models.CharField(max_length=30)

# Example: One-To-Many Relationship
class Company(models.Model):
    name = models.CharField(max_length=15)

class Employee(models.Model):
    name = models.CharField(max_length=30)
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE)

# Example: Many-To-Many Field
class Class(models.Model):
   name = models.CharField(max_length=30)

class Student(models.Model):
   name = models.CharField(max_length=30)
   classes = models.ManyToManyField(Class)

# Example: Recursive Field
class Person(models.Model):
   name    = models.CharField(max_length=30)
   friends = models.ManyToManyField('self')
          # self references the Person model

# Example: One-To-One Field
class Country(models.Model):
    name = models.CharField(max_length=30)

class President(models.Model):
    name = models.CharField(max_length=30)
    corrupt = models.BooleanField(default=True)
    country = models.OneToOneField(Country,
                                   on_delete=models.CASCADE,
                                   primary_key=True)

