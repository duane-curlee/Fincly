# About fincly.py
This Python script is a command-line tool that renames files and folders
to be universally compliant. This allows files to be copied to other
devices without worry of filename compatibility issues.

The name Fincly is a contraction from '**F**ile **N**ame **CLE**aner'.
But spelled with a 'y' instead. It's better that way.

Fincly is intended to be cross-platform, but has not yet been tested on
Linux or Mac, only on my own Windows machines... and it works fine on my
machine! ;-) Fincly is not prepared to work with semaphores, strange
links, special files, device files, etc. But I intend to develop this
script to handle more situations as I find them.

## Decision-making process of Fincly
The first step is to remove the extension from the filename and
clean both filenames and folder names with the same rules. From now
on, both are referred as 'the filename', although this means both names
of files and folders.

The first rule is to remove strings from the filenames the user
specified using the **-r** or **--remove** option. The gap is closed.

Secondly, the ampersand character (&) is changed into the word 'and',
with a space before and after. The at-sign (@) is changed into the word
'at', spaces before and after. And the pound sign is changed into the
word 'number', spaces before and after. And any space-dash-space (' - ')
found, is changed into just a space.

Each of these characters are changed into a space:

```
, " ( ) [ ] { } ~ ! $ % ^ * ; : + = ' ’ ´ ` .
```

And then any and all spaces bunched together within the filename are
folded down into just one space character.

This script then checks if the user chose to have all filenames
all-lowercase'd, if so, then lower-cases them. Then fincly.py will
re-attach the file's extension, then compare the before and after
filenames to check for a difference.

But if the user did not choose the all-lowercase option, the script will
only lowercase the words in the filename that are also in the
lowercase_words list, and then capitalize the first word of the
filename.

### What's a duplicate?
If Fincly decides to change a filename, it first ensures there not a file already
preset with that new name. If so, Fincly reports this as a duplicate and
skips the file-renaming procedure. Be sure to look for duplicates and
resolve them, and run fincly.py again.

If no change in the filenames is needed, of course the file-renaming
procedure will be skipped.

### Why won't Fincly rename my file or folder?
Besides duplicates, another reason a file or folder won't get renamed
may be due to the use of the **-r** or **--remove** option. If you
remove all the words from the file's name, there is nothing to which
rename the file. Fincly will just ignore the word removal request for
that file and continue cleaning the file as usual, without reporting the
issue. Be sure to change your removal options to confirm the issue, and
to choose a better filename regardless.

## Yet to do
At this time, Fincly does not handle read-only files. A Python exception
will be thrown if this script comes across read-only files. I recommend
resolving the file attributes, then just run this script again.

## Command-line help, for reference
This Python script is a command-line tool that renames files and folders
to be universally compliant. This allows the compliant files to be
copied to other devices without worry of filename compatibility issues.
This script will check and possibly rename files and folders provided in
the command line arguments, and traverse into those folders and possibly
rename those found files and folders, too. This script does not alter
the contents of files, nor does it ask permission, be sure the answer is
'Yes' when you press Enter.

