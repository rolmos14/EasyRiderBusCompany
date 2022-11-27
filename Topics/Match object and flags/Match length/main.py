import re

template = r'are you ready??.?.?'
word = input()

print(len(re.match(template, word).group()) if re.match(template, word) else 0)
