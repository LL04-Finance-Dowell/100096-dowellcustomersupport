# 100096-dowellcustomersupport

## Base Url https://100096.pythonanywhere.com/

### Entry Page

_GET_ to `https://100096.pythonanywhere.com/customer-support/`

- Response 201

```json
{
  "message": "show the admin_support_page_view page"
}
```

- Response 400

```json
{
  "message": "Error"
}
```

_GET_ to `https://100096.pythonanywhere.com/living-lab-support/`

- Response 201

```json
{
  "message": "show the living_lab_support_view page"
}
```

- Response 400

```json
{
  "message": "Error"
}
```

_GET_ to `https://100096.pythonanywhere.com/send/<int:pk>/`

- Response 201

```json
{
  "portfolio": "",
  "messages": [
    {
      "id": "id",
      "timestamp": "2023-03-18T00:59+00:00",
      "room_id": "room_id",
      "read": "true/fasle",
      "message": "message",
      "side": "true/fasle",
      "author": {
        "id": "id",
        "session_id": "Session_id"
      }
    }
  ]
}
```

- Response 400

```json
{
  "message": "Error"
}
```

_post_ to `https://100096.pythonanywhere.com/send/<int:pk>/`

- Request Body

```json
{
  "message": "<message>",
  "session_id": "<session_id>"
}
```

- Response 201

```json
{
  "portfolio": "",
  "messages": [
    {
      "id": "id",
      "timestamp": "2023-03-18T00:59+00:00",
      "room_id": "room_id",
      "read": "true/fasle",
      "message": "message",
      "side": "true/fasle",
      "author": {
        "id": "id",
        "session_id": "Session_id"
      }
    }
  ]
}
```

- Response 400

```json
{
  "message": "Error"
}
```

_GET_ to `https://100096.pythonanywhere.com/room_list/(?P<product>[0-9\w-]+)`

- Response 201

```json
{
  "rooms": [],
  "firstroom": null,
  "messages": []
}
```

- Response 400

```json
{
  "message": "Error"
}
```
