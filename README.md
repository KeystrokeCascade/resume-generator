# Resume Generator
A template because it was annoying to manually keep my resume up-to-date across my website and pdf copy.

Using Jinja2 in Python it reads a YAML file containing resume details, and then outputs those details to a folder specified in constant variables at the top of the script.  By default this is in `../<website>/index.html` and `../<website>/pdf/index.pdf`.

The template is very flexible, as it allows for multiple identities with various names and emails for the same resume.  Each section is iterated over allowing for any amount of sections and any amount of positions/experience within those sections.

Copy `resume.yaml.sample` into `resume.yaml` if you want to use a template.
