# api_yamdb
api_yamdb

добавлено
djangorestframework-simplejwt==4.7.2

сейчас емейлы сохраняются в папку api_yamdb\sent_emails
так что confirmation_code получать пока что там

## пока что у нас стоит в settings 
значит всем все доступно
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],


### Регистрация нового пользователя
Получить код подтверждения на переданный email.
Права доступа: Доступно без токена.
Использовать имя 'me' в качестве username запрещено.
Поля email и username должны быть уникальными.

*   `POST: /api/v1/auth/signup/
Content-Type: application/json

        {
        "email": "string",
        "username": "string"
        }


### Получение JWT-токена в обмен на username и confirmation code.
    
*   `POST: /api/v1/auth/token/
Content-Type: application/json

        {
        "username": "string",
        "confirmation_code": "string"
        }
