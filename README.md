# Find_Associations
Script finds associations for words at https://wordassociations.net using API.
 
## Description: 
Script send GET requests to https://wordassociations.net/ with words from input file and put results in output file.

       [-h] [-t {stimulus,response}] [-l LIMIT] [-p POS] [-i] [-x]
       input output apikey language {en,es,it,de,pt,ru,fr}

## positional arguments:
```bash
  input                 Path to input file with words.
  output                Path to output file with response.
  apikey                API-key from https://wordassociations.net/
  language              {en,es,it,de,pt,ru,fr}
                        Request words language.
```
## optional arguments:
```bash
  -h, --help            show this help message and exit
  -t {stimulus,response}, --type {stimulus,response}
                        Type of search method. stimulus - search for words
                        which make us think about input word. response -
                        search for words which associates with input word.
                        Default: stimulus.
  -l LIMIT, --limit LIMIT
                        Maximum number of results. Range: 1 to 300.
  -p POS, --pos POS     Part of speech.List: noun, adjective,verb, adverb. Can
                        be grouped.Default: noun,adjective,verb,adverb
  -i, --indent          Disables indents. Default: enabled.
  -x, --xml             Output in XML format. Default: JSON format.
```
