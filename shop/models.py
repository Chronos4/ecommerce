from django.db import models
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields


class Category(TranslatableModel):
    # name = models.CharField(max_length=200, db_index=True)
    # slug = models.CharField(max_length=200, db_index=True, unique=True)
    translations = TranslatedFields(
        name=models.CharField(max_length=200,
                              db_index=True),
        slug=models.SlugField(max_length=200,
                              db_index=True,
                              unique=True))

    class Meta:
        #ordering = ["name"]
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse("products:list_by_category", kwargs={"category_slug": self.slug})


class Product(TranslatableModel):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products")
    # name = models.CharField(max_length=200, db_index=True)
    # slug = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)
    #description = models.TextField(blank=True)
    translations = TranslatedFields(
        name=models.CharField(max_length=200, db_index=True),
        slug=models.SlugField(max_length=200, db_index=True),
        description=models.TextField(blank=True)
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]
       # index_together = (("id", "slug"),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"id": self.id, "slug": self.slug})
