import sys
from faker import Faker

def generator(*args):
    fake = Faker()

    sample_data = []

    min_num = 0
    max_num = 1000
    generate_count = 0

    if not args:
        print("*** No Flags Provided, Use 'python generator.py -help' for a List of All Commands ***")
        return

    flags = {'-help' : 'help',
             '-fn' : 'firstname',
              '-sn' : 'surname',
               '-d' : 'date',
               '-ip' : 'ip',
               '-r' : 'numbers (eg. -r10-20)',
               '-tf' : 'true/false',
               '-g' : 'generate (eg. -g10)',
               '-ot' : 'terminal',
               '-oj' : 'json'}
    
    if '-help' in args:
            print(flags)
            print("Example use: 'python generator.py -fn -g10 -ot'")
            return
    

    for arg in args:
        if arg.startswith('-g') and arg[2:].isdigit():
            generate_count = int(arg[2:])

        if arg.startswith('-r'):
            range_str = arg[2:]
            if '-' in range_str:
                try:
                    min_num, max_num = map(int, range_str.split('-'))       # map to split min/max values, convert to int and store in respected variables
                except ValueError:
                    print("*** Invalid range format for -r flag. Using default 0-1000 ***")

    
    if generate_count == 0:
        print("*** Use the '-g' Flag Followed by a Number to Specify How Many Records to Produce ***")
        return
    

    for i in range(generate_count):
        entry = {}

        if '-fn' in args:
            entry["first_name"] = first_name_generator(fake)
        if '-sn' in args:
            entry["surname"] = surname_generator(fake)
        if '-d' in args:
            entry["date"] = date_generator(fake)
        if any(arg.startswith('-r') for arg in args):
            entry["number"] = random_number_generator(min_num, max_num, fake)
        if 'tf' in args:
            entry['true_false'] = true_false_generator(fake)
        if '-ip' in args:
            entry['ipv4_address'] = ip_generator(fake)

        sample_data.append(entry)

    print(sample_data)
    

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

def ip_generator(fake):
    return fake.ipv4_private()


if __name__ == "__main__":
    generator(*sys.argv[1:])