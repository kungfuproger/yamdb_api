# api_yamdb
api_yamdb


    #### Получение JWT-токена в обмен на username и confirmation code.
    
*   `POST: /api/v1/auth/token/
Content-Type: application/json

        {
        "username": "string",
        "confirmation_code": "string"
        }
