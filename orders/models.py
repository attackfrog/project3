from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Pizza(models.Model):
    name = models.CharField(max_length=64)
    numToppings = models.IntegerField()
    priceSmall = models.DecimalField(max_digits=5, decimal_places=2)
    priceLarge = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name}"

class PizzaTopping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Sub(models.Model):
    name = models.CharField(max_length=64)
    specialToppings = models.BooleanField()
    priceSmall = models.DecimalField(max_digits=5, decimal_places=2)
    priceLarge = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name}"

class SubTopping(models.Model):
    name = models.CharField(max_length=64)
    isSpecial = models.BooleanField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name}"

class OneSize(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name}"

class Platter(models.Model):
    name = models.CharField(max_length=64)
    priceSmall = models.DecimalField(max_digits=5, decimal_places=2)
    priceLarge = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name}"

class Order(models.Model):
    types = (
        ("pizza", "Pizza"),
        ("sub", "Sub"),
        ("oneSize", "One-size Meal"),
        ("platter", "Platter"),
    )
    sizes = (
        ("small", "Small"),
        ("large", "Large")
    )
    category = models.CharField(max_length=15, choices=types)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, blank=True, null=True, related_name="+")
    pizzaToppings = models.ManyToManyField(PizzaTopping, blank=True, related_name="+")
    sub = models.ForeignKey(Sub, on_delete=models.CASCADE, blank=True, null=True, related_name="+")
    subToppings = models.ManyToManyField(SubTopping, blank=True, related_name="+")
    oneSize = models.ForeignKey(OneSize, on_delete=models.CASCADE, blank=True, null=True, related_name="+")
    platter = models.ForeignKey(Platter, on_delete=models.CASCADE, blank=True, null=True, related_name="+")
    size = models.CharField(max_length=5, choices=sizes)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="order")
    specialRequest = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user} purchasing a {self.category} for {self.price}"
