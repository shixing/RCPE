from django.db import models

# Create your models here.

class TokenizedRc(models.Model):
    '''
    each record is a RC pair: original-id_rank
    '''
    id = models.CharField(max_length=50,primary_key = True)
    tknPair = models.TextField(db_column = 'tknpair')
    
    class Meta:
        db_table = u'tokenizedrc'


class LabelCount(models.Model):
    '''
    each record reflects how many labels are there for specific pairs
    '''
    id = models.CharField(max_length=50,primary_key = True)
    count = models.IntegerField()
    
    class Meta:
        db_table = u'labelcount'


class LabelUser(models.Model):
    '''
    reviewId -> userName -> label
    '''
    reviewId = models.CharField(max_length=50,primary_key = True)
    userName = models.TextField()
    label = models.TextField()
    
    class Meta:
        db_table = 'labeluser'

    
