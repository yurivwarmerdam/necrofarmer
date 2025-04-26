asd = (1, 2, 3)

print(isinstance(asd, tuple))


class AClass():
    pass

def thing():
    # return (AClass)
    return ("asd")


a, *b = thing()

print(a)

print(b)
