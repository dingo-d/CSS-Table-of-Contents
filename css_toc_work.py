#
# Business-logic of "CSS Table of Contents" plugin for ST3
#

import re
import heapq

def work_get_section(contents, selected, line):

    if len(selected) == 0:
        if len(line) == 0:
            text = 'Section'
        else:
            text = line
    else:
        text = selected

    # Numbers check

    section_pat = '^(\/\*\*\*\*\*\*\*\*\*\*\*\*\*\*\* \d+)'
    section = re.findall(section_pat, contents, re.MULTILINE|re.DOTALL)

    if section:
        section_no = int(re.findall('(\d+)',section[len(section)-1])[0])
    else:
        section_no = 0

    section_no += 1
    return '/*************** '+ str(section_no) +'. '+ text +' ***************/\n'


def work_get_subsection(contents, selected, line):

    if len(selected) == 0:
        if len(line) == 0:
            text = 'Subsection'
        else:
            text = line
    else:
        text = selected

    # Numbers check

    section_pat = '^(\/\*\*\*\*\*\*\*\*\*\*\*\*\*\*\* \d+)'
    section = re.findall(section_pat, contents, re.MULTILINE|re.DOTALL)

    if section:
        section_no = int(re.findall('(\d+)',section[len(section)-1])[0])
        subsection_pat = '^(\/\*\*\*\*\*\-\-\-\-\-\-\-\-\-\- \d+\.\d+)'
        subsection = re.findall(subsection_pat, contents, re.MULTILINE|re.DOTALL)
        if subsection:
            subsection_nu = re.findall('(\d+)\.(\d+)',subsection[len(subsection)-1],re.DOTALL)[0]
            if int(subsection_nu[0]) < section_no:
                subsection_no = 0
            else:
                subsection_no = int(subsection_nu[1])
        else:
            subsection_no = 0

        subsection_no += 1

        return '/*****---------- '+ str(section_no) + '.' + str(subsection_no) +' '+ text +' ----------*****/\n'
    else:
        return '/*Please insert section first.*/\n'


def work_get_subsubsection(contents, selected, line):

    if len(selected) == 0:
        if len(line) == 0:
            text = 'Subsubsection'
        else:
            text = line
    else:
        text = selected

    # Numbers check

    section_pat = '^(\/\*\*\*\*\*\*\*\*\*\*\*\*\*\*\* \d+)'
    section = re.findall(section_pat, contents, re.MULTILINE|re.DOTALL)
    subsection_pat = '^(\/\*\*\*\*\*\-\-\-\-\-\-\-\-\-\- \d+\.\d+)'
    subsection = re.findall(subsection_pat, contents, re.MULTILINE|re.DOTALL)

    if section and subsection:
        subsubsection_pat = '^(\/\*\*\-\-\-\-\-\-\-\-\-\-\-\-\- \d+\.\d+\.\d+)'
        subsubsection = re.findall(subsubsection_pat, contents, re.MULTILINE|re.DOTALL)

        if subsubsection:
            section_no = int(re.findall('(\d+)',section[len(section)-1])[0])
            subsection_no = int(re.findall('(\d+)\.(\d+)',subsection[len(subsection)-1],re.DOTALL)[0][1])
            print(section_no)
            print(subsection_no)
            subsubsection_nu = re.findall('(\d+)\.(\d+)\.(\d+)',subsubsection[len(subsubsection)-1],re.DOTALL)[0]
            print(subsubsection_nu)
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

        return '/**------------- '+ str(section_no) +'.'+ str(subsection_no) +'.'+ str(subsubsection_no) +' '+ text +' -------------**/\n'
    else:
        return '/*Please insert section and subsection first.*/\n'


def work_get_toc(contents):

    section_pat = r'^(\/\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*.+)$'
    subsection_pat = r'^(\/\*\*\*\*\*\-\-\-\-\-\-\-\-\-\-.+)$'
    subsubsection_pat = r'^(\/\*\*\-\-\-\-\-\-\-\-\-\-\-\-\-.+)$'

    all_sections = re.findall(section_pat, contents, re.MULTILINE)
    all_subsections = re.findall(subsection_pat, contents, re.MULTILINE)
    all_subsubsections = re.findall(subsubsection_pat, contents, re.MULTILINE)

    sections = []
    subsections = []
    subsubsections = []

    for section in all_sections:
        section_clean_front = section.replace('/*************** ', '')
        section_clean_back = section_clean_front.replace(' ***************/', '')
        sections.append(section_clean_back)

    for subsection in all_subsections:
        subsection_clean_front = subsection.replace('/*****---------- ', '')
        subsection_clean_back = subsection_clean_front.replace(' ----------*****/', '')
        subsections.append(subsection_clean_back)

    for subsubsection in all_subsubsections:
        subsubsection_clean_front = subsubsection.replace('/**------------- ', '')
        subsubsection_clean_back = subsubsection_clean_front.replace(' -------------**/', '')
        subsubsections.append(subsubsection_clean_back)

    sorted_list = list(heapq.merge(sections, subsections, subsubsections))

    toc = ''

    for tocitem in sorted_list:

        if re.match('(\d+)\.(\d+)\.(\d+)', tocitem):
            toc += '\t\t' + tocitem + '\n'
        elif re.match('(\d+)\.(\d+)', tocitem):
            toc += '\t' + tocitem + '\n'
        else:
            toc += tocitem + '\n'

    return '/*\n\n[Table of Contents]\n\n' + toc + '\n*/\n\n'
