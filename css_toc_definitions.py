#
# Definitions for the "CSS Table of Contents" plugin for ST3
#

import re
import heapq
from itertools import chain

# Pattern constants
SECTION_PREFIX = '/*************** '
SECTION_SUFFIX = ' ***************/'
SUB_SECTION_PREFIX = '/*****---------- '
SUB_SECTION_SUFFIX = ' ----------*****/'
SUB_SUB_SECTION_PREFIX = '/**------------- '
SUB_SUB_SECTION_SUFFIX = ' -------------**/'
SECTION_PATTERN = '^(\/\*\*\*\*\*\*\*\*\*\*\*\*\*\*\* \d+)'
SUB_SECTION_PATTERN = '^(\/\*\*\*\*\*\-\-\-\-\-\-\-\-\-\- \d+\.\d+)'
SUB_SUB_SECTION_PATTERN = '^(\/\*\*\-\-\-\-\-\-\-\-\-\-\-\-\- \d+\.\d+\.\d+)'

def get_section(contents, selected, line):

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
        section_no = int(re.findall('(\d+)',section[len(section)-1])[0])
    else:
        section_no = 0

    section_no += 1

    return SECTION_PREFIX+ str(section_no) +'. '+ text +SECTION_SUFFIX+'\n'


def get_subsection(contents, selected, line):

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
        section_no = int(re.findall('(\d+)',section[len(section)-1])[0])
        subsection = re.findall(SUB_SECTION_PATTERN, contents, re.MULTILINE|re.DOTALL)
        if subsection:
            subsection_nu = re.findall('(\d+)\.(\d+)',subsection[len(subsection)-1],re.DOTALL)[0]
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
            section_no = int(re.findall('(\d+)',section[len(section)-1])[0])
            subsection_no = int(re.findall('(\d+)\.(\d+)',subsection[len(subsection)-1],re.DOTALL)[0][1])
            subsubsection_nu = re.findall('(\d+)\.(\d+)\.(\d+)',subsubsection[len(subsubsection)-1],re.DOTALL)[0]
            if int(subsubsection_nu[0]) < section_no:
                subsubsection_no = 0
            else:
                if int(subsubsection_nu[1]) < subsection_no:
                    subsubsection_no = 0
                else:
                    subsubsection_no = int(subsubsection_nu[2])
        else:
            section_no = int(re.findall('(\d+)',section[len(section)-1])[0])
            subsection_no = int(re.findall('(\d+)\.(\d+)',subsection[len(subsection)-1],re.DOTALL)[0][1])
            subsubsection_no = 0

        subsubsection_no += 1

        return SUB_SUB_SECTION_PREFIX+ str(section_no) +'.'+ str(subsection_no) +'.'+ str(subsubsection_no) +' '+ text +SUB_SUB_SECTION_SUFFIX+'\n'
    else:
        return '/*Please insert section and subsection first.*/\n'


def clean_section(contents):
    section_pat = r'^(\/\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*.+)$'
    all_sections = re.findall(section_pat, contents, re.MULTILINE)
    sections = []

    for section in all_sections:
        section_clean_front = section.replace(SECTION_PREFIX, '')
        section_clean_back = section_clean_front.replace(SECTION_SUFFIX, '')
        sections.append(section_clean_back)

    return sections


def clean_subsection(contents):

    subsection_pat = r'^(\/\*\*\*\*\*\-\-\-\-\-\-\-\-\-\-.+)$'
    all_subsections = re.findall(subsection_pat, contents, re.MULTILINE)
    subsections = []

    for subsection in all_subsections:
        subsection_clean_front = subsection.replace(SUB_SECTION_PREFIX, '')
        subsection_clean_back = subsection_clean_front.replace(SUB_SECTION_SUFFIX, '')
        subsections.append(subsection_clean_back)

    return subsections


def clean_subsubsection(contents):

    subsubsection_pat = r'^(\/\*\*\-\-\-\-\-\-\-\-\-\-\-\-\-.+)$'
    all_subsubsections = re.findall(subsubsection_pat, contents, re.MULTILINE)
    subsubsections = []

    for subsubsection in all_subsubsections:
        subsubsection_clean_front = subsubsection.replace(SUB_SUB_SECTION_PREFIX, '')
        subsubsection_clean_back = subsubsection_clean_front.replace(SUB_SUB_SECTION_SUFFIX, '')
        subsubsections.append(subsubsection_clean_back)

    return subsubsections


def get_toc(contents):

    sections = clean_section(contents)
    subsections = clean_subsection(contents)
    subsubsections = clean_subsubsection(contents)

    sorted_list = list(sorted(chain.from_iterable((sections, subsections, subsubsections)), key = lambda x: [int(i) for i in re.findall(r'\d+', x)]))

    toc = ''

    for tocitem in sorted_list:

        if re.match('(\d+)\.(\d+)\.(\d+)', tocitem):
            toc += '\t\t' + tocitem + '\n'
        elif re.match('(\d+)\.(\d+)', tocitem):
            toc += '\t' + tocitem + '\n'
        else:
            toc += tocitem + '\n'

    return '/*\n\n[Table of Contents]\n\n' + toc + '\n*/\n\n'
