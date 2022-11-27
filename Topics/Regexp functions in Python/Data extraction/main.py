import re

string = input()
start = '<START>'
end = '<END>'
start_end = re.split(start, string)[1].split(end)[0]
print(start_end)
