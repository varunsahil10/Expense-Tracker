from django.db import models
import uuid
from django.contrib.auth.models import User

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Transaction(BaseModel):
    description = models.CharField(max_length=100, blank=False, null=False)
    amount = models.DecimalField(max_digits=10,decimal_places=2, blank=False, null=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['created_at']

    def isNegative(self):
        return self.amount < 0