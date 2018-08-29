#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#######################################################################
# Copyright (C) La Labomedia August 2018
#
# This file is part of pymultilame.

# pymultilame is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pymultilame is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pymultilame.  If not, see <https://www.gnu.org/licenses/>.
#######################################################################

"""
Des méthodes souvent appelées par les autres scripts,
regroupées dans une class MyTools
"""


import os
import subprocess
import pathlib
from json import dumps, loads

__all__ = ['MyTools']


class MyTools:

    def get_all_files_list(self, root, file_end):
        """
        Lit le dossier et tous les sous-dosssiers.
        Retourne une liste de tous les fichiers avec l'extension file_end
        avec le chemin absolu
        exemple:
            "network/http_download.py"
        """
        file_list = []
        
        for path, subdirs, files in os.walk(root):
            for name in files:
                if name.endswith(file_end):
                    file_list.append(str(pathlib.PurePath(path, name)))
                
        return file_list
        
    def read_file(self, file_name):
        """
        Retourne les datas lues dans le fichier avec son chemin/nom
        Retourne None si fichier inexistant ou impossible à lire .
        """

        try:
            with open(file_name) as f:
                data = f.read()
            f.close()
        except:
            data = None
            print("Fichier inexistant ou impossible à lire:", file_name)

        return data

    def write_data_in_file(self, data, fichier):
        """
        Ecrit des data de type string dans le fichier, écrase l'existant.
        """

        with open(fichier, 'w') as fd:
            fd.write(data)
        fd.close()

    def data_to_json(self, data):
        """Retourne le json des datas"""

        return dumps(data)

    def get_json_file(self, fichier):
        """Retourne le json décodé des datas lues
        dans le fichier avec son chemin/nom.
        """
        with open(fichier) as f:
            data = f.read()
        f.close()

        data = loads(data)

        return data

    def print_all_key_value(self, my_dict):
        """
        Imprime un dict contenant un dict,
        affiche le nombre de clés total.
        """

        total = 0

        for k, v in my_dict.items():
            print(k)
            for f in v:
                total += 1
                print("    ", f)
        print("Nombre de clés total =", total)
        print("pour un théorique par jour de =", 24*1)

    def create_directory(self, directory):
        """
        Crée le répertoire avec le chemin absolu.
        ex: /media/data/3D/projets/meteo/meteo_forecast/2017_06
        """

        try:
            pathlib.Path(directory).mkdir(mode=0o777, parents=False)
            print("Création du répertoire: {}".format(directory))
        except FileExistsError as e:
            pass

    def get_absolute_path(self, a_file_or_a_directory):
        """
        Retourne le chemin absolu d'un répertoire ou d'un fichier
        n'importe où.
        """

        return os.path.abspath(a_file_or_a_directory)

    def run_command_system(self, command):
        """
        Excécute la command shell et reourne la sortie terminal.
        command = ['your_command', 'arg1', 'arg2', ...]
        Ne marche pas:
            resp = subprocess.call(command.split())
        """
        p = subprocess.Popen(command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        output, errors = p.communicate()

        return output.decode('utf-8')


def test_run_command_system():
    
    mt = MyTools()
    
    # ls du dossiercourant
    print(mt.run_command_system(['ls']))
    
    # ls du dossiercourant
    print(mt.run_command_system(['pydoc3.5', 'pymultilame.HttpDownload']))
    
    
def test_get_all_files_list():
    """
    Recherche des py et txt dans pymultilame/pymultilame/
    """
    
    mt = MyTools()
    d = "/media/data/3D/projets/pymultilame/pymultilame/"
    
    print("list des py dans", d)
    l = mt.get_all_files_list(d, "py")
    for f in l:
        print(f)

    print("list des txt dans", d)
    l = mt.get_all_files_list(d, "txt")
    for f in l:
        print(f)


if __name__ == "__main__":

    test_get_all_files_list()
    test_run_command_system()
