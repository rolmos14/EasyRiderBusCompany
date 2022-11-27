import re


# put your regex in the variable template
template = r"((\d{1,2}[/\.]){2})(\d{4})"
string = input()
re_match = re.match(template, string)
print(re_match.group(3) if re_match else re_match)
