from argparse import ArgumentParser
from os.path import join
from cellml.api.pmr2.utility import CellMLAPIUtility

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


# generate all commands
commands = {
    cmd.__name__: cmd for cmd in [
        codegen,
    ]
}


def main():
    import sys
    import json
    argparser = ArgumentParser()
    subparser = argparser.add_subparsers(dest='cmd', metavar='<command>')

    codegen_ap = subparser.add_parser('codegen', help='CellML Codegen')
    codegen_ap.add_argument('--input-path', action='store')
    codegen_ap.add_argument('--output-dir', action='store')

    kwargs = vars(argparser.parse_args())
    cmd_key = kwargs.pop('cmd')
    commands[cmd_key](**kwargs)
