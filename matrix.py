"""
The Matrix class
__matmul__: Matrix multiplcation
__add_    : Matrix addition
"""



def dotp(v1, v2):
    """
    Computes the dot product of two vectors, v1 and v2.
    dim v1 = dim v2
    """

    s = 0                       # O(1)
    for i, x in enumerate(v1):  # O(dim v)
        s += x * v2[i]          # O(1) + O(1)
    return s                    # O(1)
                                # Total: O(dim v)

class Matrix:
    def __init__(self, *args):
        self.zero_cell_placeholder: str = "0"

        if len(args) == 2:                  # Requires args = (m, n)
            self.arr: list[list] = []

            for y in range(args[0]):        # O(n)
                self.arr.append([])         # O(1)
                for x in range(args[1]):    # O(m)
                    self.arr[y].append(0)   # O(1)
                                            # Total: O(mn)

        if len(args) == 1:                  # Requires args = M (the matrix as a list of lists)
            self.arr: list[list] = args[0]

        if type(self.arr[0]) != list:       # The case of which the input is only a list. We must nest it.
            self.arr = [self.arr]
    def __getitem__(self, *pair: tuple) -> float:
        if len(pair) == 2:
            i, j = pair
            return self.arr[i][j]
        elif len(pair) == 1:
            if type(pair[0]) == tuple:
                i, j = pair[0]
                return self.arr[i][j]
        return self.arr[pair[0]]
    def __setitem__(self, pair: tuple, value: float):
        i, j = pair
        self.arr[i][j] = value
    def width(self) -> int:
        return len(self.arr[0])
    def height(self) -> int:
        return len(self.arr)
    def __str__(self) -> str:
        s = "\n"
        m, n = self.width(), self.height()
        max_digit_count = [1] * m
        contains_negative = [False] * m
        
        # Calculate maximum length of numbers in each column.
        for y in range(n):
            for x in range(m):
                e = self[y, x]
                if e == 0: e = self.zero_cell_placeholder
                if type(e) == str:
                    max_digit_count[x] = max(len(e), max_digit_count[x])
                    continue
                if e < 0:
                    contains_negative[x] = True
                c = len(str(abs(e)))
                if c <= max_digit_count[x]: continue
                max_digit_count[x] = c

        # String concatenation factoring in the length of each matrix entry.
        for y, row in enumerate(self.arr):
            if   y == 0:     s += "⎡"
            elif y == n - 1: s += "⎣"
            else:            s += "⎢"

            for x, e in enumerate(row):
                if e == 0: e = self.zero_cell_placeholder
                if type(e) == str:
                    if contains_negative[x]: s += " "
                    v = (max_digit_count[x] - len(e) + 1)
                    k = v // 2
                    s += " "*k + e + " "*(v-k)
                    continue
                if contains_negative[x] and e >= 0: s += " "
                es = str(e)
                v = (max_digit_count[x] - len(es) + int(e < 0))
                k = v // 2
                s += " "*k + es + " " * (v - k)
                if x < m - 1: s += " "
        
            if   y == 0:     s += "⎤"
            elif y == n - 1: s += "⎦"
            else:            s += "⎥"
            s += "\n"

        return s
    def __repr__(self) -> str:
        return str(self)

    def transpose(self) -> "Matrix":
        """
        Compute the transpose of the matrix.
        self: Matrix[n * m]
        Returns: Matrix[m * n]
        """

        m = []                             # O(1)
        for _ in range(len(self.arr[0])):  # O(m)
            m.append([])                   # O(1)

        for i in range(len(self.arr[0])):  # O(m)
            for row in self.arr:           # O(n)
                m[i].append(row[i])        # O(1)

        return Matrix(m)                   # O(1)
    
                                           # Total: O(m) + O(mn) ∈ O(mn)

    def __add__(self, other: "Matrix") -> "Matrix":
        """
        Sum with another matrix.
        self:       Matrix[n * m]
        other:      Matrix[n * m]
        Returns     Matrix[n * m]

        (Note this is not only generalised to square matrices.)
        """

        M_sum = Matrix(self.height(), self.width())     # O(mn) 
        for y in range(self.height()):                  # O(n)
            for x in range(self.width()):               # O(m)
                M_sum[y, x] = self[y, x] + other[y, x]  # O(1) + O(1)

        return M_sum                                    # O(1)
    
        # Total: T(n) = O(mn) + O(nm) + O(1) ∈ O(mn)
        # For square matrices, m = n:
        # Which means the time complexity of addition of square matrices is T(n) ∈ O(n^2).

    def __matmul__(self, other: "Matrix") -> "Matrix":
        """
        Multiply with another matrix.
        self:       Matrix[n * k]
        other:      Matrix[k * m]
        Returns     Matrix[n * m]

        (Note this is not only generalised to square matrices.)
        """

        m = Matrix(self.height(), other.width())    # O(mn)
        other_T = other.transpose()                 # O(mn)

        for y in range(self.height()):              # O(n)
            for x in range(other.width()):          # O(m)
                m[y, x] = dotp(self[y], other_T[x]) # O(dim v) ∈ O(m)

        return m                                    # O(1)
    
        # Total: 2*O(mn) + O(nm^2) + O(1) ∈ O(nm^2)
        
        # For square matrices, n = m:
        # Therefore, the time complexity of multiplication of square matrices is T(n) ∈ O(n^3)

        # This is the naive approach, by manually computing all of the dot-products of corresponding row vectors of A and column vectors of B.
        # The standard approach uses Straussen's algorithm, which has an asymptotic time complexity of O(n^2.81).
