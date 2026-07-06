from app.core.security import create_access_token, verify_access_token

token = create_access_token(
    {
        "sub": "admin@gmail.com",
        "role": "admin",
    }
)

print(token)
print(verify_access_token(token))