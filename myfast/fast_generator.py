def doh():
    return ["Homer: D'oh!", "Marge: A deer!", "Lisa: A demale deer!"]

for line in doh():
    print(line)


def doh2():
    yield "Homer: D'oh!"
    yield "Marge: A deer!"
    yield "Lisa: A demale deer!"

for line in doh2():
    print(line)