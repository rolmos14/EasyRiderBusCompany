import re


words = input()
print(re.findall(r'\w+', words, flags=re.ASCII))
