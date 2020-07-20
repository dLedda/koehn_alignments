# koehn_alignments
Visualisation of the results of the alignment algorithm in Philipp Koehn's SMT book.

## Usage 

Put the alignments, tokenised e sentences, and tokenised f sentences into the files align, e, and f, respectively (or choose your own names and enter these into the command line.)
There are examples of the format required included.

By default, each sentence is read, the alignment is printed to console on a grid, and each phrase is printed onto a grid with the alignment displayed with dots in each cell, then the phrase is printed as text below. 

```
usage: alignments.py [-h] [-r RENDER_TYPE] [-s] [-e E_FILE] [-f F_FILE] [-a ALIGN_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -r RENDER_TYPE, --render_type RENDER_TYPE
                        How to render the phrases. Choose from 'text', 'image', or 'both'. Default: 'both'
  -s, --hide_alignment  Turn off the initial render of the alignment.
  -e E_FILE, --e_file E_FILE
                        Location of the file containing the translated sentences, separated by newlines. Default: './e'
  -f F_FILE, --f_file F_FILE
                        Location of the file containing the foreign sentences, separated by newlines. Default: './f'
  -a ALIGN_FILE, --align_file ALIGN_FILE
                        Location of the file containing translated sentences, separated by newlines. Default: './align'
```

Sample output:

```
           m                                                                  
           i                                                              b   
           c             d                                                l   
           h      g      a                    d                    h      e   
           a      e      v      a             a                    a      i   
           e      h      o      u             s      e      i      u      b   
           l      t      n      s      ,      s      r      m      s      t   
        ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░       
michael ░░   ░░       ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░       
        ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░       
               ███████████████████████████████████       ░░░░░░░       ░░░░░░░
assumes        ██   ████   ████   ████████████████       ░░░░░░░       ░░░░░░░
               ███████████████████████████████████       ░░░░░░░       ░░░░░░░
        ░░░░░░░███████████████████████████████████░░░░░░░       ░░░░░░░       
   that ░░░░░░░██████████████████████████████   ██░░░░░░░       ░░░░░░░       
        ░░░░░░░███████████████████████████████████░░░░░░░       ░░░░░░░       
               ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░
     he        ░░░░░░░       ░░░░░░░       ░░░░░░░  ░░░  ░░░░░░░       ░░░░░░░
               ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░
        ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░       
   will ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░  ░░░  
        ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░       
               ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░
   stay        ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░   ░░
               ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░
        ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░       
     in ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░  ░░░  ░░░░░░░       
        ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░       
               ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░
    the        ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░   ░░       ░░░░░░░
               ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░
        ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░       
  house ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░   ░░       
        ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░       ░░░░░░░       
E:  assumes that
F:  geht davon aus , dass
```