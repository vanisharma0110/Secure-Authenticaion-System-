import os
import base64

secret = base64.urlsafe_b64encode(os.urandom(16)).decode()
print(secret)