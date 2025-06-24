import sys


def generator(*args):
    user_input = args

    if user_input == ():
        print("*** No Flags Provided, Use 'python generator.py -help' for a List of All Commands ***")
        return

    print(user_input)


if __name__ == "__main__":
    generator(*sys.argv[1:])