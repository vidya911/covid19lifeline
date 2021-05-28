from django.db import models
from django.utils.text import slugify


class BasicConfiguration(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class NameBaseConfig(BasicConfiguration):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(NameBaseConfig, self).save(*args, **kwargs)

    def __str__(self):
        return f"name: {self.name} slug: {self.slug}"


class ResourceType(NameBaseConfig):
    pass

class ServiceType(NameBaseConfig):
    pass


class State(models.Model):
    """
    get state list from: https://raw.githubusercontent.com/thatisuday/indian-cities-database/master/cities.json
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(State, self).save(*args, **kwargs)

    def __str__(self):
        return f"name: {self.name} slug: {self.slug}"


class City(models.Model):
    """
    get city list from: https://raw.githubusercontent.com/thatisuday/indian-cities-database/master/cities.json
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    class Meta:
        unique_together = [('slug', 'state')]


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(City, self).save(*args, **kwargs)

    def __str__(self):
        return f"name: {self.name} slug: {self.slug}"
