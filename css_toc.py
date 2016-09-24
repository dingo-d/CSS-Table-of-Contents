import sublime
import sublime_plugin

import math
from .css_toc_definitions import *

# Section creation command
class CsstocCreateSectionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		pos = self.view.sel()[0].begin() # Cursors position
		contents = self.view.substr(sublime.Region(0, pos)) # Contents of the file up to the position of the cursor
		region = self.view.line(self.view.sel()[0]) # Cursor region
		selected = self.view.substr(sublime.Region(self.view.sel()[0].begin(), self.view.sel()[0].end())) # Selected text
		line = self.view.substr(self.view.line(self.view.sel()[0])) # Returns the line contents of the cursor

		text = get_section(contents, selected, line)
		self.view.replace(edit, region, text)

		# Select only text
		text_region = self.view.find('([^\d\W]+)', region.begin())

		self.view.sel().clear()
		self.view.sel().add(text_region)
		self.view.show_at_center(text_region)


# Subsection creation command
class CsstocCreateSubsectionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		pos = self.view.sel()[0].begin() # Cursors position
		contents = self.view.substr(sublime.Region(0, pos)) # Contents of the file up to the position of the cursor
		region = self.view.line(self.view.sel()[0]) # Cursor region
		selected = self.view.substr(sublime.Region(self.view.sel()[0].begin(), self.view.sel()[0].end())) # Selected text
		line = self.view.substr(self.view.line(self.view.sel()[0])) # Returns the line contents of the cursor

		text = get_subsection(contents, selected, line)
		self.view.replace(edit, region, text)

		# Select only text
		text_region = self.view.find('([^\d\W]+)', region.begin())

		self.view.sel().clear()
		self.view.sel().add(text_region)
		self.view.show_at_center(text_region)


# Subsubsection creation command
class CsstocCreateSubsubsectionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		pos = self.view.sel()[0].begin() # Cursors position
		contents = self.view.substr(sublime.Region(0, pos)) # Contents of the file up to the position of the cursor
		region = self.view.line(self.view.sel()[0]) # Cursor region
		selected = self.view.substr(sublime.Region(self.view.sel()[0].begin(), self.view.sel()[0].end())) # Selected text
		line = self.view.substr(self.view.line(self.view.sel()[0])) # Returns the line contents of the cursor

		text = get_subsubsection(contents, selected, line)
		self.view.replace(edit, region, text)

		# Select only text
		text_region = self.view.find('([^\d\W]+)', region.begin())

		self.view.sel().clear()
		self.view.sel().add(text_region)
		self.view.show_at_center(text_region)


# Create Table of content command
class CsstocCreateTocCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		contents = self.view.substr(sublime.Region(0, self.view.size())) # Contents of the file
		existing_toc_pat = '^(\/\*[\s\w\n\d\[\].]+\*\/)' # Pattern for the existing TOC
		toc_exists = re.findall(existing_toc_pat, contents, re.MULTILINE) # Search of the exisitng TOC
		toc_region = self.view.find(existing_toc_pat, 0) # Region of the existing TOC

		toc = get_toc(contents)

		if not toc_exists:
			self.view.insert(edit, 0, toc)
		else:
			self.view.replace(edit, toc_region, '')
			self.view.insert(edit, toc_region.begin(), toc)
