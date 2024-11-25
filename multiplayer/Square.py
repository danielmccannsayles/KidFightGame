class Square:
    def to_dict(self):
        return {"x": self.x, "y": self.y, "color": self.color}

    @classmethod
    def from_dict(cls, data):
        return cls(x=data["x"], y=data["y"], color=data["color"])
