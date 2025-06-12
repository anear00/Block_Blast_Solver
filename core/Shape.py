from .Matrix import Matrix
from .Box import Box


class Shape:
    def __init__(self, data):
        self.shape = data
  
    def get_ascii(self):
        temp_matrix = Matrix([[0] * 7 for _ in range(7)])
        self.place(temp_matrix, 2, 5)
        temp_matrix.get_ascii(2, 5)
    
    def will_fit_in(self, matrix_obj, x, y):
        for dx, dy in self.shape:
            x_pos = x + dx
            y_pos = y + dy
            try:
                box = Box(matrix_obj, x_pos, y_pos)
                if box.status() == 1:
                    return False
            except IndexError:
                return False
        return True
    
    def fit_positions(self, matrix_obj):
        positions = []
        for x in range(len(matrix_obj.matrix)):
            for y in range(len(matrix_obj.matrix)):
                if self.will_fit_in(matrix_obj, x, y):
                    positions.append((x, y))
        return positions

    def place(self, matrix_obj, x, y):
        if not self.will_fit_in(matrix_obj, x, y):
            raise ValueError("The shape cannot be placed")

        for dx, dy in self.shape:
            x_pos = x + dx
            y_pos = y + dy
            Box(matrix_obj, x_pos, y_pos).set_status(1)

        matrix_obj.simplify()