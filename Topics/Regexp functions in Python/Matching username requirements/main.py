import re

username = input()
regexp = '[a-zA-Z]'

print('Thank you!' if re.match(regexp, username) else "Oops! The username has to start with a letter.")
