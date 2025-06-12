class Box:
    def __init__(self, matrix_obj, x, y):
        if (
            x < 0
            or y < 0
            or x > len(matrix_obj.matrix) - 1
            or y > len(matrix_obj.matrix) - 1
        ):
            raise IndexError("Invalid coordinates")
        self.x = x
        self.y = y
        self.matrix = matrix_obj.matrix

    def status(self):
        row = abs(self.y - len(self.matrix) + 1)
        return self.matrix[row][self.x]

    def set_status(self, status):
        row = abs(self.y - len(self.matrix) + 1)
        self.matrix[row][self.x] = status
