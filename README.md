# Resume Generator
A template to automatically generate a website and PDF version of a resume to keep details in sync from the same YAML file.

The template allows for each section of the resume to be iterated over allowing for any amount of sections and any amount of positions/experience within those sections.

---

You must have LuaLaTeX installed on your system to run this script.  I also use the `parskip` and `ebgaramond` LaTeX packages.

To get started, copy `resume.yaml.sample` into `resume.yaml` if you want to use a template.

```
cp resume.yaml.sample resume.yaml
```

To run, use uv

```
uv run resume-generator.py
```

Outputs to `public` directory in working folder.
