from argparse import ArgumentParser
from inspect import getargspec
from os.path import join

from cellml.api.pmr2.utility import CellMLAPIUtility

try:
    from pmr2.processor.legacy.transforms import tmpdoc2html
except ImportError:
    tmpdoc2html = None

# codegen

codegen_fileext = {
    'Python': 'py',
    'C_IDA': 'c',
    'C': 'c',
    'F77': 'f77',
    'MATLAB': 'm',
}

def codegen(input_path, output_dir):
    cu = CellMLAPIUtility()
    model = cu.model_loader.loadFromURL(input_path)
    for k, v in cu.exportCeleds(model).items():
        output_file = join(output_dir, 'code.%s.%s' % (k, codegen_fileext[k]))
        with open(output_file, 'w') as fd:
            fd.write(v)


# docgen

def tmpdoc(input_path, output_dir):
    with open(input_path) as inc:
        output = tmpdoc2html(inc)
        output_file = join(output_dir, 'index.html')
        with open(output_file, 'w') as fd:
            fd.write(output.getvalue())

def htmldoc(input_path, output_dir):
    with open(input_path) as inc:
        output_file = join(output_dir, 'index.html')
        with open(output_file, 'w') as fd:
            fd.write(inc.read())

docs = [
    (htmldoc, 'HTML Documentation'),
]

if tmpdoc2html:
    docs.append((tmpdoc, 'CellML legacy tmpdoc'))

docs_lookup = {fn.__name__: fn for fn, _ in docs}

def docgen(doctype, input_path, output_dir):
    docs_lookup[doctype](input_path, output_dir)

# set up commands

cmd_fns = [
    (codegen, 'CellML codegen'),
    (docgen, 'CellML docgen'),
]

def generate_cmd_parser(cmd_fns):
    commands = {}
    argparser = ArgumentParser()
    ap_grp = argparser.add_subparsers(dest='cmd', metavar='<command>')

    for cmd_fn, help_text in cmd_fns:
        commands[cmd_fn.__name__] = cmd_fn
        sub_ap = ap_grp.add_parser(cmd_fn.__name__, help=help_text)
        argspec = getargspec(cmd_fn)
        for arg in argspec.args:
            sub_ap.add_argument(
                '--' + arg.replace('_', '-'),
                action='store',
                required=True,
            )

    return commands, argparser


def main():
    commands, argparser = generate_cmd_parser(cmd_fns)
    kwargs = vars(argparser.parse_args())
    cmd_key = kwargs.pop('cmd')
    commands[cmd_key](**kwargs)
