# Uncomment the following imports before adding the Model code

# from django.db import models
# from django.utils.timezone import now
# from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many
# Car Models, using ForeignKey field)
# - Name
# - Type (CharField with a choices argument to provide limited choices
# such as Sedan, SUV, WAGON, etc.)
# - Year (IntegerField) with min value 2015 and max value 2023
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator

# Creating a car make Django Model  class CarMake(models.Model):
# Name, Description, A _str_ method to print a car make object
# A CarMake model to save some data about a car's make
# A __str__ method to print a car make object

class CarMake(models.Model): #CarMake
    name = models.CharField(max_length=100)
    description = models.TextField()
    #other fields as needed 

    def __str__(self):
        return self.name # Return the name as the string representation

# A CarModel model to save some data about a car's model.
#A __str__ method to print the car make and car model object

class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE) # Many-to-One relationship
    name = models.CharField(max_length=100)
    # type = models.CharField(max_length=50)
    # year = models.IntegerField()
    # dealer_id = models.IntegerField()

    CAR_TYPES = [   
        ('SEDAN', 'Sedan'),
        ('SUV', 'Suv'),
        ('WAGON', 'Wagon'),
        ('COUPE', 'Coupe'),
        # ('TRUCK', 'Truck'),
                 # Add more choices as required
                 ]
    # car_type = models.CharField(max_length=10, choices=CAR_TYPES, default='SUV' )# type should be change to car type
    type = models.CharField(max_length=10, choices=CAR_TYPES, default='SUV')
    year = models.IntegerField(default=2023,
                            validators=[
                                MaxValueValidator(2023),
                                MinValueValidator(2015)
                            ])
# Other fields as needed
# A __str__ method to print the car make and car model object

def __str__(self):
   return self.name # Return the name as the string representation
    # return f"{self.name} ({self.car_make.name})" # gemini advice
#  def __str__(self):
#         return f"{self.name} ({self.year})"
# Note: The --run-syncdb allows creating tables for apps without migrations.

class Dealer(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    zip_state = models.CharField(max_length=20)
    has_service_center = models.BooleanField(default=False)  # Added this field

    def __str__(self):
        return self.name