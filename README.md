# Grids

## Usage

```
grids 1.jpg 2.jpg 3.jpg animated.gif
```

or

```
gg 1.jpg 2.jpg 3.jpg animated.gif
```

Grids consist of two files, they are stored in $XDG_DATA_HOME/grids and are named with with the grid hash and their extension.
* The grid hash is an sha1 hash of the string of the list of files in the grid sorted and then concatenated
* _grid hash_.xml: xml file containing grid contents and state
* _grid hash_.png: a fullsized image of the current visual state of the grid. Use when nesting grids or store in a database for use with machinic programs.  

loading some grids (location depends on $XDG_DATA_HOME):

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

## Contributing
This project uses the C4 process

[https://rfc.zeromq.org/spec:42/C4/](https://rfc.zeromq.org/spec:42/C4/
)

## License
Mozilla Public License, v. 2.0

[http://mozilla.org/MPL/2.0/](http://mozilla.org/MPL/2.0/)