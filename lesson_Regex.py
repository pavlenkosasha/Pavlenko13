import re
def example_dot():
    text = "abcdaef"
    pattern = r"a.."
    print(re.findall(pattern, text))
example_dot()

def example_quantifiers():
   text = "ab, a, abbcb"
   pattern = r"ab*"
   print(re.findall(pattern, text))
   pattern = r"ab+"
   print(re.findall(pattern, text))

   text = "colouor color"
   pattern = r"colou?r"
   print(re.findall(pattern, text))
   pattern = r"colou?r"
   print(re.findall(pattern, text))
   text = "123 45 6789"
   pattern = r"d{3}"
   print(re.findall(pattern, text))
   text = "abc 123 _-!"

   print(re.findall(r"\d", text))
   print(re.findall(r"\D", text))
   print(re.findall(r"\w", text))
   print(re.findall(r"\W", text))
   print(re.findall(r"\s", text))
   print(re.findall(r"\S", text))


#example_quantifiers()
def example_group_alternatives():
    text = "gray, grey "
    pattern = r"gr(?:a|e)y"
    print(re.findall(pattern, text))
    text = "03.04.2026"
    pattern = r"(\d{2})\.(\d{2})\.(\d{4})"
    print(re.findall(pattern, text))
    match = re.search(pattern, text)
    print(match.group())
example_group_alternatives()

def example_re_sub():
    text ="This is text   with space Hello World !"
    pattern = r"\s+"
    print(re.sub(pattern, " ", text))
#example_re_sub()
def example_re_split():
    text ="apple,  banana; orange.   Pear"
    pattern = r"[,;\.]\s*"
    print(re.split(pattern, text))
#example_re_split()
def example_flags():
    text = "Hello hello HELLO"
    pattern = "hello"
    print(re.findall(pattern, text, flags=re.I))
    text = "First text\nSecond text"
    pattern = r"^\w+"
    matches = re.findall(pattern, text, flags=re.M)
    print(matches)
example_flags()
# будет урок на github
https://github.com/yeliseevalex/python13