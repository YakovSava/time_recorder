import re

strings = ["[E] Error message", "[W] Warning message", "[I] Information message"]
pattern = re.compile(r"\[\w\] ")

new_strings = [pattern.sub("<14>", string) for string in strings]
print(new_strings)
