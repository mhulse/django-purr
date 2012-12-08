from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from purr.forms import CategoryAdminForm
from purr.models import Category

#--------------------------------------------------------------------------
#
# Admin models:
#
#--------------------------------------------------------------------------

class CategoryAdmin(admin.ModelAdmin):
    
    #----------------------------------
    # Fields:
    #----------------------------------
    
    fieldsets = [
        
        ('Meta', {
            'fields': (
                'slug',
            ),
            'classes': (
                'collapse',
            ),
        },),
        
        (None, {
            'fields': [
                'parent',
                'name',
                'notes',
            ],
        },),
        
    ]
    
    prepopulated_fields = {
        'slug': ['name',],
    }
    
    #----------------------------------
    # Forms:
    #----------------------------------
    
    form = CategoryAdminForm
    
    #----------------------------------
    # Change lists:
    #----------------------------------
    
    list_display = (
        '__unicode__',
        'parent',
        'name',
        'slug',
    )
    
    list_editable = (
        'name',
        'parent',
        'slug',
    )
    
    list_per_page = 25
    
    search_fields = (
        'name',
        'parent__name',
    )
    
    actions_on_top = True
    
    actions_on_bottom = True
    
    actions_selection_counter = True

#--------------------------------------------------------------------------
#
# Registrations:
#
#--------------------------------------------------------------------------

admin.site.register(Category, CategoryAdmin)
