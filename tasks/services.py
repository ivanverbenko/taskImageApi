# tasks/services.py
import os

from django.db.models import Avg, Count, Prefetch, Q

from .models import Face, Image
from .utils import facecloud
from django.db import transaction


@transaction.atomic
def add_image_and_process(task, image_file, image_name):
    """
    Создает объект Image, отправляет изображение на сервис для обработки
    и сохраняет найденные лица в базе данных.
    """
    image = Image.objects.create(task=task, image=image_file, name=image_name)
    # Отправляем изображение на API FaceCloud для обработки
    try:
        faces_data = facecloud.process_image(image.image.path)
        for face_data in faces_data:
            Face.objects.create(
                image=image,
                bounding_box=face_data["bbox"],
                gender=face_data["demographics"]["gender"],
                age=face_data["demographics"]["age"]["mean"],
            )
    except Exception as e:
        os.remove(image.image.path)
        raise e
    return image


def calculate_statistics(task):
    """
    Рассчитывает статистику по лицам в задании.
    """

    faces = Face.objects.select_related("image__task").filter(image__task_id=task.id)

    total_faces = len(faces)
    total_men = sum(face.gender == "male" for face in faces)
    total_women = sum(face.gender == "female" for face in faces)

    ages_men = [face.age for face in faces if face.gender == "male"]
    ages_women = [face.age for face in faces if face.gender == "female"]

    average_age_men = sum(ages_men) / len(ages_men) if ages_men else 0
    average_age_women = sum(ages_women) / len(ages_women) if ages_women else 0

    return {
        "total_faces": total_faces,
        "total_men": total_men,
        "total_women": total_women,
        "average_age_men": average_age_men,
        "average_age_women": average_age_women,
    }
