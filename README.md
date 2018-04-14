# Markdown2Revealjs
- Transfor markdown to revealjs
## Usage
- `index.md` is the default markdown filename.
- `python md2reveal.py path/to/your/log/folder`
- Please refer to the  `demo` for more details
## Rules
- use `!page!` to split each page
- insert images to markdown: put images into subfolder `/imgs`
  1. if there is no need to rescale the image, use `![imgname](imgpath)`
  2. use `<img src="imgs/sobel.png" style="zoom:100%" align=center/>` if you need to rescale the image.