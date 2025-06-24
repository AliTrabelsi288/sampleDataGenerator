import sys
from faker import Faker

def generator(*args):
    fake = Faker()

    sample_data = {}

    if not args:
        print("*** No Flags Provided, Use 'python generator.py -help' for a List of All Commands ***")
        return


    flags = {'-help' : 'help',
             '-fn' : 'firstname',
              '-sn' : 'surname',
               '-d' : 'date',
               '-ip' : 'ip',
               '-r' : 'numbers',
               '-tf' : 'true/false',
               '-g' : 'generate',
               '-ot' : 'terminal',
               '-oj' : 'json'}
    

def first_name_generator(fake):
    return fake.first_name()

def surname_generator(fake):
    return fake.last_name()

def date_generator(fake):
    return fake.date()

def random_number_generator(min, max, fake):
    return fake.random_int(min=min, max=max)

def true_false_generator(fake):
    return fake.boolean()


if __name__ == "__main__":
    generator(*sys.argv[1:])