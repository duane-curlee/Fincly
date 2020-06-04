#
# Developed by Duane Curlee
# duane.curlee@gmail.com
# https://github.com/duane-curlee
#
# Check for updates here:
# https://github.com/duane-curlee/Fincly
#
import os
from argparse import ArgumentParser
from glob import glob

ill_chars_space = ',"()[]{}~!$%^*;:+='
ill_chars_remove = "'’´`."
lowercase_words = (' With ', ' As ', ' At ', ' If ', ' Is ', ' The ', ' Of ',
                   ' Am ', ' A ', ' An ', ' And ', ' Are ', ' On ', ' Or ',
                   ' It ', ' In ', ' Into ', ' Up ', ' To ', ' From', ' N ',
                   ' Its ')

def parse_input():
    parser = ArgumentParser(description = 'File and folder name cleaner',
        prog = 'fincly.py',
        epilog = "This Python script is a command-line tool that renames\
        files and folders to be universally compliant. This allows the\
        compliant files to be copied to other devices without worry of\
        filename compatability issues. This script will check and\
        possibly rename files and folders provided in the command line\
        arguments, and traverses into those folders and will possibly\
        rename those, too. This script does not alter the contents of files.\
        This script does not ask permission, be sure the answer is 'Yes'\
        when you press Enter.")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l', '--lowercase',  action="store_true",
        help='Make all letters in filenames and folders lowercase')
    group.add_argument('-c', '--capitalize', action="store_true",
        help='Capitalize each word in the filename (but not the extention)')
    parser.add_argument('-f', '--folder',   action="store_true",
        help='Only check the folder names, do not travers into the folders')
    parser.add_argument('-v', '--verbose',   action="store_true",
        help='Enable verbose mode')
    parser.add_argument('-r', '--remove', nargs = '+', type = str, metavar = 'string',
        help = 'The string(s) is removed from within all filenames and folder names, use quotes')
    parser.add_argument('-a', '--add', nargs = '+', type = str, metavar = 'word',
        help = 'Adds words into the lowercase_words list, (not permanent)')
    parser.add_argument('items', nargs='+', metavar = 'items',
        help = 'File and/or Folder names (required) for processing, wildcards welcome')

    return parser.parse_args()

def file_exists_case(the_file):
    if not os.path.isfile(the_file):
        return False

    directory, filename = os.path.split(the_file)

    return filename in os.listdir(directory)

def str_capper(our_string):
    new_list = list()
    
    for word in our_string.split():
        new_list.append(word.capitalize())

    return ' '.join(new_list)

def lowercase_this(our_string):
    for our_word in lowercase_words:
        while our_word in our_string:
            result = our_string.find(our_word)
            our_string = \
                our_string[0:result] + \
                our_word.lower() + \
                our_string[result + len(our_word):]

    return our_string

def fincly(our_string):
    if args.remove:
        tmp_string = our_string
        for del_str in args.remove:
            while del_str in our_string:
                our_string = our_string.replace(del_str, ' ')

        if len(our_string) < 1 or not any(c.isalnum() for c in our_string):
            our_string = tmp_string

    while '&' in our_string:
        result = our_string.find('&')
        our_string = our_string[0:result] + ' and ' + our_string[result + 1:]

    while '@' in our_string:
        result = our_string.find('@')
        our_string = our_string[0:result] + ' at ' + our_string[result + 1:]

    while '#' in our_string:
        result = our_string.find('#')
        our_string = our_string[0:result] + ' number ' + our_string[result + 1:]

    while ' - ' in our_string:
        result = our_string.find(' - ')
        our_string = our_string[0:result] + our_string[result + 2:]

    for our_char in ill_chars_space:
        while our_char in our_string:
            result = our_string.find(our_char)
            our_string = our_string[0:result] + ' ' + our_string[result + 1:]

    for our_char in ill_chars_remove:
        while our_char in our_string:
            result = our_string.find(our_char)
            our_string = our_string[0:result] + our_string[result + 1:]

    while '  ' in our_string:
        our_string = ' '.join(our_string.split())

    our_string = our_string.strip()

    if args.lowercase:
        our_string = our_string.lower()
    else:
        our_string = lowercase_this(our_string)

        if \
        len(our_string) > 4 and \
        our_string[0].isnumeric and \
        our_string[1].isnumeric and \
        our_string[2] == ' ' and \
        our_string[3].isalpha:
            our_string = our_string[:3] + our_string[3].upper() + our_string[4:]

        if \
        len(our_string) > 6 and \
        our_string[0].isnumeric and \
        our_string[1].isnumeric and \
        our_string[2].isnumeric and \
        our_string[3].isnumeric and \
        our_string[4] == ' ' and \
        our_string[5].isalpha:
            our_string = our_string[:5] + our_string[5].upper() + our_string[6:]

    if args.capitalize:
        our_string = str_capper(our_string)
        our_string = lowercase_this(our_string)

    return our_string

def fincly_file(this_file):
    global count_file_saw, count_file_ren, count_file_dup
    orig_file = this_file

    the_folder, the_file = os.path.split(this_file)
    the_fn, the_ext = os.path.splitext(the_file)

    the_fn = fincly(the_fn)

    if the_ext.lower() == '.jpeg':
        the_ext = '.jpg'

    the_file = the_fn.strip() + the_ext.lower()
    this_file = os.path.join(the_folder, the_file)

    if this_file != orig_file:
        if file_exists_case(this_file):
            count_file_saw += 1
            count_file_dup += 1
            print(' Cannot rename, skipping :', orig_file)
            print(' Filename already exists :', this_file)
        else:
            count_file_ren += 1
            count_file_saw += 1
            print('  Renaming file :', orig_file)
            print('             to :', this_file)
            os.rename(orig_file, this_file)
    else:
        count_file_saw += 1
        if args.verbose:
            print('  Skipping file :', orig_file)

def fincly_root(this_dir):
    global count_dirs_saw, count_dirs_ren, count_dirs_dup
    orig_dir = this_dir

    the_folder, the_dir = os.path.split(this_dir)
    the_dir = fincly(the_dir)
    this_dir = os.path.join(the_folder, the_dir)

    if this_dir != orig_dir:
        if file_exists_case(this_dir):
            count_dirs_saw += 1
            count_dirs_dup += 1
            print('Cannot rename, skipping :', orig_dir)
            print('Folder already exists   :', this_dir)
        else:
            count_dirs_saw += 1
            count_dirs_ren += 1
            print('  Renaming folder :', orig_dir)
            print('              to :', this_dir)
            os.rename(orig_dir, this_dir)
    else:
        count_dirs_saw += 1
        if args.verbose:
            print('  Skipping folder :', orig_dir)

    return this_dir

def fincly_dirs(our_dir):
    global count_dirs_saw, count_dirs_ren, count_dirs_dup
    for root, dirs, files in os.walk(our_dir):
        dirs[:]  = [d for d in dirs  if not d.startswith('.')]
        files[:] = [f for f in files if not f.startswith('.')]

        if args.verbose:
            print('Proccessing folder:', root)

        for this_dir in dirs:
            orig_dir = this_dir

            this_dir = fincly(this_dir)

            if this_dir != orig_dir:
                this_dir_full = os.path.join(root, this_dir)
                orig_dir_full = os.path.join(root, orig_dir)

                if file_exists_case(this_dir_full):
                    count_dirs_saw += 1
                    count_dirs_dup += 1
                    print('Cannot rename, skipping :', orig_dir_full)
                    print('Folder already exists   :', this_dir_full)
                else:
                    count_dirs_saw += 1
                    count_dirs_ren += 1
                    print('  Renaming folder :', orig_dir_full)
                    print('               to :', this_dir_full)
                    os.rename(orig_dir_full, this_dir_full)

                    for index, value in enumerate(dirs):
                        if value == orig_dir:
                            dirs[index] = this_dir

            else:
                count_dirs_saw += 1

        for the_file in files:
            fincly_file(os.path.join(root, the_file))

if __name__ == '__main__':
    count_dirs_ren = 0
    count_dirs_saw = 0
    count_dirs_dup = 0
    count_file_ren = 0
    count_file_saw = 0
    count_file_dup = 0

    our_cwd = os.getcwd()
    args = parse_input()
    
    if args.add:
        for new_word in args.add:
            lowercase_words += (' ' + new_word.strip().capitalize() + ' ',)

    for current_item in args.items:
        for this_item in glob(current_item):
            this_item = os.path.abspath(this_item)
            if os.path.isdir(this_item):
                if this_item == our_cwd:
                    fincly_dirs(this_item)
                elif this_item in our_cwd:
                    print('No can do:', this_item,
                        'is within our current working directory')
                elif args.folder:
                    this_item = fincly_root(this_item)
                else:
                    this_item = fincly_root(this_item)
                    fincly_dirs(this_item)

            elif os.path.isfile(this_item):
                fincly_file(this_item)
            else:
                print('What is this? :', this_item)

    print('Files found     :', count_file_saw)
    print('Files renamed   :', count_file_ren)
    print('Folders found   :', count_dirs_saw)
    print('Folders renamed :', count_dirs_ren)

    if args.verbose:
        print('Duplicate filenames found : ', count_file_dup)
        print('Duplicate folders found   : ', count_dirs_dup)
    elif count_file_dup > 0:
        print('NOTE: Duplicate filenames found : ', count_file_dup)
    elif count_dirs_dup > 0:
        print('NOTE: Duplicate folders found   : ', count_dirs_dup)
