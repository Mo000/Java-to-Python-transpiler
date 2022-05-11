from timeit import default_timer as timer
class test3:

    def __init__(self):
        pass

    def main(self, args):
        self.testFunc()

    def testFunc(self):
        e = len('hello')
        i = 0
        while i < 10000:
            print(i)
            print(e)
            i = i + 1
if __name__ == '__main__':
    start = timer()
    test3().main([])
    end = timer()
    print(end-start)