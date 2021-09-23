import enum


class Solver:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.points = set()
        self.lines = []
        self.collinear = {}
        self.lines_group_by_angle = []

    def solve(self):
        self.__read_points_from_file()
        self.__index_points()
        self.__sort_lines_by_ctg_and_dist()
        self.__print_answer()

    def __read_points_from_file(self):
        with open(self.input_file) as f:
            for line in f:
                point = tuple([int(x) for x in line.split()])
                self.points.add(point)  # add to set to avoid duplicate points
        self.points = tuple(self.points)  # cast to tuple to save order and consistency

    def __index_points(self):
        points_count = len(self.points)
        for i in range(points_count):
            for j in range(i + 1, points_count):
                self.lines.append((i, j))
        self.lines = tuple(self.lines)

    def __sort_lines_by_ctg_and_dist(self):
        # log_file = open('log.txt', "w")

        class inequality_types(enum.Enum):
            LESS = 1
            MORE = 2
            EQUAL = 3

        def get_vec(line):
            x, y = self.points[line[1]][0] - self.points[line[0]][0], \
                   self.points[line[1]][1] - self.points[line[0]][1]
            return x, y

        def ctg_cond(line_1, line_2):
            # let that angles from [0, 180), because 0 and 180 is the same lines
            a_x, a_y = get_vec(line_1)
            b_x, b_y = get_vec(line_2)
            if a_y == 0 and b_y == 0:
                return inequality_types.EQUAL
            elif a_y == 0:  # angle = 0
                return inequality_types.LESS
            elif b_y == 0:  # angle = 0
                return inequality_types.MORE
            else:
                if a_y < 0:
                    a_x, a_y = -a_x, -a_y
                if b_y < 0:
                    b_x, b_y = -b_x, -b_y
                cond_1 = a_x * b_y
                cond_2 = a_y * b_x
                if cond_1 > cond_2:  # ctg(line_1) > ctg(line_2) <=> angle(line_1) < angle(line_2)
                    return inequality_types.LESS
                elif cond_1 < cond_2:
                    return inequality_types.MORE
            return inequality_types.EQUAL

        def OX_intersect_cond(line_1, line_2):
            a_x, a_y = get_vec(line_1)
            b_x, b_y = get_vec(line_2)
            if a_y == 0 and b_y == 0:
                p_1_y = self.points[line_1[0]][1]
                p_2_y = self.points[line_2[0]][1]
                if p_1_y == p_2_y:
                    return inequality_types.EQUAL
                elif p_1_y < p_2_y:
                    inequality_types.LESS
                else:
                    return inequality_types.MORE
            else:
                if a_y < 0:
                    a_x, a_y = -a_x, -a_y
                if b_y < 0:
                    b_x, b_y = -b_x, -b_y
                p_1_y = self.points[line_1[1]][1]
                p_2_y = self.points[line_2[1]][1]
                p_1_x = self.points[line_1[1]][0]
                p_2_x = self.points[line_2[1]][0]
                cond_1 = p_1_x * b_y * a_y - p_1_y * b_y * a_x
                cond_2 = p_2_x * a_y * b_y - b_x * a_y * p_2_y
                if cond_1 < cond_2:
                    return inequality_types.LESS
                elif cond_1 > cond_2:
                    return inequality_types.MORE
            return inequality_types.EQUAL

        def two_params_merge_sort(A, cond_func):
            if len(A) == 1 or len(A) == 0:
                return A
            L, R = A[:len(A) // 2], A[len(A) // 2:]
            two_params_merge_sort(L, cond_func)
            two_params_merge_sort(R, cond_func)
            # log_file.write(f'L: {L}\n')
            # log_file.write(f'R: {R}\n')
            n = m = k = 0
            C = [0, 0] * (len(L) + len(R))
            while n < len(L) and m < len(R):
                ineq_type = cond_func(L[n], R[m])
                if ineq_type != inequality_types.MORE:
                    C[k] = L[n]
                    n += 1
                else:
                    C[k] = R[m]
                    m += 1
                k += 1
            while n < len(L):
                C[k] = L[n]
                n += 1
                k += 1
            while m < len(R):
                C[k] = R[m]
                m += 1
                k += 1
            for i in range(len(A)):
                A[i] = C[i]
            # log_file.write(f'A: {A}\n')
            return A

        self.lines = two_params_merge_sort(list(self.lines), cond_func=ctg_cond)  # lines with the same angles is neighboring
        current_type_line_idx = 0
        current_group = [self.lines[0]]
        for i in range(1, len(self.lines)):
            if ctg_cond(self.lines[i], self.lines[current_type_line_idx]) == inequality_types.EQUAL:
                current_group.append(self.lines[i])
            else:
                current_type_line_idx = i
                self.lines_group_by_angle.append(current_group)
                current_group = [self.lines[i]]
        for i in range(len(self.lines_group_by_angle)):
            self.lines_group_by_angle[i] = two_params_merge_sort(self.lines_group_by_angle[i],
                                                                 cond_func=OX_intersect_cond)

       #  log_file.close()

    def __print_answer(self):
        def check_det(line, point):
            x_1, y_1 = self.points[line[0]][0], self.points[line[0]][1]
            x_2, y_2 = self.points[line[1]][0], self.points[line[1]][1]
            x_3, y_3 = point[0], point[1]
            det = x_1 * (y_2 - y_3) - y_1 * (x_2 - x_3) + x_2 * y_3 - x_3 * y_2
            if det == 0:
                return True
            return False

        output_file = open(self.output_file, "w")
        output_file.write("Groups:")
        group_count = 0
        for i in range(len(self.lines_group_by_angle)):
            line_num = 0
            is_need_print_first = True
            is_used = set()
            for j in range(1, len(self.lines_group_by_angle[i])):
                if check_det(self.lines_group_by_angle[i][line_num],
                             self.points[self.lines_group_by_angle[i][j][1]]) and check_det(
                        self.lines_group_by_angle[i][line_num], self.points[self.lines_group_by_angle[i][j][0]]):
                    if is_need_print_first:
                        group_count += 1
                        output_file.write(f'\nGroup {group_count}: '
                                          f'{self.points[self.lines_group_by_angle[i][line_num][0]]} '
                                          f'{self.points[self.lines_group_by_angle[i][line_num][1]]} ')
                        is_used.add(self.points[self.lines_group_by_angle[i][line_num][0]])
                        is_used.add(self.points[self.lines_group_by_angle[i][line_num][0]])
                        is_need_print_first = False
                    if self.points[self.lines_group_by_angle[i][j][0]] not in is_used:
                        output_file.write(f'{self.points[self.lines_group_by_angle[i][j][0]]} ')
                        is_used.add(self.points[self.lines_group_by_angle[i][j][0]])
                    if self.points[self.lines_group_by_angle[i][j][1]] not in is_used:
                        output_file.write(f'{self.points[self.lines_group_by_angle[i][j][1]]} ')
                        is_used.add(self.points[self.lines_group_by_angle[i][j][1]])
                else:
                    line_num = j
                    is_need_print_first = True
                    is_used = set()

        output_file.close()
