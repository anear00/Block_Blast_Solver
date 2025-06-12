class Solver:
    def __init__(self, matrix_obj, shape_1_obj, shape_2_obj, shape_3_obj):
        self.perms = (
            (0, 1, 2), (0, 2, 1), (1, 0, 2),
            (1, 2, 0), (2, 0, 1), (2, 1, 0)
        )
        self.shapes = (shape_1_obj, shape_2_obj, shape_3_obj)
        self.matrix_obj = matrix_obj

    def get_solution(self):
        mat_first = []
        for lista_index, perm in enumerate(self.perms):
            shape_obj = self.shapes[perm[0]]
            mat_first.append([])

            for matrix_index, cords in enumerate(
                shape_obj.fit_positions(self.matrix_obj)
            ):
                mat_first[lista_index].append(self.matrix_obj.copy())
                shape_obj.place(
                    mat_first[lista_index][matrix_index],
                    cords[0], cords[1]
                )

        mat_second = []
        for lista_2_index, lista_2 in enumerate(mat_first):
            shape_obj = self.shapes[self.perms[lista_2_index][1]]
            mat_second.append([])

            for lista_index, lista in enumerate(lista_2):
                mat_second[lista_2_index].append([])

                for matrix_index, cords in enumerate(
                    shape_obj.fit_positions(lista)
                ):
                    mat_second[lista_2_index][lista_index].append(lista.copy())
                    shape_obj.place(
                        mat_second[lista_2_index][lista_index][matrix_index],
                        cords[0], cords[1]
                    )

        mat_third = []
        for lista_3_index, lista_3 in enumerate(mat_second):
            shape_obj = self.shapes[self.perms[lista_3_index][2]]
            mat_third.append([])

            for lista_2_index, lista_2 in enumerate(lista_3):
                mat_third[lista_3_index].append([])

                for lista_index, lista in enumerate(lista_2):
                    mat_third[lista_3_index][lista_2_index].append([])

                    for matrix_index, cords in enumerate(
                        shape_obj.fit_positions(lista)
                    ):
                        mat_third[lista_3_index][lista_2_index][lista_index].append(
                            lista.copy()
                        )
                        shape_obj.place(
                            mat_third[lista_3_index][lista_2_index][lista_index][matrix_index],
                            cords[0], cords[1]
                        )

        min_val = 50
        for lista_3_index, lista_3 in enumerate(mat_third):
            for lista_2_index, lista_2 in enumerate(lista_3):
                for lista_index, lista in enumerate(lista_2):
                    for matrix_index, matrix in enumerate(lista):
                        current_val = matrix.count_walls()
                        if current_val < min_val:
                            min_val = current_val
                            min_coords = (
                                lista_3_index,
                                lista_2_index,
                                lista_index,
                                matrix_index
                            )
        try:
            lista_3_index = min_coords[0]
            lista_2_index = min_coords[1]
            lista_index = min_coords[2]
            matrix_index = min_coords[3]

            return (
                self.perms[lista_3_index],
                self.shapes[self.perms[lista_3_index][0]]
                .fit_positions(self.matrix_obj)[lista_2_index],
                self.shapes[self.perms[lista_3_index][1]]
                .fit_positions(mat_first[lista_3_index][lista_2_index])[lista_index],
                self.shapes[self.perms[lista_3_index][2]]
                .fit_positions(mat_second[lista_3_index][lista_2_index][lista_index])[matrix_index]
            )

        except UnboundLocalError:
            raise Exception('\n\n----------NO MOVE POSSIBLE----------')

    def get_quick_solution(self):
        digest = [(0, 1, 2)]
        temp_matrix = self.matrix_obj.copy()
        for shape in self.shapes:
            for x in range(len(self.matrix_obj.matrix)):
                for y in range(len(self.matrix_obj.matrix)):
                    try:
                        shape.will_fit_in(temp_matrix, x, y)
                        shape.place(temp_matrix, x, y)
                        digest.append((x, y))
                        r = True
                        break
                    except:
                        r = False
                        continue
                if r:
                    break
            if not r:
                raise Exception('\n\n----------NO MOVE POSSIBLE----------')

        return digest
