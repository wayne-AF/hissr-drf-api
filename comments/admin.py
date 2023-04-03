# Third party imports
from django.contrib import admin

# Internal imports
from .models import Comment

admin.site.register(Comment)
