#!/usr/bin/env python2
import os
import re
import jinja2
import sys

RE_ALL = re.DOTALL | re.MULTILINE
RE_FILE_DOC = re.compile(r'\/\* docgen\n(.*?)\n\*\/\n(.*?)\(', RE_ALL)
RE_DOC_PARAM = re.compile(r'^ +- (.*?): (.*?)(?=^ +-|\Z)', RE_ALL)

EXTENSIONS = ('.c',)
DEST = 'result.md'


def get_files(path, extensions=[]):
    file_list = list()
    for (dir_, _, files) in os.walk(path):
        for f in files:
            for ext in extensions:
                if f.endswith(ext):
                    file_list.append(os.path.join(dir_, f))
    return file_list


def extract_doc(path):
    res = list()
    with open(path) as f:
        for doc in re.findall(RE_FILE_DOC, f.read()):
            match = dict(
                fn=doc[1].replace('\n', ' ').strip(),
                params=dict()
            )
            for pv in re.findall(RE_DOC_PARAM, doc[0]):
                # Fix newlines for markdown
                match['params'][pv[0]] = pv[1].replace('\n', '<br>')
            res.append(match)
    return res


def generate(path):
    doc = list()
    files = get_files(path, EXTENSIONS)
    for f in files:
        doc.append(dict(doc=extract_doc(f), file=f))
    return doc


def render(path, doc):
    path, file_ = os.path.split(path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(file_).render(doc=doc)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('Specify source folder')
    elif not os.path.isdir(sys.argv[1]):
        raise Exception('Source folder doesn\'t exist')
    with open(DEST, 'wb') as f:
        f.write(render('./template/main.md.j2',
                       generate(sys.argv[1])
                       )
                )
    print "Result saved to %s" % DEST
