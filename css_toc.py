import sublime
import sublime_plugin

from .css_toc_definitions import *

""" Definition inside classes:

selection - Text selection at the cursor position.
pos - The position of the beginning of the selection.
contents - Contents of the file up to the position of the cursor.
region - The region of the selected line/text.
selected - The selected text.
line - Line contents where the cursor is.

"""

class CsstocCreateSectionCommand(sublime_plugin.TextCommand):
    """Create section command."""

    def run(self, edit):
        selection = self.view.sel()[0]
        pos = selection.begin()
        contents = self.view.substr(sublime.Region(0, pos))
        region = self.view.line(selection)
        selected = self.view.substr(sublime.Region(pos, selection.end()))
        line = self.view.substr(self.view.line(selection))

        text = get_section(contents, selected, line)
        self.view.replace(edit, region, text)

        # Select only text
        text_region = self.view.find(r'([^\d\W]+)', region.begin())

        self.view.sel().clear()
        self.view.sel().add(text_region)
        self.view.show_at_center(text_region)


class CsstocCreateSubsectionCommand(sublime_plugin.TextCommand):
    """Create sub section command."""

    def run(self, edit):
        selection = self.view.sel()[0]
        pos = selection.begin()
        contents = self.view.substr(sublime.Region(0, pos))
        region = self.view.line(selection)
        selected = self.view.substr(sublime.Region(pos, selection.end()))
        line = self.view.substr(self.view.line(selection))

        text = get_subsection(contents, selected, line)
        self.view.replace(edit, region, text)

        # Select only text
        text_region = self.view.find(r'([^\d\W]+)', region.begin())

        self.view.sel().clear()
        self.view.sel().add(text_region)
        self.view.show_at_center(text_region)


class CsstocCreateSubsubsectionCommand(sublime_plugin.TextCommand):
    """Create sub sub section command."""

    def run(self, edit):
        selection = self.view.sel()[0]
        pos = selection.begin()
        contents = self.view.substr(sublime.Region(0, pos))
        region = self.view.line(selection)
        selected = self.view.substr(sublime.Region(pos, selection.end()))
        line = self.view.substr(self.view.line(selection))

        text = get_subsubsection(contents, selected, line)
        self.view.replace(edit, region, text)

        # Select only text
        text_region = self.view.find(r'([^\d\W]+)', region.begin())

        self.view.sel().clear()
        self.view.sel().add(text_region)
        self.view.show_at_center(text_region)


class CsstocCreateTocCommand(sublime_plugin.TextCommand):
    """Create table of contents command."""

    def run(self, edit):
        contents = self.view.substr(sublime.Region(0, self.view.size())) # Contents of the file
        existing_toc_pat = r'^(\/\*[\s\w\n\d\[\].]+\*\/)' # Pattern for the existing TOC
        toc_exists = re.findall(existing_toc_pat, contents, re.MULTILINE) # Search of the exisitng TOC
        toc_region = self.view.find(existing_toc_pat, 0) # Region of the existing TOC

        toc = get_toc(contents)

        if not toc_exists:
            self.view.insert(edit, 0, toc)
        else:
            self.view.replace(edit, toc_region, '')
            self.view.insert(edit, toc_region.begin(), toc)
