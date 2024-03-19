from django.db import models

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    product_price = models.IntegerField()
    product_image = models.ImageField(upload_to='images/')
    product_description = models.CharField(max_length=1000)
    product_category = models.CharField(max_length = 30)

    def __str__(self):
        return self.product_name






