import sys
import json
from faker import Faker

def generator(*args):
    fake = Faker()
    sample_data = []

    # Default values
    min_num = 0
    max_num = 1000
    generate_count = 0
    output_to_terminal = '-ot' in args
    output_to_json = '-oj' in args

    if not args:
        print("*** No Flags Provided, Use 'python generator.py -help' for a List of All Commands ***")
        return

    # Help option
    if '-help' in args:
        print("Flags and their actions:")
        print({
            '-help': 'show help',
            '-fn': 'first name',
            '-sn': 'surname',
            '-d': 'date',
            '-ip': 'IPv4 address',
            '-r': 'random number range (e.g. -r10-20)',
            '-tf': 'true/false',
            '-g': 'number of records to generate (e.g. -g10)',
            '-ot': 'output to terminal',
            '-oj': 'output to JSON file'
        })
        print("Example usage: 'python generator.py -fn -sn -g10 -oj' will generate 10 records consisting of firstnames and surnames, will save to file in JSON format")
        return

    # Parse generation count and number range
    for arg in args:
        if arg.startswith('-g') and arg[2:].isdigit():
            generate_count = int(arg[2:])
        elif arg.startswith('-r'):
            try:
                min_num, max_num = map(int, arg[2:].split('-'))
            except ValueError:
                print("*** Invalid range for -r. Using default 0-1000 ***")

    if generate_count == 0:
        print("*** Use the '-g' Flag Followed by a Number to Specify How Many Records to Produce ***")
        return

    # Generate the records
    for i in range(generate_count):
        entry = {}
        if '-fn' in args:
            entry["first_name"] = fake.first_name()
        if '-sn' in args:
            entry["surname"] = fake.last_name()
        if '-d' in args:
            entry["date"] = fake.date()
        if any(arg.startswith('-r') for arg in args):
            entry["number"] = fake.random_int(min=min_num, max=max_num)
        if '-tf' in args:
            entry["true_false"] = fake.boolean()
        if '-ip' in args:
            entry["ipv4_address"] = fake.ipv4_private()
        sample_data.append(entry)

    # Output
    if output_to_terminal:
        print(json.dumps(sample_data))
    if output_to_json:
        with open("data.json", "w") as f:
            json.dump(sample_data, f)
    else:
        print("*** Please Use the '-ot' or '-oj' Flags to Output Data ***")


if __name__ == "__main__":
    generator(*sys.argv[1:])