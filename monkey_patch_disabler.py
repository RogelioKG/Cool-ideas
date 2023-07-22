class MonkeyDisabler(type):
    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        return {}

    def __new__(mcs, name, bases, attrs, **kwargs):
        return super().__new__(mcs, name, bases, attrs)

    def __init__(cls, name, bases, attrs, *, disable):
        super().__init__(name, bases, attrs)
        cls.__disable = disable

    def __setattr__(cls, key, value):
        if (key == "_MonkeyDisabler__disable") or (key not in cls._MonkeyDisabler__disable):
            super().__setattr__(key, value)
        else:
            print(f"Monkey patching '{key}' is disabled.")


class Cat(metaclass=MonkeyDisabler, disable=["exclaim"]):
    def __setattr__(self, key, value):
        print(f"Attempt to set {key}")
        if key not in self.__class__._MonkeyDisabler__disable:
            super().__setattr__(key, value)
        else:
            print(f"Monkey patching '{key}' is disabled.")

    def __init__(self, name):
        self.name = name

    def exclaim(self):
        print(f"I am wawacat {self.name}!")


if __name__ == "__main__":
    cat1 = Cat("Candy")
    cat2 = Cat("Chester")

    print("-------------------------------")

    def monkey_exclaim():
        print(r"%%%%%%")

    cat1.exclaim()
    cat1.exclaim = monkey_exclaim
    cat1.exclaim()

    print("-------------------------------")

    def monkey_shouting(self):
        print(r"!!!!!!")

    cat2.exclaim()
    Cat.exclaim = monkey_shouting
    cat2.exclaim()

