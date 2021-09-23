import argparse

from Solver import Solver


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Find lines with more then three points")
    parser.add_argument('-i', '--input', help='File with input points')
    parser.add_argument('-o', '--output', help='File with output lines')

    args = parser.parse_args()

    solver = Solver(args.input, args.output)
    solver.solve()

