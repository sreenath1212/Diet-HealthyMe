from django.db import models

class emodel(models.Model):
    UID = models.IntegerField()
    ENAME = models.CharField(max_length=100)
    ETYPE = models.CharField(max_length=50)
    EDESC = models.CharField(max_length=6000)
    EVIDEO = models.FileField(upload_to='video')

    class Meta:
        db_table = 'exercise'

class ymodel(models.Model):
    YID = models.AutoField(primary_key=True)
    UID = models.IntegerField()
    YNAME = models.CharField(max_length=100)
    YTYPE = models.CharField(max_length=50)
    YDESC = models.CharField(max_length=6000)
    YPIC = models.FileField(upload_to='pictures')

    class Meta:
        db_table = 'yoga'

