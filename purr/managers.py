from django.db import models

class CategoryManager(models.Manager):
    
    def root_categories(self, **kwargs):
        
        "Get all root targets."
        
        return self.filter(parent__isnull=True, **kwargs)
