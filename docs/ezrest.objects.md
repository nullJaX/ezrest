# `ezrest.objects`

The `ezrest.objects` module focuses on managing data access with an object-oriented approach, emphasizing efficient data parsing and unparsing from REST API responses. This module prioritizes data integrity and simplicity, facilitating seamless integration with diverse APIs.

## CRUD / AsyncCRUD

**Source code:** [ezrest/objects.py](https://github.com/nullJaX/ezrest/blob/master/ezrest/objects.py)

*Object-oriented data access management*

This class serves as an interface for mapping between REST API responses and a container object holding the server data state, as well as providing read and modification functions following the CRUD principle.

The actual body of CRUD methods (CREATE, READ, UPDATE, DELETE) is intentionally left unimplemented due to the varying schema and interaction requirements across specific REST APIs. All modification methods accept an instance of the resource and should return the latest server state of the resource after performing the operation (the DELETE method should still return the resource containing data before deletion).

There is also one additional method, `list()`, designed to offer iterator-like behavior for endpoints returning collections and/or handling paginated responses. The `list` method handles these responses and iteratively `yield`s resources one-by-one.

> **NOTE:** To ensure simplicity and maintainability of your code, implementations of the CRUD class should focus on defining interaction at the object level, optionally incorporating parsing and unparsing mechanisms. Network/HTTP interaction should be delegated to a separate component or layer.

### Example

**REST API documentation:** [REQRES](https://reqres.in/), [UnknownResource schema](https://reqres.in/api-docs/#/)

**CRUD and model implementations** available in [tests/real/api.py](https://github.com/nullJaX/ezrest/blob/master/tests/real/api.py):
  - Model - `UnknownResource`
  - Synchronous version - `ReqResUnknownResourceCRUD`
  - Asynchronous version - `AsyncReqResUnknownResourceCRUD`

**Usage:**

> **NOTE:** Both CRUD implementations utilize the [`ezrest.requests`](ezrest.requests.md#ezrestrequests) classes to implement the network interaction with the service.

```python
# Sync version:
crud = ReqResUnknownResourceCRUD()

created_resource = crud.create(
    UnknownResource(id=-1, name="metro black", year=2033, color="#010101", pantone_value="77-2038")
)

read_resource = crud.read(5)

updated_resource = crud.update(
    UnknownResource(id=7, name="new name", year=1970, color="#FFF101", pantone_value="03-1138")
)

deleted_resource = crud.delete(
    UnknownResource(id=9, name="new name", year=1970, color="#FFF101", pantone_value="03-1138")
)

for listed_item in crud.list():
    print(listed_item)

# Async version:
crud = AsyncReqResUnknownResourceCRUD()

created_resource = await crud.create(
    UnknownResource(id=-1, name="metro black", year=2033, color="#010101", pantone_value="77-2038")
)

read_resource = await crud.read(5)

updated_resource = await crud.update(
    UnknownResource(id=7, name="new name", year=1970, color="#FFF101", pantone_value="03-1138")
)

deleted_resource = await crud.delete(
    UnknownResource(id=9, name="new name", year=1970, color="#FFF101", pantone_value="03-1138")
)

async for listed_item in crud.list():
    print(listed_item)
```