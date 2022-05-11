from timeit import default_timer as timer
class test3:
    def main(self):
        self.testFunc()
    def testFunc(self):
        e = len('hello')
        for i in range(10000):
            print(i)
            print(e)
if __name__ == '__main__':
    start = timer()
    test3().main()
    end = timer()
    print(end-start)