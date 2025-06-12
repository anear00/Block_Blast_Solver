import time

import config as cfg
from core import Matrix, Shape, Detector, Solver


def main():
    while True:
        print("\n\n")
        start_time = time.time()

        detector = Detector()
        
        matrix = Matrix(detector.get_matrix())

        shape_1_order, shape_2_order, shape_3_order = detector.get_shapes()
        shape_1 = Shape(shape_1_order)
        shape_2 = Shape(shape_2_order)
        shape_3 = Shape(shape_3_order)

        solver = Solver(matrix, shape_1, shape_2, shape_3)

        fast = False
        if matrix.count_walls() <= 10:
            try:
                moves = solver.get_quick_solution()
                fast = True
            except Exception:
                moves = solver.get_solution()
        else:
            moves = solver.get_solution()

        for stage in range(3):
            solver.shapes[moves[0][stage]].get_ascii()
            solver.shapes[moves[0][stage]].place(
                matrix,
                moves[stage + 1][0],
                moves[stage + 1][1]
            )
            matrix.get_ascii(
                moves[stage + 1][0],
                moves[stage + 1][1]
            )
            print()

        end_time = time.time()
        execution_time = round(end_time - start_time, 2)

        if fast:
            print('-------------------------------- Fast solved!!!')

        print(f"Execution time: {execution_time} s")
        input('Script paused. Press Enter to continue...')


if __name__ == "__main__":
    main()
