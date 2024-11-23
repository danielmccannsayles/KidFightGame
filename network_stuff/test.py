pos = ("1", "test")


class Test:
    def __init__(self, pos) -> None:
        self.set_pos(pos)

    def set_pos(self, pos):
        self.x, self.y = pos


t = Test(pos)

print(t.x)
print(t.y)
