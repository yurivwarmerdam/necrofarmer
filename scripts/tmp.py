asd = (1, 2, 3)

print(isinstance(asd, tuple))


class AClass:
    def __init__(self, thing):
        self.thing = thing
        pass


class BClass(AClass):
    def __init__(self, thing, thang):
        self.thang = thang
        super().__init__(thing)


a_class = AClass("asd")
b_class = BClass("asd", "def")


print(a_class.thing, b_class.thang)
