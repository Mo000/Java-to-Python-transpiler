class testfile:
    def main():
        threeDimensional = [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]], [[13, 14, 15], [16, 17, 18]], [[19, 20, 21], [22, 23, 24]]]
        print(threeDimensional[0][1][2])
        for twoDimensional in threeDimensional:
            print(twoDimensional)
            for oneDimensional in twoDimensional:
                print(oneDimensional)
        x = 0
        y = (x + 2) * 2
        if x == 0:
            print('0')
            if y == 4:
                print('4')
            else:
                pass
            pass
        elif x == 1:
            print('1')
            pass
        elif x == 2:
            print('2')
            pass
        elif x == 3:
            print('3')
            pass
        elif x == 4:
            print('4')
            pass
        else:
            pass
if __name__ == '__main__':
    testfile.main()