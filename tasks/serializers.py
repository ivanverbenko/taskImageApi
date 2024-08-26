# tasks/serializers.py

from rest_framework import serializers
from .models import Task, Image, Face
from .services import add_image_and_process


class FaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Face
        fields = ["bounding_box", "gender", "age"]


class ImageSerializer(serializers.ModelSerializer):
    faces = FaceSerializer(many=True, read_only=True)
    image = serializers.ImageField(write_only=True)

    class Meta:
        model = Image
        fields = ["name", "faces", "image"]


    def save(self, **kwargs):
        task = self.context.get('task')
        if not task:
            raise serializers.ValidationError("Task must be provided in the context.")
        try:
            add_image_and_process(task, self.validated_data["image"], self.validated_data["name"])
        except Exception as e:
            raise serializers.ValidationError(f"Ошибка при обработке изображения: {str(e)}")

class TaskSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ["id", "created_at", "images"]


class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class TaskListSerializer(serializers.ModelSerializer):
    images = ImageListSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = "id", "created_at", "images",
