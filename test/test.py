#coding:utf-8
from os.path import abspath, dirname
print dirname(abspath(__file__))

class A:
    def __init__(self, func):
        self.func = func
    def __call__(self):
        return self.func() + 20

@A
def a():
    return 10

def b():
    return 30

print(a())

c=A(a) #this means calling A(A(a)) , so 20+20+10
print c()

d=A(b) # 30+20
print d()

print(a())

if  __name__ == '__main__':
    pass