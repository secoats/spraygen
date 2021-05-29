#!/usr/bin/env python3
from argparse import ArgumentParser
import json
__author__ = 'oats'
__version__ = "v0.1"

logo = '''
███████╗██████╗ ██████╗  █████╗ ██╗   ██╗ ██████╗ ███████╗███╗   ██╗
██╔════╝██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝██╔════╝ ██╔════╝████╗  ██║
███████╗██████╔╝██████╔╝███████║ ╚████╔╝ ██║  ███╗█████╗  ██╔██╗ ██║
╚════██║██╔═══╝ ██╔══██╗██╔══██║  ╚██╔╝  ██║   ██║██╔══╝  ██║╚██╗██║
███████║██║     ██║  ██║██║  ██║   ██║   ╚██████╔╝███████╗██║ ╚████║
╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═══╝
'''

parser = ArgumentParser(description='Login Spray Generator ' + str(__version__) + ' by ' + str(__author__))
parser.add_argument("-i", "--input", type=str, help="File with names in \"Firstname Lastname\" format in each line. Single name is allowed as well.")
parser.add_argument("-o", "--output", type=str, help="Output filename")
parser.add_argument("-d", "--domain", type=str, help="Domain to use for email style usernames")
parser.add_argument("-v", "--verbose", action="store_true", help="Print all the steps")
parser.add_argument("-l", "--lower", action="store_true", help="Only lowercase")
parser.add_argument("-u", "--upper", action="store_true", help="Only uppercase")
parser.add_argument("-e", "--emailonly", action="store_true", default=False, help="Only create email addresses")
parser.add_argument("-c", "--nocolor", action="store_true", default=False, help="Turn off color")
parser.add_argument("-n", "--nologo", action="store_true", default=False, help="Don't print ascii logo")
args = parser.parse_args()

separators = ['', '.', '-']

class Person:
    def __init__(self, line):
        line = line.strip() # remove surrounding whitespace
        
        if not line:
            raise Exception("Empty input for person. Empty line?")

        name_list = line.split(" ")
        self.firstname = name_list[0]
        self.lastname = None

        if len(name_list) > 1:
            self.lastname = name_list[1]
    
    def to_dict(self):
        return { 'firstname': self.firstname, 'lastname': self.lastname }
    
    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()

def print_verbose(*input):
    if args.verbose:
        print(*input)

def blue(input):
    if args.nocolor:
        return input
    return '\33[34m' + '\033[1m' + str(input) + '\033[0m'

def single_name(name):
    if not name:
        return []
    result = set()
    name = name.strip()

    # mixed case
    if not args.lower and not args.upper:
        result.add(name)
        result.add(name.lower().capitalize())

    # lowercase
    if not args.upper:
        result.add(name.lower())
    
    # uppercase
    if not args.lower:
        result.add(name.upper())
    
    return result

def combine_names(firstname, lastname):
    if not firstname or not lastname:
        return []

    result = set()

    for sep in separators:
        # mixed case
        if not args.lower and not args.upper:
            # unchanged
            result.add(firstname + sep + lastname)
            result.add(firstname[0] + sep + lastname)
            result.add(lastname + sep + firstname)
            result.add(lastname[0] + sep + firstname)

            # capitalized
            result.add(firstname.lower().capitalize() + sep + lastname.lower().capitalize())
            result.add(firstname[0].lower().capitalize() + sep + lastname.lower().capitalize())
            result.add(lastname.lower().capitalize() + sep + firstname.lower().capitalize())
            result.add(lastname[0].lower().capitalize() + sep + firstname.lower().capitalize())

        # lowercase
        if not args.upper:
            result.add(firstname.lower() + sep + lastname.lower())
            result.add(firstname[0].lower() + sep + lastname.lower())
            result.add(lastname.lower() + sep + firstname.lower())
            result.add(lastname[0].lower() + sep + firstname.lower())

        # uppercase
        if not args.lower:
            result.add(firstname.upper() + sep + lastname.upper())
            result.add(firstname[0].upper() + sep + lastname.upper())
            result.add(lastname.upper() + sep + firstname.upper())
            result.add(lastname[0].upper() + sep + firstname.upper())

    return result

def make_email(username, domain):
    return username + "@" + domain

def main():
    if not args.nologo:
        print(blue(logo))
    
    print(blue(f"[*] Reading input file: {args.input}"))
    people = []
    with open(args.input, "r") as fi:
        for linenum, line in enumerate(fi):
            try:
                p = Person(line)
                print_verbose(linenum, p)
                people.append(p)
            except Exception as e:
                print_verbose(linenum, e)

    results = set()

    print_verbose(blue("[*] Create name permutations"))
    for p in people:
        fp = single_name(p.firstname)
        sp = single_name(p.lastname)
        cb = combine_names(p.firstname, p.lastname)
        results.update(fp)
        results.update(sp)
        results.update(cb)

    # generate email addresses
    emails = set()
    if args.domain:
        for r in results:
            email = make_email(r, args.domain)
            emails.add(email)

        if args.emailonly:
            results = emails
        else:
            results.update(emails)

    print(blue(f"[*] Number of results: {len(results)}"))

    # print results
    if args.verbose or not args.output:
        for r in sorted(results):
            print(r)

    # write to output file
    if args.output:
        print(blue(f"[*] Writing to output file: {args.output}"))
        with open(args.output, "w") as outputfile:
            for r in sorted(results):
                outputfile.write(r + "\n")

    print(blue(f"[*] Done"))

if __name__ == "__main__":
    main()