# CSS Table of Contents

**Version**: 1.1.1

**License**: LGPL (GNU Lesser General Public License)

**License URI**: https://www.gnu.org/copyleft/lesser.html

**Contributors**: [Alexey-T](https://github.com/Alexey-T)

A [Sublime Text 3](http://www.sublimetext.com) plugin that helps you with creating
neat table of contents on the beginning of your .css file

![demo](http://i.imgur.com/RD053Tm.gif)

Add sections, subsections and sub-subsections to your .css file with ease. The plugin
keeps track of your cursor and selection when creating section markup.
You can add your desired subsections and sub-subsections after you've already add some in.
If you don't name your sections, it's done automatically.

## How to install

### Via Package Control
Open your command palette -> Package Control: Install Package -> CSS Table of Contents

### Manual

Go to your packages folder(Preferences -> Browse Packages)
```bash
# clone this repo
git clone https://github.com/dingo-d/CSS-Table-of-Contents 'CSS Table of Contents'
```
Or download the leatest [release](https://github.com/dingo-d/CSS-Table-of-Contents/releases)
and unzip it in a folder named `CSS Table of Contents`

## How to use it

You can right click on the contents of your .css file and add them from the menu
'CSS Table of Contents', from Tools > CSS Table of Contents submenu, or by using hotkeys

`ctrl+t, g` for section

`ctrl+t, h` for subsection

`ctrl+t, j` for subsubsection

`ctrl+t, t` for table of contents creation

## To do

- Navigation through the sections, subsections and sub-subsections.

- Changing the Table of contents title in the settings.

And what ever somebody suggests. Please test it and report any bugs or issues, it will be appreciated :)

## Revision History

* v 1.0.0 Initial release

* v 1.1.0 Update
  * Bugfix - If ToC already exists, when creating a new one, the old one remained.
    		 Now you can create sections after you've created a ToC, and it will be updated.
  * Bugfix - Heapq sort using lexicographical order, so the ordering was wrong. Changed the sort
  			 according to the [answer](http://stackoverflow.com/a/39675262/629127) by Kasramvd
  * Update - After creating section, the section name will be selected for
    		 easier changing of the section title (section/subsection/sub subsection), suggestion
    		 by [henriquearthur](https://github.com/henriquearthur).
  * Update - Refactored the code (PR by [Alexey-T](https://github.com/Alexey-T)), so that the definitions are in a separate file.


* v 1.1.1 Update
  * Update - Selection view added to a variable
  * Update - Added docstrings to css_toc_definitions.py file
  * Fix - Minor linter fixes