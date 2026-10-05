# User API

The sample service exposes `POST /users`.

A user contains id, name, and email.

The email field must be unique.

Expected behavior:
- A new email creates a user.
- An existing email should be rejected with a clear 409-style conflict response.
- Unexpected database errors should be logged and returned as a 500 response.
