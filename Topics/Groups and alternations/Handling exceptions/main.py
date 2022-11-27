import re


# put your regex in the variable template
template = "(Value|Name|Type)(Error)"
string = input()
# compare the string and the template
re_match = re.match(template, string)
print(re_match.group(1) if re_match else re_match)
