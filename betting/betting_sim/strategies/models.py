from django.db import models
from django.contrib.auth.models import User
import os


class Strategy(models.Model):
    """
    Model for storing custom betting strategies uploaded by users.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='strategies')
    file = models.FileField(upload_to='strategies/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Strategies'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def file_name(self):
        return os.path.basename(self.file.name)
    
    def save(self, *args, **kwargs):
        # Ensure file has .py extension
        if not self.file.name.endswith('.py'):
            self.file.name = f"{self.file.name}.py"
        super().save(*args, **kwargs) 