# Modules

`ezrest` is designed with modularity in mind, offering developers a flexible solution for implementing REST API clients. Each module within the library focuses on a specific functionality, allowing developers to integrate only the components they need, promoting clear logic separation, ease of maintenance, and simplified integration. For detailed information on each module, please refer to the corresponding documentation page.

| Module | Class | Function |
| --- | --- | --- |
| [`ezrest.requests`](ezrest.requests.md) | [`Connector`/`AsyncConnector`](ezrest.requests.md#connector-asyncconnector) | Unified HTTP interaction with specific REST API |
| [`ezrest.requests`](ezrest.requests.md) | [`Endpoint`/`AsyncEndpoint`/`BaseEndpoint`](ezrest.requests.md#endpoint-asyncendpoint-baseendpoint) | Dynamic URL generation |
| [`ezrest.objects`](ezrest.objects.md) | [`CRUD`/`AsyncCRUD`](ezrest.objects.md#crud-asynccrud) | Object-oriented data access management |