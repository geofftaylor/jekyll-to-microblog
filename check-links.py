#! /usr/bin/env python3

import sys, os, re, requests

def main():
    # Directory containing Markdown files. This is `output_dir` from json-to-md.py.
    micro_dir = '/output/dir'
    bad_links_file = 'bad-links.txt'

    bad_links = {}

    # Regex to find URLs.
    url_pattern = re.compile(r'(https?:\/\/\w*\.?\w+\.\w+\/?[\w\@\=\?\&\/\%\-\.]*)')

    for md in [f for f in os.listdir(micro_dir) if f.endswith('.md')]:
        # Iterate over all Markdown files.
        print('Reading %s' % md)
        file_path = os.path.join(micro_dir, md)

        with open(file_path, 'r') as f:
            # Get the file contents as a string.
            contents = f.read()

        # Find any URLs.
        urls = url_pattern.findall(contents)

        for u in urls:
            print('Checking %s' % u)

            try:
                # GET the URL.
                r = requests.get(u)
                resp_status = r.status_code
            except:
                # If there's an exception, set `resp_status` to 999, which isn't a valid HTTP response code.
                resp_status = 999

            if resp_status != 200:
                if md not in bad_links.keys():
                    bad_links[md] = []

                if resp_status == 999:
                    msg = '%s returned an unknown error' % u
                else:
                    msg = '%s returned %i' % (u, resp_status)
                
                bad_links[md].append(msg)

    with open(os.path.join(micro_dir, bad_links_file), 'w') as f:
        for k in bad_links.keys():
            f.write(k + '\n')

            for bad_url in bad_links[k]:
                f.write('    %s\n' % bad_url)

    print('Done')

if __name__ == '__main__':
    main()