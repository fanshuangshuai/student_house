# coding=utf-8

class A(object):
    arr1 = 2
    def foo(self, x):
        print("executing foo( %s,%s )" % (self, x))
        print('self:', self)
        print(self.arr1)     # 对象A的实例可调用类属性
    @classmethod
    def class_foo(cls, x):
        print("executing class_foo(%s,%s)" % (cls, x))
        print('cls:', cls)
        print(cls.arr1)     # 对象A可调用类属性
    @staticmethod
    def static_foo(x):
        print("executing static_foo(%s)" % x)
        print(A.arr1)       # 类可以调用类属性

a = A()
"""
foo绑定对象A的实例，class_foo绑定对象A，static_foo没有参数绑定。
"""
a.foo(10)
a.class_foo(10)
a.static_foo(10)