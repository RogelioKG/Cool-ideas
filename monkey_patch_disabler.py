#!/usr/bin/env python
"""抓猴神器：防止猴子補丁的最佳夥伴"""
# implemented by metaclass
# My POV:
# 純粹是想練習 metaclass，
# 否則這樣的設計其實並沒有太多意義
# 對 Python 而言，開放比起封閉而言還要好。
# (當然，這並不意味著 Python 不安全。成員的易存取性是在幫助 programmer，和安全問題是兩碼子事)
# 且 Python 一直都有著 "We are all consenting adults here" 的立場。
# 我們應該對自己的行為負責，而不是從語言層面去限制對成員或方法的存取。

class MonkeyDisabler(type):
    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        return {}

    def __new__(mcs, name, bases, attrs, **kwargs):
        return super().__new__(mcs, name, bases, attrs)

    def __init__(cls, name, bases, attrs, *, disable=None):
        super().__init__(name, bases, attrs)
        if disable is None:
            cls.__disable = set(attrs.keys())
        else:
            cls.__disable = set(disable)

    def __setattr__(cls, key, value):
        if (key == "_MonkeyDisabler__disable") or (key not in cls._MonkeyDisabler__disable):
            super().__setattr__(key, value)
        else:
            print(f"Monkey patching '{key}' is disabled.")
            
# 所有在類別 __dict__ 底下的方法與屬性皆無法進行猴子補丁
# class Cat(metaclass=MonkeyDisabler):
# 指名在類別 __dict__ 底下的某些方法與屬性不可進行猴子補丁
# class Cat(metaclass=MonkeyDisabler, disable: Sequence[str]):
class Cat(metaclass=MonkeyDisabler, disable=["exclaim"]):
    def __init__(self, name):
        self.name = name
        
    # 若沒有這個 __setattr__，你仍能對個別實例進行猴子補丁
    def __setattr__(self, key, value):
        if key not in self.__class__._MonkeyDisabler__disable:
            super().__setattr__(key, value)
        else:
            print(f"Monkey patching '{key}' is disabled.")

    def exclaim(self):
        print(f"{self.name} meow")


if __name__ == "__main__":
    cat1 = Cat("Candy")
    cat2 = Cat("Chester")

    def monkey_exclaim():
        print(r"%%%%%%")

    cat1.exclaim()
    # Candy meow
    cat1.exclaim = monkey_exclaim
    # Monkey patching 'exclaim' is disabled.
    cat1.exclaim()
    # Candy meow

    def monkey_shouting(self):
        print(r"!!!!!!")

    cat2.exclaim()
    # Chester meow
    Cat.exclaim = monkey_shouting
    # Monkey patching 'exclaim' is disabled.
    cat2.exclaim()
    # Chester meow
    
