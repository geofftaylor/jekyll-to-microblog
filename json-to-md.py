#!/usr/bin/env python3

import os, json, pypandoc, re
from datetime import datetime
from urllib.parse import urlparse

def main():
    # Replace <Jekyll root> with the path to your Jekyll site.
    json_file = '/<Jekyll root>/_site/feed-all.json'

    # Replace <Jekyll root> with the path to your Jekyll site.
    output_dir = '/<Jekyll root>/_ToMicroBlog'

    # Replace with your domain.
    full_domain = 'https://www.example.me'
    
    # Add any paths that contain static files, e.g, for https://www.example.com/images/, add '/images/'.
    # The leading and trailing slashes are required.
    static_asset_paths = ['/images/']

    # Output files.
    posts_with_code_file = os.path.join(output_dir, 'posts-with-code.txt')
    posts_with_youtube_file = os.path.join(output_dir, 'posts-with-youtube.txt')
    posts_with_img_file = os.path.join(output_dir, 'posts-with-img.txt')

    posts_with_code = []
    posts_with_youtube = []
    posts_with_img = []

    # Regex to find YouTube embeds.
    youtube_pattern = re.compile(r'youtube\.com\/embed\/(\w+)"')

    # Deserialize the JSON file into a Python dictionary.
    with open(json_file, 'r') as jf:
      data = json.load(jf)

    # The posts are in a list under the "items" key.
    posts = data['items']

    posts_converted = 0

    for p in posts:
        # The post front matter needed by Micro.blog.
        # See https://help.micro.blog/t/markdown-import/56 for all front matter fields accepted by Micro.blog.

        post_title = p['title']
        post_url = p['url']

        # Convert date_published to a datetime object and format it as YYYY-MM-DD HH:MM:SS Z.
        dt = datetime.strptime(p['date_published'], '%Y-%m-%dT%H:%M:%S%z')
        post_date = datetime.strftime(dt, '%Y-%m-%d %H:%M:%S %z')

        # Convert the HTML to GitHub Flavored Markdown.
        # Micro.blog will only import the image file inside of the "src" attribute. If the <img> tag contains other attributes like "srcset," Micro.blog ignores those.
        # GitHub Flavored Markdown doesn't convert <img> tags that contain attributes other than "src" and "alt," so we can easily identify <img> tags that contain extra attributes.
        md = pypandoc.convert_text(p['content_html'], 'gfm', format='html')
        
        # Append the full domain to all static asset paths.
        for sp in static_asset_paths:
            md = md.replace(sp, full_domain + sp)

        # Construct the output file name.
        # Get the path from the URL, remove leading and trailing slashes, replace interior slashes with hyphens, and append '.md'.
        output_filename = urlparse(post_url).path.strip('/').replace('/', '-') + '.md'
        output_file_path = os.path.join(output_dir, output_filename)

        # Does the Markdown contain an <img> tag?
        if '<img' in md:
            posts_with_img.append(output_filename)

        # Does this post contain code?
        if '</code>' in p['content_html']:
            posts_with_code.append(output_filename)

        # Does this post contain a Youtube embed?
        yt_matches = youtube_pattern.search(p['content_html'])

        if yt_matches:
            yt_id = yt_matches.groups()[0]

            posts_with_youtube.append({'filename': output_filename, 'youtube_id': yt_id})

        # Write the front matter and the Markdown content to the output file.
        with open(output_file_path, 'w') as outfile:
            outfile.write('---\n')
            outfile.write('title: ' + post_title + '\n')
            outfile.write('date: ' + post_date + '\n')
            outfile.write('url: ' + post_url + '\n')
            outfile.write('---\n')
            outfile.write(md + '\n')

        posts_converted += 1

    # Log posts that contain <img> tags.
    if len(posts_with_img) > 0:
        with open(posts_with_img_file, 'w') as imgf:
            for p in posts_with_img:
                imgf.write(p + '\n')
    
    # Log posts that contain code.
    if len(posts_with_code) > 0:
        with open(posts_with_code_file, 'w') as cf:
            for p in posts_with_code:
                cf.write(p + '\n')

    # Log posts that contain Youtube embeds.
    if len(posts_with_youtube) > 0:
        with open(posts_with_youtube_file, 'w') as yf:
            for p in posts_with_youtube:
                yf.write('%s: %s\n' % (p['filename'], p['youtube_id']))

    print('%i posts to be converted' % len(posts))
    print('%i posts converted' % posts_converted)
    print('%i posts contain <img> tags' % len(posts_with_img))
    print('%i posts contain code' % len(posts_with_code))
    print('%i posts contain Youtube embeds' % len(posts_with_youtube))

if __name__ == '__main__':
    main()