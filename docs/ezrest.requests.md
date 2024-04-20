# `ezrest.requests`

The `ezrest.requests` module provides a comprehensive toolkit for facilitating communication with REST APIs at a request-response level. It empowers developers to seamlessly interact with remote services, abstracting away complexities and providing intuitive interfaces.

## Connector / AsyncConnector

**Source code:** [ezrest/requests.py](https://github.com/nullJaX/ezrest/blob/master/ezrest/requests.py)

*Unified HTTP interaction with specific REST API*

This 'interface' class contains all HTTP methods that are commonly used in REST APIs. The methods themselves (POST, GET, PUT, PATCH, DELETE) are not implemented so that developers can pick HTTP library of choice. Each method accepts URL as a first argument, the rest of the arguments (such as URL headers or parameters) are up to developer's discretion.

There is also one additional method, `list()`, its purpose is to provide iterator-like behavior for the endpoints returning collections and/or to handle paginated responses. The `list` method should handle these responses and always `yield` items/resources one-by-one.

> **NOTE:** To keep your code simple and maintainable, the implementations of this class should not define how the resources are converted from and into objects/dataclasses. The intended scope of a connector is to provide unified interface between client and a server on a request-response level, possibly with authentication scheme and error handling.

### Example

**REST API documentation:** [REQRES](https://reqres.in/)

**Connector implementations** available in [tests/real/api.py](https://github.com/nullJaX/ezrest/blob/master/tests/real/api.py):
  - Synchronous version - `ReqResConnector`
  - Asynchronous version - `AsyncReqResConnector`

**Usage:**
```python
URL = "https://reqres.in/api/users"
USER_URL = f"{URL}/2"

# Sync version:
connector = ReqResConnector()
user_with_id_2 = connector.get(USER_URL)
for user in connector.list(URL):
    print(user)

# Async version:
connector = AsyncReqResConnector()
user_with_id_2 = await connector.get(USER_URL)
async for user in connector.list(URL):
    print(user)
```

## Endpoint / AsyncEndpoint / BaseEndpoint

**Source code:** [ezrest/requests.py](https://github.com/nullJaX/ezrest/blob/master/ezrest/requests.py)

*Dynamic URL generation*

These classes allow for generating endpoint URLs dynamically without hardcoding endpoint suffixes and use [`Connector`/`AsyncConnector`](#connector-asyncconnector) instance to perform requests.

There is no significant difference between synchronous and asynchronous versions of these classes other than the naming. Each example below will generate a copy of the original endpoint instance with modified URL, but the connector instance will remain shared between the original and copied instances. On each endpoint instance one can call methods implemented in the connector. **Note, however, that these methods don't accept URL as the first argument, it is automatically injected.** The rest of the arguments are passed through without any modifications.

### Example

```python
BASE_URL = "http://x.com/"
connector = Connector[Dict[str, Any]]()
api_root = Endpoint[Dict[str, Any]](BASE_URL, connector)

api_root                # URL: http://x.com/
api_root.posts          # URL: http://x.com/posts
api_root.comments[3]    # URL: http://x.com/comments/3
api_root["comments"][3] # URL: http://x.com/comments/3
api_root.comments.3     # Not allowed, 3 is not a string type

# Sending requests:
for user_3_comment in api_root.comments.list(params={"userId": 3}):
    print(user_3_comment)

post_with_id_49 = api_root.posts[49].get()

created_post = api_root.posts.post(data={"text": "Text for a new post"})
```