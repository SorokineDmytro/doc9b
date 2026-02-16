from django.db import models
from django.utils.text import slugify

# Abstract base model to add created_at and updated_at to each model that inherits from it
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Space model
class Space(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    
    # Override the method to automatically generate slug from name if not provided
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    # Override the method for better representation (Space object (0) -> Space: Archistoire)
    def __str__(self):
        return self.name

# User_category model
class UserCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
# Page model
class Page(TimeStampedModel):
    space = models.ForeignKey(Space, related_name='pages', on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self', 
        related_name='children', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    # Many-to-many relationship with UserCategory to allow categorization of pages
    categories = models.ManyToManyField(UserCategory, related_name='pages', blank=True)

    # Ensure to have unique slug per space (since the slug can't be unique across all pages) && order by order && title (alphabetically)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["space", "slug"],
                name="unique_page_slug_per_space"
            )
        ]
        ordering = ['order', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.space.name} / {self.title}"