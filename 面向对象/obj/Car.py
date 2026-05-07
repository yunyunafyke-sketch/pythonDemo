#定义类
from day1.strDemo import name


class Car:
    pass

#动态为对象添加属性
c1=Car()
c1.color='red'
print(c1.__dict__)


class Car1:
    #类属性（所有实例共享）
    wheel=4
    #实例属性
    def __init__(self,c_color: str,c_name: str,c_price :int):
        self.color=c_color
        self.name=c_name
        self.price=c_price
    #实例方法
    def drive (self):
        print(self.name + ' driving')
    def wight (self,wight: int):
        print(self.name +  str(wight)+"kg")
    #魔法方法（__init__）
    def __str__(self):
        return self.name + str(self.price)
    def __eq__(self, other):
        return self.name == other.name
    def __lt__(self, other):
        return self.price < other.price




c1=Car1("red","bmw",1800000)

c2=Car1("red","bmw",1900000)

print(c1.__dict__)
c1.drive()


c1.wight(10000000)
print(c1.wheel)

print((c1 == c2))
print(c1<c2)
