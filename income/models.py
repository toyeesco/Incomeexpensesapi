from django.db import models
from authentication.models import User
# Create your models here.

class Income(models.Model):

    SOURCES_OPTIONS = [
        ('SALARY', 'SALARY'),
        ('BUSINESS', 'BUSINESS'),
        ('SIDE-HUSTLES', 'SIDE-HUSTLES'),
        ('PER-TIME JOB', 'PER-TIME JOB'),
        ('OTHERS', 'ORDERS')
    ]

    source = models.CharField(max_length=255, choices=SOURCES_OPTIONS)
    amount = models.DecimalField(max_length=255, max_digits=10, decimal_places=2)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)

    class Meta:
        ordering: ['-date']

    def __str__(self):
        return (self.owner)+'s income'


