import os
import json
import  xml.etree.ElementTree as ET
import argparse
import requests
from requests.exceptions import HTTPError

## API_Key = "a4251e15-9083-4de5-9755-f90ca2eba6f8"

def send_get(_API_Key, _text, _lang, _type, _limit, _pos, _indent, _xml):
    """Sends GET request to wordassociations.net with paramters. Returns response object if there is no errors."""
    assert (len(_text) > 0), "Empty text"
    indent = 'yes'
    if not _indent:
        indent = 'no'
    format = 'json'
    if _xml is True:
        format = 'xml'
    url = f"https://api.wordassociations.net/associations/v1.0/{format}/search?"
    url = url + f"apikey={_API_Key}"
    for word in _text:
        word = word.strip('\n')
        if not word:
            continue
        url = url + f'&text={word}'
    url = url + f"&lang={_lang}&type={_type}&limit={_limit}&pos={_pos}&indent={indent}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return None
    except Exception as err:
        print(f'Other error occurred: {err}')
        return None
    else:
        return response



def main():
    parser = argparse.ArgumentParser('Description: Script send GET requests to https://wordassociations.net/'
                                     ' with words from input file and put results in output file.\n')
    #positional arguments
    parser.add_argument('input', type=str, help="Path to input file with words.")
    parser.add_argument('output', type=str, help='Path to output file with response.')
    parser.add_argument('apikey', type=str, help='API-key from https://wordassociations.net/')
    parser.add_argument('language', type=str,
                        help='Request words language.', choices=['en', 'es', 'it', 'de', 'pt', 'ru', 'fr'])
    #optional arguments
    parser.add_argument('-t', '--type', type=str, choices=['stimulus', 'response'], default='stimulus',
                        help='Type of search method. '
                             'stimulus - search for words which'
                             ' make us think about input word.\n'
                             'response - search for words which '
                             'associates with input word.\n'
                             'Default: stimulus.')
    parser.add_argument('-l', '--limit', type=int, default=50, help='Maximum number of results. Range: 1 to 300.')
    parser.add_argument('-p', '--pos', type=str, default='noun,adjective,verb,adverb', help='Part of speech.'
                                                                                            'List: noun, adjective,'
                                                                                            'verb, adverb. '
                                                                                            'Can be grouped.'
                                                                                            'Default: noun,adjective,verb,adverb')
    parser.add_argument('-i', '--indent', default=True, action="store_false", help='Disables indents. '
                                                                                   'Default: enabled.')
    parser.add_argument('-x', '--xml', default=False, action="store_true", help='Output in XML format. '
                                                                                'Default: JSON format.')
    args = parser.parse_args()
    if os.path.exists(args.input) == False:
        print("Input file doesn't exists!")
        return -1
    if args.limit < 1 or args.limit > 300:
        print("Limit value should be in range from 1 to 300!")
        return -1
    poses = args.pos.split(',')
    for pos in poses:
        if pos not in ['noun', 'adjective', 'verb', 'adverb']:
            print('Wrong pos argument!')
            return -1
    #read input file words without BOM
    infile = open(args.input, 'r', encoding='utf-8-sig')
    inputlist = infile.readlines()
    infile.close()
    #create output path if not exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    outfile = open(args.output, "w", encoding='utf-16')
    #cut input words list to groups of 10 items
    groups = [inputlist[i:i + 10] for i in range(0, len(inputlist), 10)]
    for group in groups:
        #send GET request
        response = send_get(args.apikey, group, args.language, args.type, args.limit, args.pos, args.indent, args.xml)
        if response is None:
            return -2
        #if xml output needed, find all 'result' subsections
        if args.xml:
            data = response.text
            root = ET.fromstring(data)
            for item in root.iter('result'):
                outfile.writelines(ET.tostringlist(item, encoding='unicode'))
        #in json format find 'response' dictionary
        else:
            data = response.json()['response']
            json.dump(data, outfile, indent=2, ensure_ascii=False)
    outfile.close()
    return 0

main()