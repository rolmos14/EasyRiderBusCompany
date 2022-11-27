import re

string = input()
regexp = 'b.{0,}l$'
re_match = re.match(regexp, string, flags=re.DOTALL + re.IGNORECASE)
print(re_match.group() if re_match else 'No match')
