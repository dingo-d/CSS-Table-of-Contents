"""Definitions for the "CSS Table of Contents" plugin for ST3

This module contains all the definitions used in the main file for the
CSS Table of Contents plugin.

"""

import re
from itertools import chain

# Pattern constants
SECTION_PREFIX = '/*************** '
SECTION_SUFFIX = ' ***************/'
SUB_SECTION_PREFIX = '/*****---------- '
SUB_SECTION_SUFFIX = ' ----------*****/'
SUB_SUB_SECTION_PREFIX = '/**------------- '
SUB_SUB_SECTION_SUFFIX = ' -------------**/'
SECTION_PATTERN = r'^(\/\*\*\*\*\*\*\*\*\*\*\*\*\*\*\* \d+)'
SUB_SECTION_PATTERN = r'^(\/\*\*\*\*\*\-\-\-\-\-\-\-\-\-\- \d+\.\d+)'
SUB_SUB_SECTION_PATTERN = r'^(\/\*\*\-\-\-\-\-\-\-\-\-\-\-\-\- \d+\.\d+\.\d+)'


def get_section(contents, selected, line):
    """ Function that returns the section.

    The function takes contents above the pointer, looks at the selection or line,
    and create a secion based on the contents (if there is a section or not), on the
    line.

    Args:
        contents (str): The contents above the pointer.
        selected (str): Selected text to be the name of the section.
        line (str): The line where the pointer is.

    Returns:
        str: The section string with prefixes and suffixes and correct
             section number.
    """
    if len(selected) == 0:
        if len(line) == 0:
            text = 'Section'
        else:
            text = line
    else:
        text = selected

    # Numbers check
    section = re.findall(SECTION_PATTERN, contents, re.MULTILINE|re.DOTALL)

    if section:
        section_no = int(re.findall(r'(\d+)', section[len(section)-1])[0])
    else:
        section_no = 0

    section_no += 1

    return SECTION_PREFIX+ str(section_no) +'. '+ text +SECTION_SUFFIX+'\n'


def get_subsection(contents, selected, line):
    """ Function that returns the sub section.

    The function takes contents above the pointer, looks at the selection or line,
    and create a sub secion based on the contents (if there is a sub section or not), on the
    line.

    Args:
        contents (str): The contents above the pointer.
        selected (str): Selected text to be the name of the sub section.
        line (str): The line where the pointer is.

    Returns:
        str: The sub section string with prefixes and suffixes and correct
             sub section number.
    """
    if len(selected) == 0:
        if len(line) == 0:
            text = 'Subsection'
        else:
            text = line
    else:
        text = selected

    # Numbers check
    section = re.findall(SECTION_PATTERN, contents, re.MULTILINE|re.DOTALL)

    if section:
        section_no = int(re.findall(r'(\d+)', section[len(section)-1])[0])
        subsection = re.findall(SUB_SECTION_PATTERN, contents, re.MULTILINE|re.DOTALL)
        if subsection:
            subsection_nu = re.findall(r'(\d+)\.(\d+)', subsection[len(subsection)-1], re.DOTALL)[0]
            if int(subsection_nu[0]) < section_no:
                subsection_no = 0
            else:
                subsection_no = int(subsection_nu[1])
        else:
            subsection_no = 0

        subsection_no += 1

        return SUB_SECTION_PREFIX+ str(section_no) + '.' + str(subsection_no) +' '+ text +SUB_SECTION_SUFFIX+'\n'
    else:
        return '/*Please insert section first.*/\n'


def get_subsubsection(contents, selected, line):
    """ Function that returns the sub sub section.

    The function takes contents above the pointer, looks at the selection or line,
    and create a sub sub section based on the contents (if there is a sub sub section or not),
    on the line.

    Args:
        contents (str): The contents above the pointer.
        selected (str): Selected text to be the name of the sub sub section.
        line (str): The line where the pointer is.

    Returns:
        str: The section string with prefixes and suffixes and correct
             sub sub section number.
    """
    if len(selected) == 0:
        if len(line) == 0:
            text = 'Subsubsection'
        else:
            text = line
    else:
        text = selected

    # Numbers check
    section = re.findall(SECTION_PATTERN, contents, re.MULTILINE|re.DOTALL)
    subsection = re.findall(SUB_SECTION_PATTERN, contents, re.MULTILINE|re.DOTALL)

    if section and subsection:
        subsubsection = re.findall(SUB_SUB_SECTION_PATTERN, contents, re.MULTILINE|re.DOTALL)

        if subsubsection:
            section_no = int(re.findall(r'(\d+)', section[len(section)-1])[0])
            subsection_no = int(re.findall(r'(\d+)\.(\d+)', subsection[len(subsection)-1], re.DOTALL)[0][1])
            subsubsection_nu = re.findall(r'(\d+)\.(\d+)\.(\d+)', subsubsection[len(subsubsection)-1], re.DOTALL)[0]
            if int(subsubsection_nu[0]) < section_no:
                subsubsection_no = 0
            else:
                if int(subsubsection_nu[1]) < subsection_no:
                    subsubsection_no = 0
                else:
                    subsubsection_no = int(subsubsection_nu[2])
        else:
            section_no = int(re.findall(r'(\d+)', section[len(section)-1])[0])
            subsection_no = int(re.findall(r'(\d+)\.(\d+)', subsection[len(subsection)-1], re.DOTALL)[0][1])
            subsubsection_no = 0

        subsubsection_no += 1

        return SUB_SUB_SECTION_PREFIX+ str(section_no) +'.'+ str(subsection_no) +'.'+ str(subsubsection_no) +' '+ text +SUB_SUB_SECTION_SUFFIX+'\n'
    else:
        return '/*Please insert section and subsection first.*/\n'


def clean_section(contents):
    """ Function that returns the list with the section name
    stripped from the prefixes and suffixes.

    The function takes contents above the pointer, finds the section pattern
    and replaces the pattern prefixes and suffixes from it, and appends it to a list.

    Args:
        contents (str): The contents above the pointer.

    Returns:
        list: List with all the sections sorted.
    """
    section_pat = r'^(\/\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*.+)$'
    all_sections = re.findall(section_pat, contents, re.MULTILINE)
    sections = []

    for section in all_sections:
        section_clean_front = section.replace(SECTION_PREFIX, '')
        section_clean_back = section_clean_front.replace(SECTION_SUFFIX, '')
        sections.append(section_clean_back)

    return sections


def clean_subsection(contents):
    """ Function that returns the list with the sub section name
    stripped from the prefixes and suffixes.

    The function takes contents above the pointer, finds the sub section pattern
    and replaces the pattern prefixes and suffixes from it, and appends it to a list.

    Args:
        contents (str): The contents above the pointer.

    Returns:
        list: List with all the sub sections sorted.
    """
    subsection_pat = r'^(\/\*\*\*\*\*\-\-\-\-\-\-\-\-\-\-.+)$'
    all_subsections = re.findall(subsection_pat, contents, re.MULTILINE)
    subsections = []

    for subsection in all_subsections:
        subsection_clean_front = subsection.replace(SUB_SECTION_PREFIX, '')
        subsection_clean_back = subsection_clean_front.replace(SUB_SECTION_SUFFIX, '')
        subsections.append(subsection_clean_back)

    return subsections


def clean_subsubsection(contents):
    """ Function that returns the list with the sub sub section name
    stripped from the prefixes and suffixes.

    The function takes contents above the pointer, finds the sub sub section pattern
    and replaces the pattern prefixes and suffixes from it, and appends it to a list.

    Args:
        contents (str): The contents above the pointer.

    Returns:
        list: List with all the sub sub sections sorted.
    """
    subsubsection_pat = r'^(\/\*\*\-\-\-\-\-\-\-\-\-\-\-\-\-.+)$'
    all_subsubsections = re.findall(subsubsection_pat, contents, re.MULTILINE)
    subsubsections = []

    for subsubsection in all_subsubsections:
        subsubsection_clean_front = subsubsection.replace(SUB_SUB_SECTION_PREFIX, '')
        subsubsection_clean_back = subsubsection_clean_front.replace(SUB_SUB_SECTION_SUFFIX, '')
        subsubsections.append(subsubsection_clean_back)

    return subsubsections


def get_toc(contents):
    """ Function that returns the table of contents.

    The function takes all the contents in the file and returns the
    ready and indented table of contents.

    Args:
        contents (str): The contents in the file.

    Returns:
        str: The table of contents to be placed at the top of the .css file.
    """
    sections = clean_section(contents)
    subsections = clean_subsection(contents)
    subsubsections = clean_subsubsection(contents)

    sorted_list = list(sorted(chain.from_iterable((sections, subsections, subsubsections)),
                              key=lambda x: [int(i) for i in re.findall(r'\d+', x)]))

    toc = ''

    for tocitem in sorted_list:

        if re.match(r'(\d+)\.(\d+)\.(\d+)', tocitem):
            toc += '\t\t' + tocitem + '\n'
        elif re.match(r'(\d+)\.(\d+)', tocitem):
            toc += '\t' + tocitem + '\n'
        else:
            toc += tocitem + '\n'

    return '/*\n\n[Table of Contents]\n\n' + toc + '\n*/\n\n'


def get_toc_lines_count(contents):
    """ Function gets number of lines in the TOC in text.
    Gets 0 if no TOC present at begin.
    """
    items = contents.splitlines()
    if not items or not items[0].startswith('/*'): 
        return 0
        
    res = items.index('*/')
    if (res+1<len(items)) and (items[res+1]==''):
        res += 1
    return res
