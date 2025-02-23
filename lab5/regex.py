#task1
import re

def match_string(s):
    pattern = r'^ab*$'  # 'a' followed by zero or more 'b's
    if re.fullmatch(pattern, s):
        return "Match found!"
    else:
        return "No match."

strings = ["a", "b", "ab", "dab", "ababe", "ab"]
for s in strings:
    print(f"The string '{s}' matches the pattern: {match_string(s)}")

#task2
import re

def match_string(s):
    if re.fullmatch(r'^ab{2,3}$', s):
        return "Match found!"
    else:
        return "No match."

strings = ["a", "ab", "abb", "abbc", "abbb", "abbbb", "b", "aa", "abb"]
for s in strings:
    print(f"'{s}': {match_string(s)}")

#task3
import re

def match_string(s):
    pattern = r'^[a-z]+(_[a-z]+)*$'  # последовательность строчных букв, соединенных подчеркиванием
    if re.fullmatch(pattern, s):
        return "Match found!"
    else:
        return "No match."

# Тестовые случаи
strings = ["hello_world", "test_case", "example", "wrongExample", "snake_case_test", "123_invalid"]
for s in strings:
    print(f"'{s}': {match_string(s)}")
#task4
import re

def match_string(s):
    pattern = r'[A-Z][a-z]+$'  # последовательность строчных букв, соединенных подчеркиванием
    if re.fullmatch(pattern, s):
        return "Match found!"
    else:
        return "No match."

# Тестовые случаи
strings = ["Assasa", "test_case", "example", "wrongExample", "snake_case_test", "123_invalid"]
for s in strings:
    print(f"'{s}': {match_string(s)}")

#task5
import re

def match_string(s):
    pattern = r'^a.+b$'  # последовательность строчных букв, соединенных подчеркиванием
    if re.fullmatch(pattern, s):
        return "Match found!"
    else:
        return "No match."

# Тестовые случаи
strings = ["Assasa", "test_case", "example", "wrongExample", "snake_case_test", "123_invalid"]
for s in strings:
    print(f"'{s}': {match_string(s)}")

#task6
import re

def replace_delimiters(s):
    pattern = r'[ ,.]'  # Matches space, comma, or dot
    return re.sub(pattern, ':', s)

# Test cases
test_strings = ["Hello, world. This is a test", "Python is great. Do you agree?", "Space,comma.dot"]

for string in test_strings:
    print(f"Original: '{string}'")
    print(f"Modified: '{replace_delimiters(string)}'\n")

#task7
import re

def snake_to_camel(s):
    return ''.join(word.capitalize() if i > 0 else word for i, word in enumerate(s.split('_')))

# Test cases
test_strings = ["hello_world", "convert_this_string", "snake_case_to_camel"]

for string in test_strings:
    print(f"Original: '{string}'")
    print(f"Camel Case: '{snake_to_camel(string)}'\n")

#task8
import re

def split_at_uppercase(s):
    return re.findall(r'[A-Z][a-z]*', s)

# Test cases
test_strings = ["HelloWorld", "SplitAtUpperCase", "PythonProgramming"]

for string in test_strings:
    print(f"Original: '{string}'")
    print(f"Split: {split_at_uppercase(string)}\n")

#task9
import re

def insert_spaces(s):
    return re.sub(r'(?<!^)([A-Z])', r' \1', s)

# Test cases
test_strings = ["HelloWorld", "InsertSpacesBetweenWords", "PythonProgramming"]

for string in test_strings:
    print(f"Original: '{string}'")
    print(f"With spaces: '{insert_spaces(string)}'\n")
#task10
import re

def camel_to_snake(s):
    return re.sub(r'(?<!^)([A-Z])', r'_\1', s).lower()

# Test cases
test_strings = ["HelloWorld", "ConvertCamelCase", "PythonProgramming"]

for string in test_strings:
    print(f"Original: '{string}'")
    print(f"Snake case: '{camel_to_snake(string)}'\n")
