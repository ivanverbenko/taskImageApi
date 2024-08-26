# Task image API Service

REST API для управления задачами и работы с изображениями, которые загружаются в эти задачи. API позволяет не только добавлять и удалять задачи и изображения, но и автоматически распознавать лица на изображениях, определять их пол и возраст, а также собирать статистику на основе этих данных.

## Запуск сервиса


```bash
docker-compose up --build
```

После успешного запуска сервис будет доступен по адресу:

```
http://localhost:8000/
```

## Аутентификация

API защищено с помощью HTTP Basic Auth. Для доступа ко всем ручкам, кроме `http://localhost:8000/swagger/`, требуется логин и пароль.

### Swagger

Для работы с API через интерфейс Swagger необходимо авторизоваться через кнопку **Authorize**.
Креды для авторизации можно найти в файле `.env`:

```plaintext
BASIC_AUTH_USERNAME=user
BASIC_AUTH_PASSWORD=pass
```

### Postman

Для работы с API через Postman необходимо выбрать тип аутентификации Basic Auth. Пример настройки аутентификации в Postman:


### Примеры запросов с использованием cURL

#### Получение списка задач

```bash
curl --location 'http://localhost:8000/api/tasks/' \
--header 'Authorization: Basic dXNlcjpwYXNz'
```

#### Добавление задачи

```bash
curl --location --request POST 'http://localhost:8000/api/tasks/' \
--header 'Authorization: Basic dXNlcjpwYXNz'
```

#### Получение детальной информации по задаче

```bash
curl --location 'http://localhost:8000/api/tasks/{task_id}' \
--header 'Authorization: Basic dXNlcjpwYXNz'
```

#### Добавление изображения в задачу
через Swagger не работает
```bash
curl --location 'http://localhost:8000/api/tasks/4/add_image/' \
--header 'Authorization: Basic dXNlcjpwYXNz' \
--form 'image=@"/E:/1.jpg"' \ 
--form 'name="image_name"'
```
В постмане дополнительно выбрать select files


Изображения сохраняются на диске по адресу `media/images/{task_id}/`. В том числе, все изменения в локальной файловой системе будут отражаться в контейнере, так как волюм прокинут.

##  .env

Креды FACE_CLOUD_EMAIL и FACE_CLOUD_PASSWORD можно задать через файл .env или напрямую через docker-compose.yml
Приоритет отдается значениям из docker-compose, остальные в .env