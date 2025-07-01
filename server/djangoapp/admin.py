# from django.contrib import admin
# from .models import related models


# Register your models here.

# CarModelInline class

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here

from django.contrib import admin 
# from .models import related models 
from .models import CarMake, CarModel
# Registering models with their respective admins
# Use the admin.site.register()\ function to register each of your models with the admin site.
from .models import Dealer      # Import your Dealer model

admin.site.register(CarMake)
admin.site.register(CarModel)
admin.site.register(Dealer)


## google ai suggestion
# from django.contrib import admin
# from .models import CarMake, CarModel

# class CarMakeAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description') # Display these fields in the list view
#     search_fields = ('name',) # Enable search by name

# class CarModelAdmin(admin.ModelAdmin):
#     list_display = ('make', 'name', 'year')
#     list_filter = ('make', 'year') # Add filters on the sidebar
#     search_fields = ('name',)

# admin.site.register(CarMake, CarMakeAdmin)
# admin.site.register(CarModel, CarModelAdmin)