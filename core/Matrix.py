from .Box import Box


class Matrix:
    def __init__(self, data):
        self.matrix = data

    def get_ascii(self, m_x=0, m_y=0):
        for y in reversed(range(len(self.matrix))):
            for x in range(len(self.matrix)):
                status = Box(self, x, y).status()

                if status == 1 and (x != m_x or y != m_y):
                    print("■", end=" ")
                elif status == 1 and x == m_x and y == m_y:
                    print("X", end=" ")
                elif status == 0 and x == m_x and y == m_y:
                    print("O", end=" ")
                else:
                    print("·", end=" ")
            print()
        print("-" * (len(self.matrix) * 2))

    def empty(self):
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix)):
                Box(self, x, y).set_status(0)

    def copy(self):
        return Matrix([row[:] for row in self.matrix])

    def count_walls(self):
        count = 0
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix)):
                if Box(self, x, y).status() == 1:
                    count += 1
        return count

    def simplify(self):
        pending_boxes = []

        # Check filled columns
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix)):
                if Box(self, x, y).status() == 0:
                    break
                if y == len(self.matrix) - 1:
                    for clear_y in range(len(self.matrix)):
                        pending_boxes.append((x, clear_y))

        # Check filled rows
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix)):
                if Box(self, x, y).status() == 0:
                    break
                if x == len(self.matrix) - 1:
                    for clear_x in range(len(self.matrix)):
                        pending_boxes.append((clear_x, y))

        # Clear the boxes
        for x, y in pending_boxes:
            Box(self, x, y).set_status(0)

        return bool(pending_boxes)