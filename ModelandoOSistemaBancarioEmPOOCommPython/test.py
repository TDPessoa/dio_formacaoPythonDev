class Test:
    def __init__(self):
        self.test = 'test'


list_of_tests = []
test1 = Test()
test2 = Test()
test2.test = 'no test'
list_of_tests.append(test1)
list_of_tests.append(test2)
list_of_tests[0].test = 'is test'
print(test1.test)
