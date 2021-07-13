#!/usr/bin/python3

# Developed by Duane Curlee
# duane.curlee@gmail.com
# https://github.com/duane-curlee
#
# Check for updates here:
# https://github.com/duane-curlee/Fincly

import os
from argparse import ArgumentParser
from glob import glob

class Fincly:
    rem_strings = ("'",)
    ill_char = '.,’´`"()[]{}~!$%^*;:+='
    all_upper = False
    all_lower = False
    insig_word = (' A ', ' Am ', ' An ', ' And ', ' Are ', ' As ', ' At ',\
        ' From', ' If ', ' In ', ' Into ', ' Is ', ' It ', ' Its ', ' N ',\
        ' Of ', ' On ', ' Or ', ' The ', ' To ', ' Up ', ' With ')

    def rem_strings_add(self, our_word):
        if self.rem_strings == None:
            self.rem_strings = (our_word,)
        else:
            self.rem_strings = self.rem_strings + (our_word,)

    def rem_strings_del(self, our_word):
        pass

    def rem_strings_run(self, our_string):
        if self.rem_strings != None:
            tmp_string = our_string
            for del_str in self.rem_strings:
                while del_str in our_string:
                    our_string = our_string.replace(del_str, '')

            if len(our_string) < 1 or not any(c.isalnum() for c in our_string):
                our_string = tmp_string
        return our_string

    def ill_char_add(self, our_char):
        self.ill_char = self.ill_char + our_char

    def ill_char_del(self, our_char):
        pass

    def ill_char_run(self, our_string):
        for our_char in self.ill_char:
            while our_char in our_string:
                our_string = our_string.replace(our_char, ' ')
        return our_string

    def insig_word_add(self, our_word):
        self.insig_word = self.insig_word + (' ' + our_word.strip().capitalize() + ' ',)

    def insig_word_del(self, our_word):
        pass

    def insig_word_run(self, our_string):
        for our_word in self.insig_word:
            while our_word in our_string:
                our_string = our_string.replace(our_word, our_word.lower())
        return our_string

    def str_capper(self, our_string):
        new_list = list()

        for word in our_string.split():
            new_list.append(word.capitalize())

        return ' '.join(new_list)

    def fincly(self, the_string):
        the_string = self.rem_strings_run(the_string)

        while '&' in the_string:
            result = the_string.find('&')
            the_string = the_string[0:result] + ' and ' + the_string[result + 1:]

        while '@' in the_string:
            result = the_string.find('@')
            the_string = the_string[0:result] + ' at ' + the_string[result + 1:]

        while '#' in the_string:
            result = the_string.find('#')
            the_string = the_string[0:result] + ' number ' + the_string[result + 1:]

        while ' - ' in the_string:
            result = the_string.find(' - ')
            the_string = the_string[0:result] + the_string[result + 2:]

        the_string = self.ill_char_run(the_string)

        while '  ' in the_string:
            the_string = ' '.join(the_string.split())

        the_string = the_string.strip()

        if self.all_upper == True and self.all_lower == True:
            the_string = "Yep, you broke Fincly's brain!"
        elif self.all_upper == True:
            the_string = the_string.upper()
        elif self.all_lower == True:
            the_string = the_string.lower()
        else:
            if len(the_string) > 2:
                the_string = self.str_capper(the_string)
                the_string = self.insig_word_run(the_string)

            if len(the_string) > 4 and \
                the_string[0].isnumeric() and \
                the_string[1].isnumeric() and \
                the_string[2].isspace() and \
                the_string[3].isalpha():
                    the_string = the_string[:3] + the_string[3].upper() + the_string[4:]

            if len(the_string) > 6 and \
                the_string[0].isnumeric() and \
                the_string[1].isnumeric() and \
                the_string[2].isnumeric() and \
                the_string[3].isnumeric() and \
                the_string[4].isspace() and \
                the_string[5].isalpha():
                    the_string = the_string[:5] + the_string[5].upper() + the_string[6:]

        return the_string


def file_exists_case(the_file):
    """
    Use this funtion if you need a case-sensitive filename checker.
    Linux does not need this, but Windows does.
    """
    if not os.path.isfile(the_file):
        return False

    directory, filename = os.path.split(the_file)

    return filename in os.listdir(directory)

def fincly_file(this_file):
    global count_file_saw, count_file_ren, count_file_dup
    orig_file = this_file

    the_folder, the_file = os.path.split(this_file)
    the_fn, the_ext = os.path.splitext(the_file)

    the_fn = my_fink.fincly(the_fn)

    if the_ext.lower() == '.jpeg':
        the_ext = '.jpg'

    the_file = the_fn.strip() + the_ext.lower()
    this_file = os.path.join(the_folder, the_file)

    if this_file == orig_file:
        count_file_saw += 1
        if args.verbose:
            print('Skipping, filename ok :', orig_file)
    else:
        count_file_saw += 1
        if os.path.isfile(this_file) == True:
            count_file_dup += 1
            print('Skipping, cannot rename :', orig_file)
            print('Filename already exists :', this_file)
        else:
            if args.preview == True:
                print('    Original :', orig_file)
                print('Preview only :', this_file)
            else:
                count_file_ren += 1
                print('Original :', orig_file)
                print('     New :', this_file)
                os.rename(orig_file, this_file)

def fincly_folder(this_dir):
    global count_dirs_saw, count_dirs_ren, count_dirs_dup
    orig_dir = this_dir

    the_folder, the_dir = os.path.split(this_dir)
    the_dir = my_fink.fincly(the_dir)
    this_dir = os.path.join(the_folder, the_dir)

    if this_dir == orig_dir:
        count_dirs_saw += 1
        if args.verbose:
            print('Skipping, folder name ok :', orig_dir)
    else:
        count_dirs_saw += 1
        if os.path.isdir(this_dir):
            count_dirs_dup += 1
            print('Skipping, cannot rename :', orig_dir)
            print('         Already exists :', this_dir)
        else:
            if args.preview == True:
                print('Origianl folder name :', orig_dir)
                print('        Preview only :', this_dir)

            else:
                count_dirs_ren += 1
                print('Original folder name :', orig_dir)
                print('                 New :', this_dir)
                os.rename(orig_dir, this_dir)
    return this_dir

def fincly_gosub(our_dir):
    global count_dirs_saw, count_dirs_ren, count_dirs_dup
    for root, dirs, files in os.walk(our_dir):
        dirs[:]  = [d for d in dirs  if not d.startswith('.')]
        files[:] = [f for f in files if not f.startswith('.')]

        if args.verbose:
            print('Proccessing folder:', root)

        for this_dir in dirs:
            orig_dir = this_dir

            this_dir = my_fink.fincly(this_dir)

            if this_dir != orig_dir:
                this_dir_full = os.path.join(root, this_dir)
                orig_dir_full = os.path.join(root, orig_dir)

                if os.path.isdir(this_dir_full):
                    count_dirs_saw += 1
                    count_dirs_dup += 1
                    print('Skipping, cannot rename :', orig_dir_full)
                    print('         Already exists :', this_dir_full)
                else:
                    if args.preview == True:
                        count_dirs_saw += 1
                        print('Original folder name :', orig_dir_full)
                        print('        Preview only :', this_dir_full)
                    else:
                        count_dirs_saw += 1
                        count_dirs_ren += 1
                        print('Original folder name :', orig_dir_full)
                        print('                 New :', this_dir_full)
                        os.rename(orig_dir_full, this_dir_full)

                    for index, value in enumerate(dirs):
                        if value == orig_dir:
                            dirs[index] = this_dir

            else:
                count_dirs_saw += 1

        for the_file in files:
            fincly_file(os.path.join(root, the_file))

def parse_input():
    parser = ArgumentParser(description = 'File and folder name cleaner',
        prog = 'fincly.py',
        epilog = "This Python script is a command-line tool that will check\
        and possibly rename files and folders to be universally compliant.\
        This allows files to be copied to other devices without\
        worry of filename compatability issues. This script does not ask\
        permission, be sure the answer is 'Yes' when you press Enter.")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l', '--all_lower',  action="store_true",
        help='Make all letters in filenames and folders lower-case')
    group.add_argument('-u', '--all_upper',  action="store_true",
        help='Make all letters in filenames and folders upper-case')
    parser.add_argument('-v', '--verbose',   action="store_true",
        help='Enable verbose mode')
    parser.add_argument('-p', '--preview',   action="store_true",
        help='Enable preview mode')
    parser.add_argument('-t', '--travers',   action="store_true",
        help='Traverses into sub-folders')
    parser.add_argument('-r', '--remove', nargs = '+', type = str, metavar = 'string',
        help = 'Adds strings to Fincly\'s Removal Strings list (not permanent)')
    parser.add_argument('-a', '--add', nargs = '+', type = str, metavar = 'word',
        help = 'Adds words to Fincly\'s Insignificant Words list (not permanent)')
    parser.add_argument('items', nargs='+', metavar = 'items',
        help = 'File and/or folder names (required) for processing, wildcards welcome')

    return parser.parse_args()

if __name__ == '__main__':
    count_dirs_ren = 0
    count_dirs_saw = 0
    count_dirs_dup = 0
    count_file_ren = 0
    count_file_saw = 0
    count_file_dup = 0
    the_cwd = os.getcwd()
    args = parse_input()
    my_fink = Fincly()
    
    if args.all_lower:
        my_fink.all_lower = args.all_lower

    if args.all_upper:
        my_fink.all_upper = args.all_upper

    if args.remove:
        for rem_word in args.remove:
            my_fink.rem_strings_add(rem_word)

    if args.add:
        for new_word in args.add:
            my_fink.insig_word_add(new_word)

    for current_item in args.items:
        for this_item in glob(current_item):
            this_item = os.path.abspath(this_item)
            if os.path.isdir(this_item):
                if this_item == the_cwd:
                    print('Cannot process:', this_item,
                        '\nReason: our current working directory')
                elif this_item in the_cwd:
                    print('Cannot process:', this_item,
                        '\nReason: upstream of our current working directory')
                elif args.travers == True:
                    this_item = fincly_folder(this_item)
                    fincly_gosub(this_item)
                else:
                    this_item = fincly_folder(this_item)

            elif os.path.isfile(this_item):
                fincly_file(this_item)
            else:
                print('Skipping, unrecognized:', this_item)

    print('\nFiles found     :', count_file_saw)
    print('Files renamed   :', count_file_ren)
    print('Folders found   :', count_dirs_saw)
    print('Folders renamed :', count_dirs_ren)

    if args.verbose:
        print('\nDuplicate filenames found : ', count_file_dup)
        print('Duplicate folders found   : ', count_dirs_dup)
    elif count_file_dup > 0:
        print('\nNOTE: Duplicate filenames found : ', count_file_dup)
    elif count_dirs_dup > 0:
        print('\nNOTE: Duplicate folder names found   : ', count_dirs_dup)
