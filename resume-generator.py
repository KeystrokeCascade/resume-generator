import yaml
import jinja2
import os
import shutil
import datetime
import subprocess

# Constants
RESUME = 'resume.yaml'
OUTPUT_DIR = 'public'
HTML_TEMPLATE = 'index.html'
LATEX_TEMPLATE = 'index.tex'
LATEX_SUBDIR = 'pdf'
DATE = datetime.datetime.now().year

def load_env():
	# Set location and create environment
	env = jinja2.Environment(
		loader=jinja2.FileSystemLoader('templates'),
		trim_blocks = True,
		lstrip_blocks = True
	)
	return env

def render_env(env, template, resume):
	render = env.get_template(template).render(
		name = resume['name'],
		email = resume['email'],
		address = resume['address'],
		phone = resume['phone'],
		summary = resume['summary'].split('\n\n'),
		skills = resume['skills'],
		experiences = resume['experiences'],
		referees = resume['referees'],
		date = DATE
	)
	return render

# HTML generation
def html_doc(resume):
	env = load_env()
	template = HTML_TEMPLATE
	doc = render_env(env, template, resume)
	return doc

# LaTeX generation
def latex_doc(resume):
	env = load_env()
	# LaTeX-specific environment changes
	env.block_start_string = '\\BLOCK{'
	env.block_end_string = '}'
	env.variable_start_string = '\\VAR{'
	env.variable_end_string = '}'
	env.comment_start_string = '\\#{'
	env.comment_end_string = '}'
	env.line_statement_prefix = '%%'
	env.line_comment_prefix = '%#'
	env.autoescape = False

	template = LATEX_TEMPLATE
	doc = render_env(env, template, resume)
	return doc

# Execute time
def main():
	# Load settings
	with open(RESUME, mode='r', encoding='utf8') as f:
		resume = yaml.safe_load(f)

	# Generate folders
	os.makedirs(os.path.dirname(os.path.join(OUTPUT_DIR, LATEX_SUBDIR, LATEX_TEMPLATE)), exist_ok=True)
	# Copy static files
	for file in os.listdir('static'):
		shutil.copy2(os.path.join('static', file), os.path.join(OUTPUT_DIR, file))

	# Write out
	with open(os.path.join(OUTPUT_DIR, HTML_TEMPLATE), mode='w', encoding='utf8') as f:
		f.write(html_doc(resume))
	with open(os.path.join(OUTPUT_DIR, LATEX_SUBDIR, LATEX_TEMPLATE), mode='w', encoding='utf8') as f:
		f.write(latex_doc(resume))

	# Compile LaTeX doc and delete log files if no err
	out = subprocess.run([
		'lualatex',
		'--output-directory=' + os.path.join(OUTPUT_DIR, LATEX_SUBDIR),
		os.path.join(OUTPUT_DIR, LATEX_SUBDIR, LATEX_TEMPLATE)
	])
	if not out.returncode:
		for file in os.listdir(os.path.join(OUTPUT_DIR, LATEX_SUBDIR)):
			if file.split('.')[-1] in ['aux', 'log', 'out']:
				os.remove(os.path.join(OUTPUT_DIR, LATEX_SUBDIR, file))

if __name__ == '__main__':
	main()
