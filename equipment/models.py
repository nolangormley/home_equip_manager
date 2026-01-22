from django.db import models
from django.utils import timezone

class Equipment(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'Needs Maintenance'),
        ('broken', 'Broken'),
        ('stored', 'Stored'),
        ('retired', 'Retired'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    image = models.ImageField(upload_to='equipment/', blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    purchase_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('icebox', 'Icebox'),
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]
    
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.equipment.name}"

class Update(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='updates')
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Update on {self.equipment.name} at {self.timestamp}"
