from copy import deepcopy
import numpy as np
import traceback


class Simplex():
    def __init__(self, A, b, c):
        self.A = A
        self.b = b
        self.c = c
        self.m, self.n = A.shape  # m: 方程式の数, n: 変数の次元

        # 辞書の定義
        self.dic = np.zeros((self.m + 1, self.n + 1), dtype='float64')
        for i in range(self.m):
            for j in range(self.n):
                self.dic[i + 1, j + 1] += A[i, j]
        for j in range(self.n):
            self.dic[0, j + 1] += c[j]
        for i in range(self.m):
            self.dic[i + 1, 0] += -b[i]
        self.x_n = np.zeros(self.n, dtype='float64')  # 非基底変数
        self.x_m = np.zeros(self.m, dtype='float64')  # 基底変数
        self.x_n_index = np.arange(0, self.n, dtype='int64')
        self.x_m_index = np.arange(self.n, self.m + self.n, dtype='int64')

    def run(self):
        # 原点が許容解であるか確認
        for j in range(self.n):
            self.x_n[j] = 0.0
        self.x_m = self.update_basis()  # 非基底変数が原点のときの基底変数を代入
        is_feasible = True
        for x in self.x_m:
            is_feasible = is_feasible and (x >= 0.0)
        if not is_feasible:
            try:  # 原点が非許容である場合エラー出力
                raise Exception('The origin is not feasible.')
            except BaseException:
                print(traceback.format_exc())

        z_sol = self.loop()

        x_sol = [0 for _ in range(self.n)]
        x_concat = np.concatenate([self.x_n, self.x_m])
        index_concat = np.concatenate([self.x_n_index, self.x_m_index])
        for j, x in zip(index_concat, x_concat):
            if j < self.n:
                x_sol[j] = x

        return z_sol, np.array(x_sol)

    def loop(self):
        while True:
            self.show_dic()
            # 非基底変数の選択
            j_pivot = -1
            for j, a in enumerate(self.dic[0, 1:]):
                if a < 0:
                    j_pivot = j + 1
                    break
            if j_pivot == -1:  # 負である係数が存在しない場合終了
                return self.get_cost()

            # 基底変数の選択
            base_candidate = {}
            for i in range(1, self.m + 1):
                if self.dic[i, j_pivot] < 0:
                    base_candidate[i] = self.dic[i, 0] \
                        / abs(self.dic[i, j_pivot])
            if len(base_candidate) == 0:
                # 基底の候補がない場合はこの線形計画問題は非有界
                raise Exception('This problem is unbounded.')
            d_min = min(base_candidate.values())
            i_min_list = [kv[0] for kv in base_candidate.items()
                          if kv[1] == d_min]
            # 基底の候補から添え字の最小となる基底を選択
            i_pivot = self.m + self.n
            index_pivot = self.m + self.n
            for i_min in i_min_list:
                if index_pivot >= self.x_m_index[i_min - 1]:
                    i_pivot = i_min
                    index_pivot = self.x_m_index[i_min - 1]

            # 選択された非基底変数を許容性を保存しつつ最大限まで増加させる
            self.x_n[j_pivot - 1] = d_min
            self.x_m[i_pivot - 1] = 0.0

            # ピボット演算でdic, x_m, x_n, x_m_index, x_n_indexを更新
            self.pivot(i_pivot, j_pivot)

    def pivot(self, i_pivot, j_pivot):
        self.x_m[i_pivot - 1], self.x_n[j_pivot - 1] = \
            self.x_n[j_pivot - 1], self.x_m[i_pivot - 1]
        self.x_m_index[i_pivot - 1], self.x_n_index[j_pivot - 1] = \
            self.x_n_index[j_pivot - 1], self.x_m_index[i_pivot - 1]

        dic_prev = deepcopy(self.dic)
        for i in range(self.m + 1):
            if i == i_pivot:
                c = -1.0 / dic_prev[i_pivot, j_pivot]
                self.dic[i, :] = dic_prev[i, :] * c
                self.dic[i_pivot, j_pivot] = -c
            else:
                c = dic_prev[i, j_pivot] / dic_prev[i_pivot, j_pivot]
                self.dic[i, :] = dic_prev[i, :] - dic_prev[i_pivot, :] * c
                self.dic[i, j_pivot] = c

    def update_basis(self):
        return np.dot(self.dic[1:, 1:], self.x_n) + self.dic[1:, 0]

    def get_cost(self):
        return np.dot(self.dic[0, 1:], self.x_n) + self.dic[0, 0]

    def show_dic(self):
        print('    |          |', end='')
        for x in self.x_n_index:
            print('%10.2f ' % (x), end='')
        print('')
        print('-' * (4 + 11 + 11 * self.n))

        print('cost|%10.2f|' % (self.dic[0, 0]), end='')
        for d in self.dic[0, 1:]:
            print('%10.2f ' % (d), end='')
        print('')

        for i in range(1, self.m + 1):
            print('%4d|%10.2f|' % (self.x_m_index[i - 1], self.dic[i, 0]), end='')
            for d in self.dic[i, 1:]:
                print('%10.2f ' % (d), end='')
            print('')
        print('')


# 実際に実行してみる
if __name__ == "__main__":
    A = np.array([[1, 0, 0, 1, 0], [1, 1, 0, 0, 0],
                  [0, 1, 1, 0, 0], [0, 0, 1, 0, 1]], dtype='float64')
    b = np.array([3, 6, 5, 2], dtype='float64')
    c = np.array([-17, -16, -18, -8, -9], dtype='float64')
    print(Simplex(A, b, c).run())
