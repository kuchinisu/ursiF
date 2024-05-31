from django.db import models
from apps.user.models import UserAccount

class Tags(models.Model):
    nombre = models.CharField(max_length=50)
    usuario = models.ForeignKey(UserAccount, related_name='tags_usuario', on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre
    
