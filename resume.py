#!/usr/bin/python
import yaml
import jinja2
import os
import datetime
import subprocess

# Constants
DATA = 'resume.yaml'
PROGRAM_LOCATION = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
WEBSITE_LOCATION = '/srv'
HTML_TEMPLATE = 'template.html'
HTML_NAME = 'index'
LATEX_TEMPLATE = 'template.tex'
LATEX_NAME = 'index'
LATEX_SUBDIR = 'pdf'
DATE = datetime.datetime.now().year

# Get the good stuff
with open(DATA, mode='r', encoding='utf8') as f:
	resume = yaml.safe_load(f)

def loadEnv():
	# Set location and create environment
	dir = os.path.dirname(os.path.abspath(__file__))
	env = jinja2.Environment(
		loader=jinja2.FileSystemLoader(dir),
		trim_blocks = True,
		lstrip_blocks = True
	)
	return env

def renderEnv(env, template, id):
	render = env.get_template(template).render(
		name = id['name'],
		email = id['email'],
		address = resume['address'],
		phone = resume['phone'],
		summary = resume['summary'].split('\n\n'),
		experiences = resume['experiences'],
		referees = resume['referees'],
		date = DATE
	)
	return render

# HTML generation
def htmlDoc(id):
	env = loadEnv()
	template = HTML_TEMPLATE
	doc = renderEnv(env, template, id)

	return doc

# LaTeX generation
def latexDoc(id):
	env = loadEnv()

	# LaTeX-specific environment changes
	env.block_start_string = '\BLOCK{'
	env.block_end_string = '}'
	env.variable_start_string = '\VAR{'
	env.variable_end_string = '}'
	env.comment_start_string = '\#{'
	env.comment_end_string = '}'
	env.line_statement_prefix = '%%'
	env.line_comment_prefix = '%#'
	env.autoescape = False

	template = LATEX_TEMPLATE
	doc = renderEnv(env, template, id)

	return doc

# Generate website structure including symbolic links
def genStructure(website, path):
	# Generate folders
	if not os.path.exists(os.path.join(path, LATEX_SUBDIR)):
		os.makedirs(os.path.join(path, LATEX_SUBDIR))
	# Generate internal symlinks
	for file in os.listdir(os.path.join(PROGRAM_LOCATION, 'data')):
		if not os.path.exists(os.path.join(PROGRAM_LOCATION, 'data', file)):
			os.symlink(os.path.join(PROGRAM_LOCATION, 'data', file), os.path.join(path, file))
	# Generate symlink from website location to here
	if not os.path.exists(os.path.join(WEBSITE_LOCATION, website)):
		os.symlink(path, os.path.join(WEBSITE_LOCATION, website))

# Write out to file
def write(doc, filename):
	with open(filename, mode='w', encoding='utf8') as f:
		f.write(doc)

# Execute time
for id in resume['ids']:
	website = id['email'].split('@')[1]  # Website from email
	path = os.path.join(PROGRAM_LOCATION, website)
	genStructure(website, path)
	write(htmlDoc(id), os.path.join(path, HTML_NAME + '.html'))
	write(latexDoc(id), os.path.join(path, LATEX_SUBDIR,  LATEX_NAME + '.tex'))
	# Compile LaTeX doc and delete log files if no err
	out = subprocess.run(['lualatex',
		'--output-directory=' + os.path.join(path, LATEX_SUBDIR),
		 os.path.join(path, LATEX_SUBDIR, LATEX_NAME + '.tex')])
	if not out.returncode:
		os.remove(os.path.join(path, LATEX_SUBDIR, LATEX_NAME + '.aux'))
		os.remove(os.path.join(path, LATEX_SUBDIR, LATEX_NAME + '.log'))
		os.remove(os.path.join(path, LATEX_SUBDIR, LATEX_NAME + '.out'))
