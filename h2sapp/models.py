from django.db import models

# Create your models here.

class ModerationRequest(models.Model):
    url = models.URLField(blank=True, null=True)
    document = models.FileField(upload_to="documents/", blank=True, null=True)
    analysis_result = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url if self.url else self.document.name


class ModeratedText(models.Model):
    text = models.TextField()
    is_hateful = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{'Hateful' if self.is_hateful else 'Safe'} - {self.text[:50]}"