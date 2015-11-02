'''
Created on Oct 6, 2015
@program A program to see if all subdivisions of K_2_3 have a even cycle
@author: Dallas Fraser
'''

print("Hey")


def go():
    n = 6
    for solution in ['{:0{}b}'.format(i, n) for i in range(1 << n)]:
        x, y, z = get_variables(solution)
        print("Checking Solution %s" % solution, end="")
        if check_solutions(x, y, z):
            print("Found a valid", solution)
        print()

def get_variables(solution):
    x = [int(solution[0]), int(solution[1])]
    y = [int(solution[2]), int(solution[3])]
    z = [int(solution[4]), int(solution[5])]
    return x, y, z

def check_solutions(x, y, z):
    first_cycle = x[0] + x[1] + y[0] + y[1]
    second_cycle = y[0] + y[1] + z[0] + z[1]
    third_cycle = x[0] + x[1] + z[0] + z[1]
    return all_odd(first_cycle, second_cycle, third_cycle)

def all_odd(c, c2, c3):
    x1 = c % 2 == 1
    x2 = c2 % 2 == 1
    x3 = c3 % 2 == 1
    t = x1 and x2 and x3
    print("({},{},{}) - {}".format(x1, x2, x3, t))
    return t


if __name__ == "__main__":
    go()