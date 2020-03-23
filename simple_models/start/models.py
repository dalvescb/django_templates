from django.db import models

# defines a Relation SPerson
# with attributes (name,age)
#   i.e a table
#        | name | age  |
#        +-------------+
#        | .... |  ... |
#        | .... |  ... |
class Person(models.Model):
    # use a CharField to store Strings data (must set max length)
    name = models.CharField(max_length=30)
    # use an IntegerField to store Integer data
    age = models.IntegerField()
