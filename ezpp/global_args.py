import os
import glob


def add_global_argments(sub_parser):
    sub_parser.add_argument('-i',
                            '--infile',
                            help='input file or dir')

    sub_parser.add_argument('-r',
                            '--recursive',
                            default=False,
                            action='store_true',
                            help='recursive the input dir, outfiles will overwrite inputfiles. And the -o will be ignore')
    sub_parser.add_argument('-o',
                            '--outfile',
                            help='Optional the output file')


def parser_io_argments(params):
    infile = params['infile']
    outfile = params['outfile']
    recursive = params['recursive']
    if not os.path.exists(infile):
        print(f'Cant find --infile :{infile}')
        os._exit(1)

    if os.path.isfile(infile) and recursive:
        print('"-r" is only for inputfile is a dir')
        os._exit(1)

    if os.path.isdir(infile) and not recursive:
        print('"-r" is needed when --infile is a dir')
        os._exit(1)

    return infile, outfile, recursive


def get_recursive_pic_infiles(indir):
    file_exts = ['jpeg', 'jpg', 'png', 'webp', 'JPEG', 'JPG', 'PNG', 'WEBP']
    paths = []
    for file_ext in file_exts:
        type_filter_str = os.path.join(
            f'{indir}', f'**/*.{file_ext}')
        picfiles = glob.glob(type_filter_str, recursive=True)
        paths.extend(picfiles)
    return paths
