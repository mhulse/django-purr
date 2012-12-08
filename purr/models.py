import datetime

from django import forms
from django.core import urlresolvers
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from purr import managers

#--------------------------------------------------------------------------
#
# Abstract:
#
#--------------------------------------------------------------------------

class Base(models.Model):
    
    #----------------------------------
    # All database fields:
    #----------------------------------
    
    # Hidden:
    created  = models.DateTimeField(auto_now_add=True, editable=False,)
    modified = models.DateTimeField(auto_now=True, editable=False,)
    
    # Base:
    notes = models.TextField(_(u'notes'), blank=True, help_text=_(u'Not published.'),)
    
    #----------------------------------
    # Class Meta:
    #----------------------------------
    
    class Meta:
        
        abstract = True
        get_latest_by = 'modified'
    
    #----------------------------------
    # Custom methods:
    #----------------------------------
    
    @property
    def is_modified(self):
        
        return self.modified > self.created

#--------------------------------------------------------------------------
#
# Models:
#
#--------------------------------------------------------------------------

class Category(Base):
    
    #----------------------------------
    # All database fields:
    #----------------------------------
    
    # Meta:
    slug = models.SlugField(max_length=255, help_text=_(u'Short descriptive unique name for use in urls.'),)
    
    # Base:
    name = models.CharField(_(u'name'), max_length=200, help_text=_(u'Short descriptive name for this category.'),)
    
    # Foreign keys:
    parent = models.ForeignKey('self', null=True, blank=True, related_name='child',)
    
    #----------------------------------
    # Custom manager attributes:
    #----------------------------------
    
    objects = managers.CategoryManager()
    
    #----------------------------------
    # Class Meta:
    #----------------------------------
    
    class Meta:
        
        ordering = ['parent__name', 'name',]
        unique_together = ('slug', 'parent',)
        verbose_name = _('category',)
        verbose_name_plural = _('categories',)
    
    #----------------------------------
    # def __XXX__()
    #----------------------------------
    
    def __unicode__(self):
        
        name_list = [category.name.upper() for category in self._recurse_for_parents(self)]
        
        name_list.append(self.name)
        
        return _(u'%s') % self.get_separator().join(name_list)
    
    #----------------------------------
    # def save()
    #----------------------------------
    
    def save(self, **kwargs):
        
        if self.id:
            
            if self.parent and self.parent_id == self.id:
                raise forms.ValidationError(_(u'You may not save a category in itself!'))
            
            for p in self._recurse_for_parents(self):
                
                if self.id == p.id:
                    raise forms.ValidationError(_(u'You may not save a category in itself!'))
        
        if not self.slug:
            self.slug = slugify(self.name)
        
        super(Category, self).save(**kwargs) # Call the "real" save()
    
    #----------------------------------
    # def get_absolute_url()
    #----------------------------------
    
    def get_absolute_url(self):
        
        parents = self._recurse_for_parents(self)
        
        slug_list = [category.slug for category in parents]
        
        if slug_list:
            
            slug_list = '/'.join(slug_list) + '/'
        
        else:
            
            slug_list = ''
        
        return urlresolvers.reverse('purr_category_purr', kwargs={'hierarchy' : slug_list,},)
    
    #----------------------------------
    # Custom methods:
    #----------------------------------
    
    def parents(self):
        
        return self._recurse_for_parents(self)
    
    #----------------------------------
    
    def children(self):
        
        return self.category_set.all().order_by('name')
    
    #----------------------------------
    
    def get_separator(self):
        
        return ' | '
    
    #----------------------------------
    
    def _recurse_for_parents(self, category_obj):
        
        p_list = []
        
        if category_obj.parent_id:
            
            p = category_obj.parent
            p_list.append(p)
            
            if p != self:
                
                more = self._recurse_for_parents(p)
                p_list.extend(more)
        
        if category_obj == self and p_list:
            p_list.reverse()
        
        return p_list
    
    #----------------------------------
    
    def _parents_repr(self):
        
        "Representation of categories."
        
        name_list = [category.name for category in self._recurse_for_parents(self)]
        
        return self.get_separator().join(name_list)
        
    _parents_repr.short_description = _(u'Category parents')
    
    #----------------------------------
    
    def get_url_name(self):
        
        "Get all the absolute URLs and names for use in the site navigation."
        
        name_list = []
        url_list = []
        
        for category in self._recurse_for_parents(self):
            
            name_list.append(category.name)
            url_list.append(category.get_absolute_url())
        
        name_list.append(self.name)
        
        url_list.append(self.get_absolute_url())
        
        return zip(name_list, url_list)
    
    #----------------------------------
    
    def _flatten(self, L):
        
        "Taken from a python newsgroup post."
        
        if type(L) != type([]): return [L]
        
        if L == []: return L
        
        return self._flatten(L[0]) + self._flatten(L[1:])
    
    #----------------------------------
    
    def _recurse_for_children(self, node):
        
        children = []
        
        children.append(node)
        
        for child in node.child.all():
            
            if child != self:
                
                children_list = self._recurse_for_children(child)
                children.append(children_list)
        
        return children
    
    #----------------------------------
    
    def get_all_children(self, include_self=False):
        
        "Gets a list of all of the children categories."
        
        children_list = self._recurse_for_children(self)
        
        if include_self:
            ix = 0
        else:
            ix = 1
        
        flat_list = self._flatten(children_list[ix:])
        
        return flat_list
