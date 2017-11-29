#!/usr/bin/env python

"""
Extract archive files
Convert FLAC to v0 mp3
"""
import sys
import os
import argparse
import pyunpack
import pydub
from util import find
from util import tools
from util import log_lite

logger = log_lite.build_logger(name = __name__, log_format = '[%(asctime)s] %(levelname)s (%(funcName)s:%(lineno)d) %(message)s', date_format = "%H:%M:%S")

# ~~~~~ FUNCTIONS ~~~~~ #
def extract_archive(archive, output_dir = None):
    """
    Extract an archive file

    .... doesnt have a password option??
    """
    if not output_dir:
        # outputdir in same location as archive file
        output_dir = os.path.join(os.path.dirname(archive), os.path.splitext(archive)[0])
    tools.mkdirs(output_dir)
    pyunpack.Archive(archive).extractall(output_dir)

def get_passwords(password_file):
    """
    Read the passwords from a file, one per line
    """
    with open(password_file) as f:
        lines = f.read()
    passwords = [x for x in lines.split('\n') if x != '']
    return(passwords)


def extract_7zip(archive, password, output_dir = None):
    """
    Extract an archive with system installed 7zip

    7z x "$item" -p${password} -y -o"${outdir}"
    """
    if not output_dir:
        # outputdir in same location as archive file
        output_dir = os.path.join(os.path.dirname(archive), os.path.splitext(archive)[0])
    tools.mkdirs(output_dir)

    command = '7z x "{0}" -p{1} -y -o"{2}"'.format(archive, password, output_dir)
    logger.debug('Running:\n' + command)

    run_cmd = tools.SubprocessCmd(command = command).run()
    logger.debug('\n' + run_cmd.proc_stdout)
    logger.debug('\n' + run_cmd.proc_stderr)

    if run_cmd.process.returncode == 0:
        logger.debug("Processes ended successfully")
        return(True)
    else:
        logger.error("Process did not end successfully")
        return(False)









# ~~~~~ RUN ~~~~~ #
password_file = sys.argv.pop(1)
if not tools.item_exists(item = password_file, item_type = 'file'):
    logger.error('password_file is not a file')
    sys.exit()
input_dirs = sys.argv[1:]

# make sure the inputs are actually dirs
valid_input_dirs = []
for input_dir in input_dirs:
    if not tools.item_exists(item = input_dir, item_type = 'dir'):
        logger.error('{0} is not a directory'.format(input_dir))
    else:
        valid_input_dirs.append(input_dir)


passwords = get_passwords(password_file = password_file)
logger.debug(passwords)
logger.debug(valid_input_dirs)

# list to hold the archives we find in the dirs
archives = []

for input_dir in valid_input_dirs:
    # find the archive files in the dir
    matches = find.find(search_dir = input_dir,
                        inclusion_patterns = ('*.rar', '*.zip', '*.7z'),
                        search_type = 'file',
                        match_mode = "any")
    for item in matches:
        archives.append(item)
logger.debug(archives)

for password in passwords:
    for archive in archives:
        extract_7zip(archive = archive, password = password)
# pyunpack.Archive(filename = archive).extractall(directory = outdir)
# os.path.splitext(x)
