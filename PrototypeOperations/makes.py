from tempfile import TemporaryDirectory
import tempfile
import subprocess
import shutil
import os
# Project Imports
from PrototypeOperations.prototype_TeX import PrototypeEncyclopediaTeX


def printex(label, directory, failed_latex):
    """

    :param label:
    :param directory:
    :param failed_latex: This must be an attribute (i.e. self.failed_latex)
    :return:
    """
    tempfile.tempdir = os.getcwd() + "/generated/pdfs/temp"
    with TemporaryDirectory() as tempdir:
        temp_file = tempdir + f'/{label}.tex'
        temp_file_pdf = tempdir + f'/{label}.pdf'
        with open(temp_file, 'w') as t:
            proto = PrototypeEncyclopediaTeX(label, 'essential_data/JSONs', "essential_data/anrl_protos_with_parameters.pretty.json", 'essential_data/JSONs', 'essential_data/proto.tex')

            if proto.data_info is None:
                if not os.path.exists(directory):
                    pass
                shutil.copyfile(f'redesignate/failed.pdf', directory + f'/has_image/{label}.pdf')
                failed_latex.append(label)
                print(label)
                return
            else:
                t.write(proto.generate_tex())
            # exit()
        cmd = ['latexmk', '-pdf', '-interaction=nonstopmode', temp_file]
        try:
            # current_dir = (pathlib.Path('..'))
            # print(current_dir.resolve())
            #            subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=30, cwd=current_dir.resolve().as_posix()+'/pdfs')
            # print(tempdir)
            with open(tempdir + '/foundin.bib', 'w') as f:
                f.write(proto.found_ins_bib)
                f.close()
            with open(tempdir + '/references.bib', 'w') as f:
                f.write(proto.bibliography_bib)
                f.close()

            subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=30, cwd=tempdir)
        except Exception as e:
            error = open("generated/logs/error.log", "a")
            error.write(str(e) + "\n")
            error.close()

        if os.path.exists(f"essential_data/PICS/{label.split('-')[0]}_composite_full.png"):
            try:
                shutil.move(temp_file_pdf, directory + f'/has_image/{label}.pdf')
            except Exception as e:
                if not os.path.exists(directory + "/has_image"):
                    os.mkdir(directory + "/has_image")
                shutil.move(temp_file_pdf, directory + f'/has_image/{label}.pdf')

        else:
            try:
                shutil.move(temp_file_pdf, directory + f'/no_image/{label}.pdf')
            except Exception as e:
                if not os.path.exists(directory + "/no_image"):
                    os.mkdir(directory + "/no_image")
                shutil.move(temp_file_pdf, directory + f'/no_image/{label}.pdf')
