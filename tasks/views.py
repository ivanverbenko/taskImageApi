from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Task, Image
from .serializers import TaskSerializer, ImageSerializer, TaskListSerializer
from .services import add_image_and_process, calculate_statistics


class TaskPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    http_method_names = ["get", "post", "delete"]
    pagination_class = TaskPagination

    def get_serializer_class(self):
        if self.action == "list":
            return TaskListSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=["post"])
    def add_image(self, request, pk=None):
        """
        Добавляет изображение в задание и запускает его обработку.
        """
        task = self.get_object()
        data = {
            "task": task.id,
            "image": request.FILES.get("image"),
            "name": request.data.get("name"),
        }
        serializer = ImageSerializer(data=data, context={'task': task})

        if serializer.is_valid():
            serializer.save()  # save() обрабатывает и сохраняет изображение
            return Response(
                {"message": "Image added and processed"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """
        Получает детали задания с вычисленной статистикой.
        """
        task = self.get_object()
        serializer = self.get_serializer(task)
        data = serializer.data

        # Рассчитываем статистику с помощью функции из сервиса
        statistics = calculate_statistics(task)
        data.update(statistics)

        return Response(data)
