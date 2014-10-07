#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
from itertools import islice
import json
import re
import os

FONT_DIRECTORY_GH_PAGES = '//fontdirectory.github.io'


def get_gitmodules(source_file, exclude_filters=()):
    with open(source_file) as f:
        while True:
            next_n_lines = list(islice(f, 3))
            if not next_n_lines:
                break
            submodule_pattern = r'"*/(?P<submodule>[\w_\./\\-]*)"'
            url_pattern = r'=\s{0,}(?P<url>[\w_\.\:\@\//\\-]*)'
            path_pattern = r'=\s{0,}(?P<path>[\w_\./\\-]*)'
            submodule = re.search(submodule_pattern, next_n_lines[0]).group('submodule')
            path = re.search(path_pattern, next_n_lines[1]).group('path')
            url = re.search(url_pattern, next_n_lines[2]).group('url')
            gh_page = os.path.join(FONT_DIRECTORY_GH_PAGES, submodule)
            item = dict(submodule=submodule, path=path, url=url, gh_page=gh_page)
            if not exclude_filters:
                yield item
            elif exclude_filters:
                if any([_filter(item) for _filter in exclude_filters]):
                    continue
                else:
                    yield item


if __name__ == '__main__':
    in_file_default = '.gitmodules'
    out_file_default = 'gitmodules.json'

    def is_valid_file(parser, arg):
        if not os.path.exists(arg):
            parser.error('The file "{}" does not exist! Please provide '
                         'path to {} file'.format(arg, in_file_default))
        return arg

    parser = argparse.ArgumentParser()
    parser.add_argument('--jsonp', dest='tojsonp', action='store_true')
    parser.add_argument('-i', dest='infile', required=False,
                        help='Path to .gitmodules file.'
                             'Defaults to "{}"'.format(in_file_default),
                        metavar='IN_FILE',
                        type=lambda x: is_valid_file(parser, x))
    parser.add_argument('-o', dest='outfile', required=False,
                        help='File to write data into. '
                             'Defaults to "{}"'.format(out_file_default),
                        metavar='OUT_FILE',
                        type=str)
    parser.set_defaults(tojsonp=False)
    args = parser.parse_args()
    in_file = args.infile if args.infile else in_file_default
    out_file = args.outfile if args.outfile else out_file_default
    # exclude 'tools'
    filter1 = lambda x: True if x['path'].startswith('tools') else False
    gitmodules = list(get_gitmodules(in_file, exclude_filters=(filter1, )))
    if args.tojsonp:
        with open(out_file, 'w') as f:
            lst = json.dumps(gitmodules, f, indent=2)
            f.write('jsonCallback({})'.format(lst))
    else:
        with open(out_file, 'w') as f:
            json.dump(gitmodules, f, indent=2)
