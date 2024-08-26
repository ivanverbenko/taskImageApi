from django.db import models


class Task(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Task {self.id}"


def get_upload_to(instance, filename):
    return f"images/task_{instance.task_id}/{filename}"


class Image(models.Model):
    task = models.ForeignKey(Task, related_name="images", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False, blank=False)
    image = models.ImageField(upload_to=get_upload_to)

    def __str__(self):
        return f"{self.name} {self.id}"


class Face(models.Model):
    image = models.ForeignKey(Image, related_name="faces", on_delete=models.CASCADE)
    bounding_box = models.JSONField()
    gender = models.CharField(max_length=10)
    age = models.IntegerField()

    def __str__(self):
        return f"Face {self.id} in {self.image.name}"
