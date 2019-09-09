import os
import sys
import re
import stat
import gzip
import json
import yaml
import datetime
import subprocess


def printError(message):
    """
    Print error message(s) on screen with red color.
    """
    print('\033[1;31m' + str(message) + '\033[0m')

def printGreen(message):
    """
    Print highlight message(s) on screen with red color.
    """
    print('\033[1;32m' + str(message) + '\033[0m')

def printWarning(message):
    """
    Print warning message(s) on screen with yellow color.
    """
    print('\033[1;33m' + str(message) + '\033[0m')

def openWrite(file, mode, message):
    """
    Open a file and write specified message(s) with specified mode ('a'/'w').
    """
    if mode != 'a' and mode != 'w':
        printError('*Error*: the write mode for sub-function "openWrite" can only be "a" or "w".')
        sys.exit(1)

    try:
        FL = open(file, mode)
        FL.write(message)
        FL.close()
    except Exception as error:
        printError('*Error*: Failed to open file "' + str(file) + '" for read/write, ' + str(error))
        sys.exit(1)

def doublePrint(file, mode, message):
    """
    Print the message(s) on both of screen and specified file.
    """
    print(message)
    openWrite(file, mode, str(message) + '\n')

def doublePrintError(file, mode, message):
    """
    Print error message(s) on both of screen and specified file, it is red color on screen.
    """
    printError(message)
    openWrite(file, mode, str(message) + '\n')

def doublePrintWarning(file, mode, message):
    """
    Print warning message(s) on both of screen and specified file, it is yellow color on screen.
    """
    printWarning(message)
    openWrite(file, mode, str(message) + '\n')

def showCommand(file):
    """
    Print the input arguments on both of screen and specified file.
    """
    command = ""
    for arg in sys.argv:
        command = command + ' ' + arg

    length = 13 + len(command)
    doublePrint(file, 'a', '*'*length)
    doublePrint(file, 'a', '* COMMAND :' + command + ' *')
    doublePrint(file, 'a', '*'*length)
    doublePrint(file, 'a', '')

def sourceShell(shellFile):
    """
    Supply a cshell environment variable configuration file, enable the environment variable settings on python script.
    """
    if os.path.exists(shellFile):
        if not os.path.isfile(shellFile) and not os.path.islink(shellFile):
            printError('*Error*: "' + str(shellFile) + '" is not a file, cannot source it.')
            sys.exit(1)
    else:
        printError('*Error*: File "' + str(shellFile) + '" is missing.')
        sys.exit(1)

    ENV = os.popen("tcsh -f -c 'source " + str(shellFile) + "; env'").readlines()

    for env in ENV:
        env = env.strip() 
        if re.match('^([^ ]+)=([^ ]+)$', env):
            envMatch = re.match('^([^ ]+)=([^ ]+)$', env)
            os.environ[envMatch.group(1)] = envMatch.group(2)

def subprocessPopen(command, mystdin=subprocess.PIPE, mystdout=subprocess.PIPE, mystderr=subprocess.PIPE):
    """
    Run system command with subprocess.Popen, get returncode/stdout/stderr.
    """
    SP = subprocess.Popen(command, shell=True, stdin=mystdin, stdout=mystdout, stderr=mystderr)                                                                                                                    
    (stdout, stderr) = SP.communicate()
    return(SP.returncode, stdout, stderr)

def debug(message):
    """
    If environment variable 'METHODOLOGY_DEBUG' is set to '1', print the debug message.
    """
    if "METHODOLOGY_DEBUG" in os.environ:
        if os.environ["METHODOLOGY_DEBUG"] == "1":
            currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print('DEBUG [' + str(currentTime) + ']: ' + str(message))

def getDateBasedOnSpecifiedDate(specifiedDate='', format='%Y%m%d', diff=0):
    """
    Get date which is "diff" days apart from the specified date.
    """
    if specifiedDate == '':
        print('*Error*: specifiedDate is not specified.')
        sys.exit(1) 
    else:
        try:
            stdSpecifiedDate = datetime.datetime.strptime(specifiedDate, format)
        except Exception as error:
            print('*Error*: "' + str(specifiedDate) + '": invalid begin date.')
            sys.exit(1)

        resultDate = stdSpecifiedDate + datetime.timedelta(days=int(diff))
        resultDate = resultDate.strftime(format)
        return(resultDate) 

def getDateList(beginDate='', endDate='', format='%Y%m%d'):
    """
    Gei data list between begin date and end data.
    """
    dateList = []

    if beginDate == '':
        print('*Error*: begin date is not specified.')
        sys.exit(1) 
    elif endDate == '':
        print('*Error*: end date is not specified.')
        sys.exit(1) 
    elif int(beginDate) >= int(endDate):
        print('*Error*: beginDate cannot be later than endData!.')
        sys.exit(1) 
    else:
        try:
            stdBeginDate = datetime.datetime.strptime(beginDate, format)
        except Exception as error:
            print('*Error*: "' + str(beginDate) + '": invalid begin date.')
            sys.exit(1)

        try:
            stdEndDate = datetime.datetime.strptime(endDate, format)
        except Exception as error:
            print('*Error*: "' + str(endDate) + '": invalid end date.')
            sys.exit(1)

        while stdBeginDate <= stdEndDate:
            formatDate = stdBeginDate.strftime(format) 
            dateList.append(formatDate)
            stdBeginDate += datetime.timedelta(days=1)

        return(dateList)

def tryCommand(command, errorMessage='*Error*: Failed on executing system command'):
    """
    Execute a system command, exit 1 with any error.
    """
    try:
        os.system(command)
    except Exception as error:
        print(str(errorMessage) + ': ' + str(error))
        sys.exit(1)


#-----------------------------
# Useful Class Object
#----------------------------- 
class Partten:
    """Compile a pattern 

    Attributes:
        re_str : string to be matched
        re     : re object

    """
    def __init__(self, re_str):
        self.re_str = re_str
        self.re = re.compile(re_str, re.M|re.S)
        self.sub = self.re.sub

    def is_found(self, line):
        """If found(not found), reutrn True(False)."""

        m = self.re.search(line)
        if (m == None):
            return False
        else:
            return True

    def findall (self, line):
        """If found(not found), reutrn matched list(None) """

        return self.re.findall(line)

    def match(self, line):
        """If found(not found), reutrn matched list(None) """
        m = self.re.match(line)
        if (m==None):
            return None
        else:
            ls = list()
            for s in m.groups():
                ls.append(s.strip('"'))
            return ls


class ExcuteShell:
    """Excute shell cmd in python scripts and return output

    Attributes:
        output : message from shell cmds
        
    """
    def __init__(self, cmd):
        self.output = os.popen(cmd).read()

    def return_string(self):
        """Return shell print as stirngs."""
        return self.output

    def return_list(self):
        """Return shell print as list."""
        outputstring = self.output.split('\n')
        return outputstring[:-1]


#-----------------------------
# File and Directory handling 
#----------------------------- 
def get_root_files(path):
    """Get all first-level directories under the specified directory.

    Args:
        path : specified directory

    Returns:
        A list directory names get from specified directory
        
    """
    for root, dirs, files in os.walk(path):
        if root == path:
            return files


def get_root_dirs(path):
    """Get all first-level fiies under the specified directory.

    Args:
        path : specified directory

    Returns:
        A list file names get from specified directory
        
    """
    for root, dirs, files in os.walk(path):
        if root == path:
            return dirs


def get_filename_from_path(filepath):
    """get file name from filepath

    Args:
        filepath : file name or file path

    Returns:
        A string of filename itself

    """
    filename = Partten(r'(?:.*\/)?(\S+)')
    filename.is_found(filepath)
    name = filename.match(filepath)[0]
    return name


def remove_file_suffix(filepath, suffix='\.'):
    """Remove file suffix from file name or file path

    Args:
        filepath : filename or file path
        suffix   : filename's suffix, default is dot

    Returns:
        A string of filename without suffix
    """
    filename = Partten(r"(?:.*\/)?(.*?)" + suffix)
    if filename.is_found(filepath):
        name = filename.match(filepath)[0]
        return name
    else:
        print (''.join([filepath,' is not end with  ', suffix, '*']))
        return 

def remove_file_prefix(filepath, suffix='\.'):
    """Remove file suffix from file name or file path

    Args:
        filepath : filename or file path
        suffix   : filename's suffix, default is dot

    Returns:
        A string of filename without perfix
    """
    filename = Partten(r"(?:.*\/)?(.*?)" + suffix + "(.*)")
    if filename.is_found(filepath):
        name = filename.match(filepath)[1]
        return name
    else:
        print (''.join([filepath,' is not end with  ', suffix, '*']))
        return 

def get_file_as_array(filepath):
    """Open a specified file as array, supported .gz file

    Args:
        failepath : specified file path

    Returns:
        A string of specified file
        
    """
    if filepath.endswith('.gz'):
        with gzip.open(filepath, 'r') as f:
            lines = f.readlines()
    else:
        with open(filepath, 'r') as f:
            lines = f.readlines()
    return lines


def get_file_as_string(filepath):
    """Open a specified file as string, supported .gz file

    Args:
        failepath : specified file path

    Returns:
        A string of specified file
        
    """
    if filepath.endswith('.gz'):
        with gzip.open(filepath, 'r') as f:
            lines = f.readlines()
    else:
        with open(filepath, 'r') as f:
            lines = f.readlines()
    return ''.join(lines)

def gen_json_file(data, path):
    """Generate a json format file to specified path

    Args:
        data : data to be saved

    Returns:
        json file

    """
    with open(path, 'w') as tmp:
        json.dump(data, tmp)
        tmp.close

def load_json_file(path):
    """Load JSON file
        
    Args:
        path : json file path

    Returns:
    rawdata : dic data

    """
    if os.path.exists(path):
        rawdata  = json.load(open(path))
        return rawdata
    else:
        print (''.join(['Error: ', path, ' is not exists!']))
        sys.exit(0)

def load_yaml_file(path):
    """Load YAML file

    Args:
        path : yaml file path

    Returns:
    rawdata : dicdata

    """
    f = open(path)
    cont = f.read()
    rawdata = yaml.load(cont)
    return rawdata


#-----------------------------
# Common Functions 
#----------------------------- 
def get_time():
    return time.strftime("%H:%M:%S", time.localtime()).strip()

