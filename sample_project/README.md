# Sample User Service

POST /users calls `create_user()` in `users.py`.

Emails are unique. Duplicate emails should produce a controlled conflict response instead of a raw database error.
