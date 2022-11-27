import re

password = input()

password_pattern = r'[A-z0-9]{6,15}$'
password_match = re.match(password_pattern, password)
print('Thank you!' if password_match else 'Error!')
