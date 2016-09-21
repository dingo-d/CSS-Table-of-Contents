import sublime
import sublime_plugin
import math
from .css_toc_work import *

# Section creation command
class CsstocCreateSectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        pos = self.view.sel()[0].begin() # Cursors position
        contents = self.view.substr(sublime.Region(0, pos)) # Contents of the file up to the position of the cursor
        region = self.view.line(self.view.sel()[0]) # Cursor region
        selected = self.view.substr(sublime.Region(self.view.sel()[0].begin(), self.view.sel()[0].end())) # Selected text
        line = self.view.substr(self.view.line(self.view.sel()[0])) # Returns the line contents of the cursor

        text = work_get_section(contents, selected, line)
        self.view.replace(edit, region, text)


# Subsection creation command
class CsstocCreateSubsectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        pos = self.view.sel()[0].begin() # Cursors position
        contents = self.view.substr(sublime.Region(0, pos)) # Contents of the file up to the position of the cursor
        region = self.view.line(self.view.sel()[0]) # Cursor region
        selected = self.view.substr(sublime.Region(self.view.sel()[0].begin(), self.view.sel()[0].end())) # Selected text
        line = self.view.substr(self.view.line(self.view.sel()[0])) # Returns the line contents of the cursor

        text = work_get_subsection(contents, selected, line)
        self.view.replace(edit, region, text)


# Subsubsection creation command
class CsstocCreateSubsubsectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        pos = self.view.sel()[0].begin() # Cursors position
        contents = self.view.substr(sublime.Region(0, pos)) # Contents of the file up to the position of the cursor
        region = self.view.line(self.view.sel()[0]) # Cursor region
        selected = self.view.substr(sublime.Region(self.view.sel()[0].begin(), self.view.sel()[0].end())) # Selected text
        line = self.view.substr(self.view.line(self.view.sel()[0])) # Returns the line contents of the cursor

        text = work_get_subsubsection(contents, selected, line)
        self.view.replace(edit, region, text)


# Create Table of content command
class CsstocCreateTocCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        contents = self.view.substr(sublime.Region(0, self.view.size()))

        text = work_get_toc(contents)
        self.view.insert(edit, 0, text)
