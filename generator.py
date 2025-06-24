import sys
import json
from faker import Faker

def generator(*args):
    fake = Faker()
    sample_data = []
    extracted_flags = set()

    # Default values
    min_num = 0
    max_num = 1000
    generate_count = 0
    output_to_terminal = '-ot' in args
    output_to_json = '-oj' in args
    valid_prefixes = ['-help', '-fn', '-sn', '-d', '-ip', '-r', '-tf', '-g', '-ot', '-oj']

    if not args:
        print("*** No Flags Provided, Use 'python generator.py -help' for a List of All Commands ***")
        return

    # Help option
    if '-help' in args:
        print("Flags and Their Actions:\n")
        print("-help : Show Help")
        print("-fn   : First Name")
        print("-sn   : Surname")
        print("-d    : Date")
        print("-ip   : IPv4 Address")
        print("-r    : Random Number Range (e.g. -r10-20)")
        print("-tf   : True/False")
        print("-g    : Number of Records to Generate (e.g. -g10)")
        print("-ot   : Output to Terminal")
        print("-oj   : Output to JSON File\n")
        print("Example Minimal Usage:\n  python generator.py -fn -g10 -oj")
        print("This Will Generate 10 Records with First Names and Save Them to a JSON File.")
        return


    # Parse generation count, number range and valid prefixes
    for arg in args:
        if arg.startswith('-g') and arg[2:].isdigit():
            generate_count = int(arg[2:])
        elif arg.startswith('-r'):
            try:
                min_num, max_num = map(int, arg[2:].split('-'))
            except ValueError:
                print("*** No Range for -r. Using Default 0-1000 ***")
        elif arg.startswith('-'):
            for prefix in valid_prefixes:
                if arg.startswith(prefix):
                    break
            else:
                extracted_flags.add(arg)

    if extracted_flags:
        print(f"*** Invalid Flag(s): {', '.join(extracted_flags)}  ***")
        print("*** Use the '-help' Flag for a List of Valid Flags ***")
        return

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
        
        if entry:
            sample_data.append(entry)
        else:
            print("*** Please Enter Schema Specifying Flags in Command ***")
            return


    # Output
    if output_to_terminal:
        print(json.dumps(sample_data))
    elif output_to_json:
        with open("data.json", "w") as f:
            json.dump(sample_data, f)
    else:
        print("*** Please Use the '-ot' or '-oj' Flags to Output Data ***")
        return


if __name__ == "__main__":
    generator(*sys.argv[1:])