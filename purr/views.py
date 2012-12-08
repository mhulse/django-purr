# http://stackoverflow.com/a/712799/922323
try: import simplejson as json
except ImportError: import json

from django import http
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.detail import BaseDetailView

from purr.models import Category

# https://docs.djangoproject.com/en/1.3/topics/class-based-views/#more-than-just-html
class JSONResponseMixin(object):
    
    def render_to_response(self, context):
        
        "Returns a JSON response containing 'context' as payload."
        
        return self.get_json_response(self.convert_context_to_json(context))
    
    def get_json_response(self, content, **httpresponse_kwargs):
        
        "Construct an `HttpResponse` object."
        
        return http.HttpResponse(content, content_type='application/json', **httpresponse_kwargs)
    
    def convert_context_to_json(self, context):
        
        "Convert the context dictionary into a JSON object."
        
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        
        return json.dumps(context, indent=4)

class Purr(JSONResponseMixin, BaseDetailView):
    
    def get(self, request, *args, **kwargs):
        
        # Get the category slug URI string:
        hierarchy = self.kwargs['hierarchy']
        
        # Trim leading/trailing slashes and convert hierarchy to list of slugs:
        category_slugs = hierarchy.strip('/').split('/')
        
        # Initialize category list:
        categories = []
        
        # Loop over slug list:
        for slug in category_slugs:
            
            if not categories:
                
                # There's no parent:
                parent = None
                
            else:
                
                # Set parent to the next category object:
                parent = categories[-1]
            
            # Get the category object:
            category = get_object_or_404(Category, slug__iexact=slug, parent=parent,)
            
            # Append the category object to the category list:
            categories.append(category)
        
        # Create response context dict:
        context = {
            'category': category.name, # Simply adding the context's name.
        }
        
        # Generate JSON response:
        return self.render_to_response(context) # We're done!
