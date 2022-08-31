import sys
import traceback


class GaussJorden:
    def __init__(self):
        self.a = [
            [ 5, -4,  6,  8],
            [ 7,  -6, 10,  14],
            [ 4,  9, 7,  74]
        ]
        self.n = len(self.a)

    def exec(self):
        """ Solving and display """
        try:
            self.__display_equations()
            for k in range(self.n):
                p = self.a[k][k]
                for j in range(k, self.n + 1):
                    self.a[k][j] /= p
                for i in range(self.n):
                    if i == k:
                        continue
                    d = self.a[i][k]
                    for j in range(k, self.n + 1):
                        self.a[i][j] -= d * self.a[k][j]
            self.__display_answers()
        except Exception as e:
            raise

    def __display_equations(self):
        """ Display of source equations """
        try:
            for i in range(self.n):
                for j in range(self.n):
                    print("{:+d}x{:d} ".format(self.a[i][j], j + 1), end="")
                print("= {:+d}".format(self.a[i][self.n]))
        except Exception as e:
            raise

    def __display_answers(self):
        """ Display of answer """
        try:
            for k in range(self.n):
                print("x{:d} = {:f}".format(k + 1, self.a[k][self.n]))
        except Exception as e:
            raise


if __name__ == '__main__':
    try:
        obj = GaussJorden()
        obj.exec()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)