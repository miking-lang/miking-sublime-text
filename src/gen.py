#!/usr/bin/python3

import argparse
import regex
import os
import shutil
import sys
import tempfile

p_templatefname = regex.compile(r"(?P<filename>(?P<name>\w+)[.]sublime-syntax-base)")
p_import = regex.compile(r"(?P<full>#%%IMPORT=(?P<fragment>[-a-zA-Z.]+)[(]\s*(?:(?P<args>(?:[-a-zA-Z]+[=])?\"[^\"]*\")\s*(?:[,]\s*(?P<args>(?:[-a-zA-Z]+[=])?\"[^\"]*\")\s*)*)?[)])")
p_args = regex.compile(r"(?P<full>#%%ARGS=[(](?:(?P<args>[-a-zA-Z]+(?:[=]\"[^\"]*\")?)(?:[,](?P<args>[-a-zA-Z]+(?:[=]\"[^\"]*\")?))*)?[)])")
p_usearg = regex.compile(r"(?P<full>(#|%)%%USEARG=(?P<name>[-a-zA-Z]+))")

def main(args):
	cwd = os.path.dirname(os.path.realpath(__file__))

	dstdir = args.dstdir
	if dstdir is None:
		dstdir = cwd
	try:
		os.listdir(dstdir)
	except FileNotFoundError:
		print("Error: Could not find target directory \"%s\"" % dstdir)
		sys.exit(1)

	lang = args.lang[0]
	langdir = os.path.join(cwd, lang)
	try:
		files = os.listdir(langdir)
	except FileNotFoundError:
		print("Error: No such language \"%s\"" % lang)
		sys.exit(1)

	templates = [m for m in [p_templatefname.match(f) for f in files] if m is not None]
	for tmatch in templates:
		filename = tmatch.group("filename")
		name = tmatch.group("name")
		targetpath = os.path.join(dstdir, name + ".sublime-syntax")
		with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmpfile:
			scan_template(tmpfile, langdir, filename)

		shutil.move(tmpfile.name, targetpath)
		shutil.copystat(os.path.join(langdir, filename), targetpath)

# Scan a *.sublime-syntax-base file
def scan_template(outfile, langdir, filename):
	filepath = os.path.join(langdir, filename)

	with open(filepath, "r") as f:
		for line in f.readlines():
			m = p_import.match(line.strip())
			if m is not None:
				indent = line.find(m.group("full"))
				fragfilename = m.group("fragment") + ".fragment"
				frag_args = []
				frag_kwargs = dict()
				for fragarg in m.captures("args"):
					eqidx = fragarg.find("=")
					if eqidx >= 0:
						key = fragarg[:eqidx]
						value = fragarg[eqidx+1:].replace("\"", "")
						frag_kwargs[key] = value
					else:
						frag_args.append(fragarg.replace("\"", ""))

				scan_fragment(outfile, langdir, fragfilename, frag_args, frag_kwargs, [fragfilename], indent)
			else:
				outfile.write(line)

# Scan a *.fragment file
def scan_fragment(outfile, langdir, filename, args=[], kwargs=dict(), scanned=[], indent=0):
	filepath = os.path.join(langdir, filename)

	with open(filepath, "r") as f:
		i = -1
		argconv = dict()
		for line in f.readlines():
			i += 1
			if line[-1] == "\n":
				line = line[:-1]

			def fragerror(msg):
				print("Error in \"%s\" on line %d: %s" % (filename, i, msg))
				sys.exit(1)

			if i == 0:
				if line != "%YAML 1.2":
					fragerror("First line is not the YAML version")
			elif i == 1:
				m = p_args.match(line.strip())
				if m is None:
					fragerror("Second line does not specify fragment arguments")

				if len(args) > len(m.captures("args")):
					fragerror("Too many arguments provided")

				ordered_keys = []
				for argdef in m.captures("args"):
					eqidx = argdef.find("=")
					if eqidx >= 0:
						key = argdef[:eqidx]
						default = argdef[eqidx+1:].replace("\"", "")
					else:
						key = argdef
						default = None
					argconv[key] = default
					ordered_keys.append(key)

				for key,value in zip(ordered_keys[:len(args)], args):
					argconv[key] = value

				for key,value in kwargs.items():
					if key not in argconv:
						fragerror(f"Unknown argument provided \"{key}\"")
					else:
						argconv[key] = value

				for key,value in argconv.items():
					if value is None:
						fragerror(f"No value provided for argument \"{key}\"")

			else:
				lineparts = []
				m = p_usearg.search(line)
				while m is not None:
					argname = m.group("name")
					if argname not in argconv:
						fragerror("Could not find argument")
					
					i = m.span("name")[1]
					pre_m = line[:i]
					line = line[i:]
					lineparts.append(pre_m.replace(m.group("full"), argconv[argname], 1))
					m = p_usearg.search(line)

				lineparts.append(line)
				line = "".join(lineparts)

				# Check if replaced line is an import statement
				m = p_import.match(line.strip())
				if m is not None:
					imp_indent = line.find(m.group("full"))
					imp_name = m.group("fragment") + ".fragment"
					imp_args = []
					imp_kwargs = dict()
					for imparg in m.captures("args"):
						eqidx = imparg.find("=")
						if eqidx >= 0:
							key = imparg[:eqidx]
							value = imparg[eqidx+1:].replace("\"", "")
							imp_kwargs[key] = value
						else:
							imp_args.append(imparg.replace("\"", ""))

					if imp_name in scanned:
						fragerror("Import loop detected:" + (" -> ".join(scanned + [imp_name])))

					scan_fragment(outfile, langdir, imp_name, imp_args, imp_kwargs, scanned + [imp_name], indent + imp_indent)
				else:
					line = (" " * indent) + line + "\n"
					outfile.write(line)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Generate a sublime syntax highlighter file from'
	                                             ' templates and fragments.')
	parser.add_argument('lang', metavar='LANG', type=str, nargs=1,
	                    help='The language to generate syntax highlighting for.')
	parser.add_argument('--dstdir', dest='dstdir', type=str, default=None,
	                    help='Specifies the target directory for the generated file.')

	args = parser.parse_args()
	main(args)
