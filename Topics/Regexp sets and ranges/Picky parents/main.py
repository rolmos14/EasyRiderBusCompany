import re

regexp = '[B-N][aeiou]'

puppy_name = input()

if re.match(regexp, puppy_name):
    print('Suitable!')
