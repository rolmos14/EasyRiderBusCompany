import re

template = r'... Jude'
re_match = re.match(template, input())
print(re_match.group() if re_match else 'None')
