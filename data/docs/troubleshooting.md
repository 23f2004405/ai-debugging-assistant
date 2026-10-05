# Troubleshooting

## Duplicate email errors

If creating a user with an existing email produces a raw database exception, check whether the application handles the uniqueness constraint before returning the response.

The service should translate a duplicate-email database error into a client-friendly conflict response.

## 500 errors

A 500 means the server encountered an unexpected error. Check the application logs and the failing database operation.

Do not expose raw database exception messages to API clients.
