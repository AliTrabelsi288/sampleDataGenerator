import sys
import json
from faker import Faker

import xml.etree.ElementTree as ET
import csv

def generator(*args):
    fake = Faker()
    sample_data = []
    extracted_flags = set()
    valid_prefixes = ['-help', '-fn', '-sn', '-d', '-ip', '-r', '-tf', '-g', '-ot', '-oj', '-oxml', '-ocsv', '-okv', '-otxt']

    # Default values
    min_num = 0
    max_num = 1000
    generate_count = 0

    #Output type
    output_to_terminal = '-ot' in args
    output_to_json = '-oj' in args
    output_to_xml = '-oxml' in args
    output_to_csv = '-ocsv' in args
    output_to_kvp = '-okv' in args
    output_to_txt = '-otxt' in args

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
        print("-oxml : Output to XML File")
        print("-ocsv : Output to CSV File")
        print("-okv  : Output as Key Value Pairs")
        print("-otxt : Output to TXT File")
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

    elif output_to_xml:
        root = ET.Element("records")

        for record in sample_data:
            item = ET.SubElement(root, "record")
            for key, value in record.items():
                field = ET.SubElement(item, key)
                field.text = str(value)

        tree = ET.ElementTree(root)
        tree.write("data.xml", encoding="utf-8", xml_declaration=True)

    elif output_to_csv:
        headers = sample_data[0].keys()     # Get CSV headers from keys of first Dictionary

        with open("data.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            for row in sample_data:
                writer.writerow(row)

    elif output_to_kvp:
        with open("data.kpv", "w", encoding="utf-8") as file:
            for record in sample_data:
                for key, value in record.items():
                    file.write(f"{key}={value}\n")
                file.write("\n")

    elif output_to_txt:
        with open("data.txt", "w", encoding="utf-8") as f:
            for record in sample_data:
                line = ", ".join(str(value) for value in record.values())
                f.write(line + "\n")

    else:
        print("*** Please Use a Valid Output Flag to Output the Data ***")
        return


if __name__ == "__main__":
    generator(*sys.argv[1:])