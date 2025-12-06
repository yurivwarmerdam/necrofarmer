from blinker import signal


class SomeObj:
    def __init__(self) -> None:
        self.ngu = signal("number go up")

    def send(self):
        self.ngu.send(self)


def some_func(sender):
    print(f"gettign stuff: {sender}")
def second_func(sender):
    print(f"gettign more stuff: {sender}")

some_obj = SomeObj()
another_obj =SomeObj()

# these two are the same object.
ngu = signal("number go up")
observer2=signal("number go up")

# connecting twice, under different name does nothing the second time around.
ngu.connect(some_func)
# observer2.connect(some_func)
ngu.connect(lambda sender: print(sender),weak=False)

some_obj.send()
# another_obj.send()

# in it's simplest form, you name a signal, and either conncet, or send through it.
# all signals wiht same name will link up.
# It kiiinda look like multiple connects to the same func (instance?) will only fire once.
# (think set in the observer list)