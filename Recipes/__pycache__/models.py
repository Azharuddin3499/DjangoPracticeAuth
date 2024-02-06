from django.db import models

class MyRecipes(models.Model):
    r_name=models.CharField(max_length =50)
    r_description=models.TextField()
    r_img=models.ImageField(upload_to='userimages')
    