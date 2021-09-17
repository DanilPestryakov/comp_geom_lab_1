class Solver:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.points = []
        self.lines = []
        self.collinear = {}

    def solve(self):
        self.__read_points_from_file()
        self.__index_points()

        return None

    def __read_points_from_file(self):
        with open(self.input_file) as f:
            for line in f:
                point = tuple([int(x) for x in line.split()])
                self.points.append(point)
        self.points = tuple(self.points)

    def __index_points(self):
        points_count = len(self.points)
        for i in range(points_count):
            for j in range(i + 1, points_count):
                self.lines.append((i, j))
        self.lines = tuple(self.lines)

    def __get_collinear(self):
        lines_count = len(self.lines)
        type_number = 0
        use_index = [False for i in range(lines_count)]
        for i in range(lines_count):
            if use_index[i]:
                continue
            collinear = [].append(i)
            use_index[i] = True
            for j in range(i + 1, lines_count):
                if self.lines[i][0][0] * self.lines[j][1][1] == self.lines[i][0][1] * self.lines[j][1][0]:
                    collinear.append(j)
                    use_index[j] = True
            self.collinear[type_number] = collinear
            type_number += 1

    def __sort_collinear(self):
        return None

    def __print_answer(self):
        return None