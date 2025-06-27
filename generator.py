import sys
import json
from faker import Faker
import xml.etree.ElementTree as ET
import csv

def generator(*args):
    fake = Faker()
    sample_data = []
    extracted_flags = set()
    field_map = {}
    
    valid_flags = ['-fn', '-sn', '-d', '-ip', '-r', '-tf', '-g', '-ot', '-oj', '-oxml', '-ocsv', '-okv', '-otxt', '-help', '-p', '-ts', '-us', '-e', '-sess', '-mac']
    
    # Defaults
    min_num = 0
    max_num = 1000
    generate_count = 0
    pretty_print = None

    # Output types
    output_to_terminal = '-ot' in args
    output_to_json = '-oj' in args
    output_to_xml = '-oxml' in args
    output_to_csv = '-ocsv' in args
    output_to_kvp = '-okv' in args
    output_to_txt = '-otxt' in args

    # Help menu
    if not args or '-help' in args:
        print("Flags and Their Actions:\n")
        print("-help : Show Help")
        print("KEY-FLAG Mappings (example: full_name-fn):")
        print("  -fn   : First Name")
        print("  -sn   : Surname")
        print("  -d    : Date")
        print("  -ip   : IPv4 Address")
        print("  -r    : Random Number in Range 0-1000")
        print("  -tf   : True/False")
        print("  -ts   : Timestamp")
        print("  -us   : Username")
        print("  -e    : Email")
        print("  -sess : Session ID")
        print("  -mac  : MAC Address")
        print("Other Flags:")
        print("  -g#   : Number of Records to Generate (e.g. -g10)")
        print("  -ot   : Output to Terminal")
        print("  -oxml : Output to XML File")
        print("  -ocsv : Output to CSV File")
        print("  -okv  : Output as Key Value Pairs")
        print("  -otxt : Output to TXT File")
        print("  -oj   : Output to JSON File")
        print("  -p    : Pretty Print\n")
        print("Example:\n  python generator.py name-fn surname-sn ip-ip -g5 -ot")
        return

    # Parse generation count, keys and values and pretty flag
    for arg in args:
        if arg.startswith('-g') and arg[2:].isdigit():
            generate_count = int(arg[2:])
        elif '-' in arg and not arg.startswith('-'):
            try:
                key, val = arg.rsplit('-', 1)
                val = '-' + val
                if val in valid_flags:
                    field_map[key] = val
                else:
                    extracted_flags.add(val)
            except ValueError:
                continue
        elif '-p' in arg:
            pretty_print = True
        
    if extracted_flags:
        print(f"*** Invalid Flag(s): {', '.join(extracted_flags)}  ***")
        print("*** Use the '-help' Flag for a List of Valid Flags ***")
        return

    if generate_count == 0:
        print("*** Use the '-g' Flag Followed by a Number to Specify How Many Records to Produce ***")
        return

    # Generate sample data
    for i in range(generate_count):
        entry = {}
        for key, flag in field_map.items():
            if flag == '-fn':
                entry[key] = fake.first_name()
            elif flag == '-sn':
                entry[key] = fake.last_name()
            elif flag == '-d':
                entry[key] = fake.date()
            elif flag == '-r':
                entry[key] = fake.random_int(min=min_num, max=max_num)
            elif flag == '-tf':
                entry[key] = fake.boolean()
            elif flag == '-ip':
                entry[key] = fake.ipv4_private()
            elif flag == '-ts':
                entry[key] = fake.date_time().isoformat()
            elif flag == '-us':
                entry[key] = fake.user_name()
            elif flag == '-e':
                entry[key] = fake.email()
            elif flag == '-sess':
                entry[key] = fake.uuid4()
            elif flag == '-mac':
                entry[key] = fake.mac_address()

        sample_data.append(entry)


    # Output handling
    if output_to_terminal:
        if pretty_print:
            print(json.dumps(sample_data, indent=2))
        else:
            print(json.dumps(sample_data))

    elif output_to_json:
        with open("data.json", "w") as f:
            if pretty_print:
                json.dump(sample_data, f, indent=2)
            else:
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
        headers = sample_data[0].keys()
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
                line = ", ".join(f"{k}={v}" for k, v in record.items())
                f.write(line + "\n")

    else:
        print("*** Please Use a Valid Output Flag to Output the Data ***")

if __name__ == "__main__":
    generator(*sys.argv[1:])
