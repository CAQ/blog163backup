Backup 163.com blog articles:
- Download the main content HTML source
- Extract meta info: Title, post time, category, tags
- Extract main content: Text, image links
- Download the images

To use it, you need to manually edit the 
  articles.txt
, pasting all the blog article links into it, one link per line.

Then run 
  python fetcharticles.py

(You can edit the last four lines to control which steps to run.)

Output:
- HTML sources: in data/
- meta info: meta.txt
- main content: txt/
- images: img/
