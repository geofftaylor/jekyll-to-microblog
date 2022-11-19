# Jekyll to Micro.blog

These scripts will help you migrate a [Jekyll](https://jekyllrb.com) blog to [Micro.blog](https://micro.blog).


1. `feed-all.json` generates a JSON feed of your site.
2. `json-to-md.py` converts the HTML in the JSON file to Markdown files that can be imported by Micro.blog.
3. `check-links.py` checks for bad links in the converted Markdown files.

## Requirements

1. [Python 3](https://www.python.org) (tested on Python 3.9)
2. [Pandoc](https://pandoc.org)
3. [pypandoc](https://pypi.org/project/pypandoc/)
4. [Requests](https://requests.readthedocs.io/en/latest/) (optional; see [Check for bad links](https://github.com/geofftaylor/jekyll-to-microblog#check-for-bad-links-optional) below)

## Instructions

### Setup

1. Clone this repository or download the individual files.
2. Install [Python 3](https://www.python.org).
3. Install [Pandoc](https://pandoc.org).
4. Open your preferred terminal app.
4. `pip install pypandoc`
5. `pip install requests` (optional; see [Check for bad links](https://github.com/geofftaylor/jekyll-to-microblog#check-for-bad-links-optional) below)

### Generate the JSON feed

1. Copy `feed-all.json` to the root of your Jekyll site.
2. Build your site.

### Set variables in `json-to-md.py`

1. `json_file = '/<Jekyll root>/_site/feed-all.json'`: Change `<Jekyll root>` to the root of your Jekyll directory.
2. `output_dir = '/<Jekyll root>/_ToMicroBlog'`: Change `<Jekyll root>` to the root of your Jekyll directory.
3. `static_asset_paths = ['/images/']`: Add paths to static assets (e.g., images). Make sure you include leading and trailing slashes.

### Convert JSON to Markdown

1. `cd` to the directory that contains `json-to-md.py`.
2. Type `./json-to-md.py` and press Enter.

### Clean up the Markdown files

All files will be output in `/<Jekyll root>/_ToMicroBlog`.

Review **posts-with-code.txt**, **posts-with-youtube.txt** and **posts-with-img.txt**. Clean up anything that didn't convert cleanly.
For `<img>` tags, remove any `srcset` attributes (or manually upload the image files and fix the URLs after importing to Micro.blog).
For YouTube embeds, **posts-with-youtube.txt** will list the YouTube IDs in each post. Add `{{< youtube ID >}}` to the Markdown file (replace "ID" with the ID in the file). This is Hugo shortcode for a YouTube embed. Micro.blog will translate this to the embedded video.

### Check for bad links (optional)

`check-links.py` can check for bad links in your converted Markdown files. If you want to check the links, make sure you installed Requests in Setup step 5. Then type `./check-links.py` and press Enter. The script will produce a file called **bad-links.txt** that lists the bad links in each Markdown file. A link is considered "bad" if it doesn't return HTTP 200 (OK).

### Import to Micro.blog

Zip your Markdown files and [import the zip file to Micro.blog](https://help.micro.blog/t/markdown-import/56).