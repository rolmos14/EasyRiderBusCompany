import re

string = input()

date_format = r'((0[1-9])|([1-2][0-9])|(3[0-1]))/((0[1-9])|(1[0-2]))/\d{4}'
print('True' if re.match(date_format, string) else 'False')
