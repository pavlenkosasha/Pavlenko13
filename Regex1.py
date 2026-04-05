import re


# def example_group_alternatives():
#     text = "gray, grey "
#     pattern = r"gr(?:a|e)y"
#     print(re.findall(pattern, text))
#     text = "03.04.2026"
#     pattern = r"(\d{2})\.(\d{2})\.(\d{4})"
#     print(re.findall(pattern, text))
#     match = re.search(pattern, text)
#     print(match.group())
# example_group_alternatives()
def example():
    text = "034764++*532++00"
    pattern = r".+"
    pattern2 = ".+?"
    print(re.findall(pattern, text))
    print(re.findall(pattern2, text))


example()


#git switch -c feature/new-page