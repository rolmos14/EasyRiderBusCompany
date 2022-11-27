import re

string = input()

regexp = "Good (morning|afternoon|evening)"
re_match = re.match(regexp, string)

print(re_match.group() if re_match else "No greeting!")
