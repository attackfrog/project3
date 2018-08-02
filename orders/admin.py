from django.contrib import admin

# Register your models here.
from .models import Pizza, PizzaTopping, Sub, SubTopping, OneSize, Platter, Order

admin.site.register(Pizza)
admin.site.register(PizzaTopping)
admin.site.register(Sub)
admin.site.register(SubTopping)
admin.site.register(OneSize)
admin.site.register(Platter)
admin.site.register(Order)
