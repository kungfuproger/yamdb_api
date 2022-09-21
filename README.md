# api_yamdb
api_yamdb

добавлено
djangorestframework-simplejwt==4.7.2


    ### Получение JWT-токена в обмен на username и confirmation code.
    
*   `POST: /api/v1/auth/token/
Content-Type: application/json

        {
        "username": "string",
        "confirmation_code": "string"
        }
