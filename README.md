# SprayGen

Login Spray Generator. 

This is a small script that I wrote in order to automate the annoying part of spray attacks. It creates common username permutations as a wordlist.

## Usage

```default
usage: spraygen.py [-h] [-i INPUT] [-o OUTPUT] [-d DOMAIN] [-v] [-l] [-u] [-e] [-c] [-n]

Login Spray Generator

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        File with names in "Firstname Lastname" format in each line. Single name is allowed as well.
  -o OUTPUT, --output OUTPUT
                        Output filename
  -d DOMAIN, --domain DOMAIN
                        Domain to use for email style usernames
  -v, --verbose         Print all the steps
  -l, --lower           Only lowercase
  -u, --upper           Only uppercase
  -e, --emailonly       Only create email addresses
  -c, --nocolor         Turn off color
  -n, --nologo          Don't print ascii logo

```

There are no library requirements. Use Python 3.x

## Input

Expected input file format:

```default
Max Musterman
Eli Vance
Megatron
Steve Urban
admin
```

So either `"Firstname Lastname"` or just a single `"Username"` in each line.

I did not really optimize this thing, so if you have a large number of input names, then you might want to use some better solution.

## Examples

```bash
# Basic example
spraygen.py -i names.txt -o spraylist.txt
spraygen.py -i names.txt
```
Omitting the output filename will print the created names in the terminal directly.

You can also generate email-style usernames (e.g. `j.smith@domain.com`) using a supplied domain name:

```bash
# Create emails and regular usernames
spraygen.py -i names.txt -d test.local -o spraylist.txt
```

If you only want email addresses and nothing else, then use the `-e` / `--emailonly` parameter:

```bash
# Create only emails
spraygen.py -i names.txt -d test.local -o spraylist.txt -e
```

It is highly recommended to use the `-l` / `--lower` parameter in order to decrease the number of results. Email addresses are also usually lowercase anyway.

```bash
# only lowercase usernames
spraygen.py -i names.txt -o spraylist.txt --lower

# only lowercase emails
spraygen.py -i names.txt -o spraylist.txt -d mydomain.com -el
```