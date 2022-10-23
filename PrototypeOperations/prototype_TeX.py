import json
import pathlib
import re
import subprocess
import jinja2
import jmespath
import logger
import numpy as np
import os

class PrototypeEncyclopediaTeX:

    def __init__(self, anrl_prototype_label, info_json_folder_path, anrl_json_path, bib_folder_path, jinja_template, html_template='prototype_template_AG.html', generate_html=True):
        """

        :param anrl_prototype_label:
        :param info_json_folder_path:
        :param anrl_json_path:
        :param bib_folder_path:
        :param jinja_template:
        :param html_template:
        """

        self.ind = None
        self.anrl_prototype_label = anrl_prototype_label
        self.info_json_folder_path = info_json_folder_path
        self.anrl_json_path = anrl_json_path
        self.bib_folder_path = bib_folder_path
        self.encyclopedia_prototype_label = anrl_prototype_label.split('-')[0]
        self.data_david = None
        self.load_data_david()
        self.data_anrl = None
        self.info_json_path = None
        self.data_info = None
        self.old_comments = self.data_david[self.encyclopedia_prototype_label]['comments']['latex'],
        self.bibliography_bib = None
        self.found_ins_bib = ''
        self.load_found_ins()
        self.load_bib()
        if generate_html:
            self.load_proto_jsons()
        self.latex_jinja_env = None
        self.html_jinja_env = None
        self.set_jinja_env()
        self.set_html_jinja_env()
        self.template = self.latex_jinja_env.get_template(jinja_template)
        self.html_template = self.html_jinja_env.get_template(html_template)

    #########################
    # Initializer Functions #
    #########################
    def load_data_david(self):
        data_json = json.load(open("essential_data/all_prototypes_parts_1_2_3.json"))
        lab_list = [i['aflow_label']['html'] for i in data_json]
        self.data_david = dict(zip(lab_list, data_json))

    def load_found_ins(self):
        bib_folder = pathlib.Path(self.bib_folder_path)
        temp = bib_folder.glob('**/found_in.bib')
        for i in temp:
            if i.parent.name == self.encyclopedia_prototype_label:
                self.found_ins_bib = i.read_text()
                # loader status
                # print("loaded found_in: ", i.resolve())
                # TODO: What purpose does this serve
                with open('temp/temp_found_ins.bib', 'w') as f:
                    f.write(self.found_ins_bib)
        # TODO: Check least misfit as well

    def load_bib(self):
        bib_folder = pathlib.Path(self.bib_folder_path)
        temp = bib_folder.glob('**/*.bib')
        for i in temp:
            if i.name != 'found_in.bib' and i.parent.name == self.encyclopedia_prototype_label:
                try:
                    self.bibliography_bib = i.read_text()
                    break
                except Exception as error:
                    print(error)
                    logger.error(error)
                # loader status
                # print("loaded found_in: ", i.resolve())
                # with open('temp_found_ins.bib', 'w') as f:
                #     f.write(self.found_ins_bib)
        # print("found ins", self.found_ins_bib)

    def load_proto_jsons(self):
        full_anrl_json = json.load(open(self.anrl_json_path))

        self.data_anrl = jmespath.search(f'[?label==`{self.anrl_prototype_label}`]', full_anrl_json)
        json_folder = pathlib.Path(self.info_json_folder_path)
        temp = json_folder.glob('**/*.json')
        self.ind = full_anrl_json.index(self.data_anrl[0])

        for i in temp:
            folder = i.parent.name
            if str(folder == str(self.encyclopedia_prototype_label)):
                print(folder)
                try:

                    self.data_info = json.load(open(i))
                    # loader status
                    # print("loaded info json: ", i.resolve())
                    self.info_json_path = i.resolve()
                    break
                except Exception as error:
                    with open("generated/logs/error.log", "a") as f:
                        f.write(str(error) + "\n")
                        f.close()

                    # error = open("generated/logs/error.log", "a")
                    # error.write(str(e) + "\n")
                    # error.close()

    def set_jinja_env(self):
        self.latex_jinja_env = jinja2.Environment(
            block_start_string='\BLOCK{',
            block_end_string='}',
            variable_start_string='\VAR{',
            variable_end_string='}',
            comment_start_string='\#{',
            comment_end_string='}',
            line_statement_prefix='%%',
            line_comment_prefix='%#',
            trim_blocks=True,
            autoescape=False,
            loader=jinja2.FileSystemLoader(os.path.abspath('.'))
        )

    def set_html_jinja_env(self):
        self.html_jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.abspath('./static/templates'))
        )

    #######################
    # Generator Functions #
    #######################
    def generate_tex(self):
        proto_page = self.template.render(
            prototypeMaterial=self.get_Prototype(),
            paramsList=self.get_AFLOW_prototype_command(),
            AFLOWPrototypeLabelEscaped=self.get_AFLOW_prototype_label(escaped=True),
            AFLOWPrototypeLabel=self.get_AFLOW_prototype_label(),
            strukturberichtDesignation=self.get_Strukturbericht_designation(),
            comments=self.get_comments(),
            clean_comments=self.get_clean_comments(),
            pearsonSymbol=self.get_Pearson_symbol(),
            spaceGroupNumber=self.get_Space_group_number(),
            spaceGroupSymbol=self.get_space_group_symbol(),
            primitiveVectors=self.get_primitive_vectors(),
            basisVectors=self.get_basis_vectors())
        return proto_page

    ##############################
    # Generator Helper Functions #
    ##############################
    def get_Prototype(self):
        if "prototype" in self.data_info:
            return self.data_info["prototype"]
        else:
            return "not found"

    def get_AFLOW_prototype_command(self):
        if "params_list" in self.data_anrl:
            params_list = self.data_anrl["params_list"]
        else:
            return "not found"
        params_list = re.sub("[0-9]+", r"_{\g<0>}", params_list).replace('gamma', '\\gamma').replace('alpha',
                                                                                                     '\\alpha').replace(
            'beta', '\\beta').replace(',', ', \\allowbreak ')
        return params_list

    def get_AFLOW_prototype_label(self, escaped=False):
        if escaped:
            return self.encyclopedia_prototype_label.replace('_', '\\_')
        return self.encyclopedia_prototype_label

    def get_Strukturbericht_designation(self):
        if "strukturbericht" in self.data_info:
            return self.data_info["strukturbericht"]
        else:
            return "None"

    def get_comments(self):
        if "comments" in self.data_info and self.data_info["comments"] != '':
            comment_list = self.data_info["comments"].split('\n')
            comments = '\\begin{flushleft} \n \\begin{itemize} \n' + '\\\\'.join(
                f'\\item{{{l}}}' for l in comment_list) + '\n  \\end{itemize}  \n \\end{flushleft}'
            return comments
        else:
            return ""

    def get_clean_comments(self):
        comments_clean = self.data_david[self.encyclopedia_prototype_label]['comments']['latex']
        comment_list = comments_clean.split('\n')
        comments = '\\begin{flushleft} \n \\begin{itemize} \n' + '\\\\'.join(
            f'\\item{{{l}}}' for l in comment_list) + '\n  \\end{itemize}  \n \\end{flushleft}'
        return comments

    def get_Pearson_symbol(self):
        return self.encyclopedia_prototype_label.split('_')[1]

    def get_Space_group_number(self):
        return self.encyclopedia_prototype_label.split('_')[2]

    def get_space_group_symbol(self):
        result = subprocess.run(["aflow", f"--proto={self.anrl_prototype_label}", "--cif"], stdout=subprocess.PIPE)
        lines = result.stdout.decode('utf-8').split('\n')
        space = ''
        for line in lines:
            if re.search("_symmetry_space_group_name", line):
                space = line.split()[1].strip('\'')

    def get_primitive_vectors(self):
        result = subprocess.run(["aflow", f"--proto={self.anrl_prototype_label}", "--equations_only"],
                                stdout=subprocess.PIPE)
        res = result.stdout.decode('utf-8').split("\n")
        wyckoff_index = [i for i, s in enumerate(res) if 'Wyckoff' in s]
        direct_index = [i for i, s in enumerate(res) if 'Direct' in s]
        primitive = res[wyckoff_index[0] + 2:direct_index[0] - 1]
        primitive = [i.strip() for i in primitive]
        basis = res[direct_index[0] + 1:-1]
        basis = [i.strip() for i in basis]
        primitive = [i.split() for i in primitive]
        basis = [i.split() for i in basis]
        # print(primitive)
        # print(basis)

        hats = ['\\, \\mathbf{\\hat{x}}', '\\, \\mathbf{\\hat{y}}', '\\, \\mathbf{\\hat{z}}']
        for i, p in enumerate(primitive):
            for idx, xyz in enumerate(p):
                primitive[i][idx] = self.conv_text2latex(xyz) + hats[idx] + '+'
        primitive = self.make_a(primitive)
        return primitive

    def get_basis_vectors(self):
        result = subprocess.run(["aflow", f"--proto={self.anrl_prototype_label}", "--equations_only"],
                                stdout=subprocess.PIPE)
        res = result.stdout.decode('utf-8').split("\n")
        direct_index = [i for i, s in enumerate(res) if 'Direct' in s]
        basis = res[direct_index[0] + 1:-1]
        basis = [i.strip() for i in basis]
        basis = [i.split() for i in basis]
        basis = (np.array(basis)[:, 0:3]).tolist()
        check = np.array(['a', 'b', 'c'])
        hats = ['\\, \\mathbf{\\hat{x}}', '\\, \\mathbf{\\hat{y}}', '\\, \\mathbf{\\hat{z}}', 'I \\\\']
        # print(basis)
        # exit()
        for i, p in enumerate(basis):
            for idx, xyz in enumerate(p):
                # print(idx)
                # print(xyz)
                if len(xyz.split('+')) > 1:
                    basis[i][idx] = '(' + self.conv_text2latex(xyz) + ')' + hats[idx] + '+'
                else:
                    basis[i][idx] = self.conv_text2latex(xyz) + hats[idx] + '+'
        basis = self.make_b(basis)
        return basis
