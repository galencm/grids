# Grids

## Usage

**create a grid:**

```
grids 1.jpg 2.jpg 3.jpg animated.gif foo.txt
```

or

```
gg 1.jpg 2.jpg 3.jpg animated.gif foo.txt
```

**store grid visual-state on db (for machinic):**

```
gg *.jpg --use-db
```

**on grids**

Grids consist of two files, they are stored in $XDG_DATA_HOME/grids and are named with with the _grid hash_ and their extension.
* The _grid hash_ is an sha1 hash of the string of the list of files in the grid sorted and then concatenated
* _grid hash_.xml: xml file containing grid contents and state
* _grid hash_.png: a fullsized image of the current visual state of the grid. Use when nesting grids or store in a database for use with machinic programs.  

**load some grids** (location depends on $XDG_DATA_HOME):

```
cd ~/.local/share/grids
grids *.xml
```

## Installation

Pip:
```
pip3 install git+https://github.com/galencm/grids --user
```

Clone / download:
```
git clone https://github.com/galencm/grids
```

Develop while using pip:
```
git clone https://github.com/galencm/grids
cd grids
pip3 install --editable ./ --user
```

Setup Linting and Formatting git hooks
```
cd grids
pre-commit install
pre-commit install -t commit-msg
```

## Contributing

[Contribution guidelines](CONTRIBUTING.md)

## License
Mozilla Public License, v. 2.0

[http://mozilla.org/MPL/2.0/](http://mozilla.org/MPL/2.0/)