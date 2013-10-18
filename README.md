# API Documentation

### Responses
Successful responses will always contain a data key. The value may be a
dictionary for a single object response, or a list of dictionaries for
batch object responses.

```javascript
{
    "data": ...
}
```

### Errors

Error responses will always be listed as follows:

```javascript
{
    "error" : {
        "message": "Error summary",
        "errors": [
            "Error message one.",
            "Error message two."
        ]
    }
}
```

The absense of either an error or data key is undefined.

### Endpoints

GET  /event       # Get all events.
POST /event       # Create a new event.
PUT  /event/1234  # Update an event.
GET  /event/1234/details  # Get attributes/stream output for an event.
POST /event/1234/details  # Create attributes/streams for an event.
PUT  /event/1234/details  # Update attributes/streams for an event.

