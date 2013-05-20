# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Review(models.Model):
    id = models.IntegerField(primary_key=True)
    business_id = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50)
    review_text = models.TextField()
    review_date = models.DateField()
    review_clauses = models.TextField()

    class Meta:
        db_table = u'review'

class Users(models.Model):
    user_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    review_count = models.IntegerField()
    class Meta:
        db_table = u'users'

class Business(models.Model):
    business_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    full_address = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    review_count = models.IntegerField()
    categories = models.CharField(max_length=20)
    class Meta:
        db_table = u'business'

class Rc(models.Model):
    review = models.ForeignKey(Review,db_column = 'id')
    pairs = models.TextField()
    tuples = models.TextField()
    coref = models.TextField()
    class Meta:
        db_table = u'rc'

