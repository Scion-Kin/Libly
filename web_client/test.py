from flask import Flask, session
from itsdangerous import URLSafeSerializer

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

s = URLSafeSerializer(app.secret_key)

# Encrypt data
token = s.dumps({'username': 'user123'})
print(token)

# Decrypt data
data = s.loads(token)
print(data)
