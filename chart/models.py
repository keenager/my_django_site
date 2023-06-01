from django.db import models

# Create your models here.


class HayulGrowth(models.Model):
    year_month = models.DateField(verbose_name='연월')
    height = models.FloatField(verbose_name='키')
    weight = models.FloatField(verbose_name='몸무게')

    class Meta:
        ordering = ['year_month']
