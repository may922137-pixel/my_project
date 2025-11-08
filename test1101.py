class student:
    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.m = [self.age, sex]

    a = 1

    def d(self):
        print(a)


a = student(None, None, None)
b = student(1, 2, 3)
print(b.d())
