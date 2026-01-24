from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

"""
# --- Helper Models (Now User-Specific) ---
class Category(models.Model):
    # Added: Each category belongs to a specific user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        # Optional: Prevent duplicates for the SAME user, but allow different users to have same category names
        unique_together = ('user', 'title')

    def __str__(self):
        return self.title


class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'title')

    def __str__(self):
        return self.title


class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'title')

    def __str__(self):
        return self.title


# --- Main Project Model ---
class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    # These remain ManyToMany, but we will filter them in the Forms/Views later
    categories = models.ManyToManyField(Category, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)

    estimated_profit = models.FloatField(default=0, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# --- Notes, Stages, and Tasks remain the same ---
# They don't need a User field directly because they link to Project,
# and Project already links to User.
class Note(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Note for {self.project.title}"

class Stage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='stages')
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created']

    def __str__(self):
        return f"{self.project.title} - {self.name}"

class Task(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
"""