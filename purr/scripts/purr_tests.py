import pprint

from django.shortcuts import get_object_or_404

from purr.models import Category

# $ python manage.py runscript purr_tests

def run():
    
    """
    category = Category.objects.get(slug__iexact='business')
    print category.parent # None
    """
    
    # Example: /business/sports/eating-contest/pizza/
    #print Category.objects.get(slug__iexact='business', parent__slug__exact=None,)           # Business
    #print Category.objects.get(slug__iexact='sports', parent__slug__exact='business',)       # BUSINESS | Sports
    #print Category.objects.get(slug__iexact='eating-contest', parent__slug__exact='sports',) # BUSINESS | SPORTS | Eating contest
    #print Category.objects.get(slug__iexact='pizza', parent__slug__exact='eating-contest',)  # BUSINESS | SPORTS | EATING CONTEST | Pizza
    
    
    hierarchy = '/business/sports/eating-contest/pizza/'
    
    """
    category_slugs = hierarchy.split('/')
    pprint.pprint(category_slugs) # ['', 'business', 'sports', 'eating-contest', 'pizza', '']
    """
    
    """
    category_slugs = hierarchy.strip('/').split('/')
    pprint.pprint(category_slugs) # ['business', 'sports', 'eating-contest', 'pizza']
    """
    
    category_slugs = hierarchy.strip('/').split('/')
    
    categories = []
    
    for slug in category_slugs:
        
        if not categories:
            
            parent = None
            
        else:
            
            parent = categories[-1]
        
        category = get_object_or_404(Category, slug__iexact=slug, parent=parent,)
        
        categories.append(category)
    
    pprint.pprint(categories)
