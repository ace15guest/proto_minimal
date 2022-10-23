from pathlib import Path
import os
import pickle


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def dependency_check():
    checks = [essential_data_folder_check, generated_folder_check, temporary]
    all_error = []
    for check in checks:
        status, error = check()
        all_error.extend(error)
        if not status:
            return

    print('-' * 50 + 'ERROR REPORT' + '-' * 50)
    for err in all_error:
        print(err)


def temporary():
    """

    :return:
    """
    errors = []
    try:
        Path("temp").mkdir(exist_ok=True, parents=True)
    except Exception as error:
        print(f"{bcolors.FAIL}Failed to make the broad temporary folder temp{bcolors.ENDC}")
        errors.append(f"{bcolors.FAIL}Failed to make the broad temporary folder temp\t\t{error}{bcolors.ENDC}")
    return True, errors


def generated_folder_check():
    """
       checks dependencies in generated
       ./generated/cifs
       ./generated/html
       ./generated/logs
       ./generated/pdfs
       :return:
       """
    required = ["cifs", "html", "logs", "pdfs"]
    errors = []
    if os.path.exists("generated"):
        try:
            for folder in required:
                Path("generated/" + folder).mkdir(parents=True, exist_ok=True)
                print(f"{bcolors.OKGREEN}Folder {folder} in location: {os.getcwd()}/generated{bcolors.ENDC}")
        except Exception as error:
            print(print(f"{bcolors.FAIL}{error}{bcolors.FAIL}"))
            errors.append(error)
    else:
        Path("generated").mkdir(parents=True, exist_ok=True)
        generated_folder_check()
    Path("generated/pdfs/temp").mkdir(parents=True, exist_ok=True)
    Path("generated/pdfs/checked").mkdir(parents=True, exist_ok=True)
    Path("generated/pdfs/unchecked").mkdir(parents=True, exist_ok=True)
    Path("generated/html/checked").mkdir(parents=True, exist_ok=True)
    Path("generated/html/unchecked").mkdir(parents=True, exist_ok=True)
    open("generated/pdfs/proto_page.pdf", "w")
    open("generated/pdfs/123_proto_page.pdf", "w")
    open("generated/logs/error.log", "w")

    return True, errors


def essential_data_folder_check():
    errors = []
    needed_files = ('.bib', '.cif', '.json')
    if not os.path.exists("essential_data"):
        print(
            f"{bcolors.FAIL}Fatal Error: \'essential_data\' directory does not exist. The build has stopped{bcolors.FAIL}")
        return False, errors
    else:
        if os.path.exists("essential_data/pickle/master_json_with_CIF.pickle"):
            pickle_in = open("essential_data/pickle/master_json_with_CIF.pickle", "rb")
            master_json = pickle.load(pickle_in)
            for item in master_json:
                found = []

                path = f"essential_data/JSONs/{item}"

                if os.path.isdir(path):
                    for file in os.listdir(path):
                        if file.endswith(needed_files):
                            found.append(os.path.splitext(file)[1])
                out = ''
                for ext in needed_files:
                    if ext in found:
                        out += f" {bcolors.OKGREEN}{ext}{bcolors.ENDC}"
                    else:
                        out += f" {bcolors.FAIL}{ext}{bcolors.FAIL}"
                        errors.append(f"{bcolors.FAIL}{path + ' is missing:': <100}  {ext:<100}{bcolors.ENDC}")
                print(f"{bcolors.BOLD}{path : <90}{bcolors.ENDC}{out}")

    if not os.path.exists("essential_data/pickle/prototype.pickle"):
        errors.append(f"{bcolors.FAIL}prototype.pickle is missing{bcolors.ENDC}")
    else:
        print(f"{bcolors.OKGREEN}Found: prototype.pickle{bcolors.ENDC}")

    if not os.path.exists("essential_data/anrl_protos_with_parameters.pretty.json"):
        errors.append(f"{bcolors.FAIL}anrl_protos_with_parametes.pretty.json is missing{bcolors.ENDC}")
    else:
        print(f"{bcolors.OKGREEN}Found: anrl_protos_with_parametes.pretty.json{bcolors.ENDC}")

    templates = ['prototype_template_html', 'prototype_template.tex']
    if os.path.exists('essential_data/templates'):
        for template in templates:
            if os.path.exists(f"essential_data/templates/{template}"):
                print(f"{bcolors.OKGREEN}Found: {template}{bcolors.ENDC}")
            else:
                message = f"{bcolors.FAIL}Missing: {'essential_data/tempaltes/' + template:>100}{bcolors.ENDC}"
                print(message)
                errors.append(message)



    return True, errors
#
dependency_check()
