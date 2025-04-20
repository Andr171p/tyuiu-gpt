# Документация ТИУ-GPT API

# REST API

# Рабочая версия: /api/v1

# Chat

### Основные сущности:

* <b>UserMessage</b>

```json
{
  "chat_id": "string",
  "role": "user",
  "text": "string"
}
```

* <b>AssistantMessage</b>

```json
{
  "chat_id": "string",
  "role": "assistant",
  "text": "string"
}
```

> POST `/api/v1/chat/completion`

Метод для работы с AI агентом с сохранением контекста диалога.<br>

Request body:
```json
{
  "chat_id": "string",
  "role": "user",
  "text": "string"
}
```

Response body:
```json
{
  "chat_id": "string",
  "role": "assistant",
  "text": "string"
}
```

> GET `/api/v1/chat/messages/{chat_id}`

Метод для получения истории чата пользователя по его chat_id.<br>

Parameters:<br>

|  Name   |              Type              |  Description   |
|:-------:|:------------------------------:|:--------------:|
| chat_id |             string             | Уникальный идентификатор чата |
| is_paginated |     boolean, default false     | Использовать ли пагинацию |
| page |       integer, minimum 1       | Страница |
| limit | integer, minimum 1, default 10 | Количетсво элементов на странице |


Response body if <b>is_paginated = False</b>:
```typescript
{
  "chat_id": "string",
  "messages": [
    {
      "chat_id": "string",
      "role": "user" | "assistant",
      "text": "string"
    }
  ]
}
```

Response body if <b>is_paginated = True</b>:
```typescript
{
  "total": "integer",
  "page": "integer",
  "limit": "integer",
  "chat_id": "string",
  "messages": [
    {
      "chat_id": "string",
      "role": "user" | "assistant",
      "text": "string"
    }
  ]
}
```

## Websocket

> GET /api/v1/ws/chat/{chat_id}

Устанавливает соединение WebSocket для чата в режиме реального времени с AI агентом.

Parameters:

|  Name   |              Type              |  Description   |
|:-------:|:------------------------------:|:--------------:|
| chat_id |             string             | Уникальный идентификатор чата |

Пример сообщения:
```typescript
{
  "chat_id": "string",
  "role": "user",
  "text": "string"
}
```

Пример ответа:
```typescript
{
  "chat_id": "string",
  "role": "assistant",
  "text": "string"
}
```