import sys


def generator(*args):
    user_input = args

    if user_input == ():
        print("*** No Flags Provided, Use 'python generator.py -help' for a List of All Commands ***")
        return

    flags = {'-help' : 'help',
             '-fn' : 'firstname',
              '-sn' : 'surname',
               '-d' : 'date',
               '-ip' : 'ip',
               '-r' : 'numbers',
               '-tf' : 'true or false value',
               '-g' : 'generate',
               '-ot' : 'terminal',
               '-oj' : 'json'}


if __name__ == "__main__":
    generator(*sys.argv[1:])