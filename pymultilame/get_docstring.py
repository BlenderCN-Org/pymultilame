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
Récupère la doc de tous les scripts pour le wiki
et enregistre dans tools/docstring.txt
TODO:
    pour les scripts qui importent twisted ou pour OSC3, la doc est très longue.
    Voir pour que pydoc3.5 ne prennent pas en compte les héritages.
"""

import re
import ast

import pydoc

from mytools import MyTools


class GetDoc:
    """
    Lit tous les scripts pour récupérer les docstrings.
    Enregistre dans un fichier docstring.txt
    classé par script
    Contrainte:
    - doc du script
    - doc de la classe avec Usage
    - doc des méthodes
    - Ne récupère pas les fonctions en dehors de la class,
      ni le if __name__ == '__main__':
    """

    def __init__(self, directory):
        """
        directory = dossier racine de recherche des scripts
        """
        self.directory = directory
        self.mt = MyTools()
        self.DOC = ""

    def get_doc_batch(self):
        """
        OSC3 et twisted dénére une doc top longue
        pas de 
        './irctwisted.py'
        './tcptwisted.py'
        './multicasttwisted.py'
        './get_docstring.py', les variables dict_doc etc ... rallonge
        """
        all_scripts = [ './blendergetobject.py',
                        './blendersound.py',
                        './blendertempo.py',
                        './blendertexture.py',
                        './blendertools.py',
                        './blenderviewport.py',
                        './fifolist.py',
                        './getmyip.py',
                        './httpdownload.py',
                        './multicast.py',
                        './myconfig.py',
                        './mytools.py',
                        './tcpclient.py',
                        './udpclient.py']

        for script in all_scripts:
            self.get_doc(script)

        # Enregister en écrasant dans "docstring.txt"
        self.DOC += '\n'
        print(self.DOC)
        self.save_doc(self.DOC)
        
    def get_doc(self, script):
        """
        Crée la doc du script avec pydoc3.5
        Installation de pydoc3.5
        sudo pip3 install pydoc
        et l'ajoute à self.DOC
        """
        
        command = ['pydoc3.5', script]
        resp = self.mt.run_command_system(command)
        doc = self.improve_resp(resp)
        
        # Ajout
        self.DOC += '====' + script[2:-3] + '====\n'
        self.DOC += '<code txt>\n' + doc + '</code>\n\n'

    def save_doc(self, doc):
        """
        Save in docstring.txt
        """
        fichier = "docstring.txt"
        self.mt.write_data_in_file(doc, fichier)

    def improve_resp(self, resp):
        """
        Amélioration par suppression de l'inutile!
        """
        # Suppression des 5 premières lignes
        lines = resp.splitlines()  # list
        lines = lines[5:]

        n = 0
        line_to_delete = []
        for line in lines:
            # Si DATA au début de la ligne, suppr de la ligne et la suivante
            if line[:4] == 'DATA':
                line_to_delete.extend([n, n+1])

            # Si FILE au début de la ligne, suppr de la ligne et la suivante
            if line[:4] == 'FILE':
                line_to_delete.extend([n, n+1, n+2])

            # Si CLASSES au début de la ligne, suppr de la ligne et la suivante
            if line[:7] == 'CLASSES':
                line_to_delete.extend([n+1, n+2, n+3])

            # au suivant
            n += 1
            
        # Suppression des lignes
        somelist = [i for j, i in enumerate(lines) if j not in line_to_delete]

        # Suppr des 2 dernières lignes
        somelist = somelist[:-2]
        
        # Reconversion de la liste en str
        doc = ''
        for l in somelist:
            doc += l + '\n'

                # suppression des docs héritées
        usefull_doc = self.suppr_inheritance(doc)
        
        return usefull_doc

    def suppr_inheritance(self, doc):

        doc = doc.replace(dict_doc_1, '')
        doc = doc.replace(dict_doc_2, '')
        doc = doc.replace(dict_doc_3, '')
        doc = doc.replace(data_dict_doc, '')
        
        return doc


data_dict_doc = """     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
"""

dict_doc_1 = """|  ----------------------------------------------------------------------
     |  Methods inherited from builtins.dict:
     |  
     |  __contains__(self, key, /)
     |      True if D has a key k, else False.
     |  
     |  __delitem__(self, key, /)
     |      Delete self[key].
     |  
     |  __eq__(self, value, /)
     |      Return self==value.
     |  
     |  __ge__(self, value, /)
     |      Return self>=value.
     |  
     |  __getattribute__(self, name, /)
     |      Return getattr(self, name).
     |  
     |  __getitem__(...)
     |      x.__getitem__(y) <==> x[y]
     |  
     |  __gt__(self, value, /)
     |      Return self>value.
     |  
     |  __iter__(self, /)
     |      Implement iter(self).
     |  
     |  __le__(self, value, /)
     |      Return self<=value.
     |  
     |  __len__(self, /)
     |      Return len(self).
     |  
     |  __lt__(self, value, /)
     |      Return self<value.
     |  
     |  __ne__(self, value, /)
     |      Return self!=value.
     |  
     |  __new__(*args, **kwargs) from builtins.type
     |      Create and return a new object.  See help(type) for accurate signature.
     |  
     |  __repr__(self, /)
     |      Return repr(self).
     |  
     |  __setitem__(self, key, value, /)
     |      Set self[key] to value.
     |  
     |  __sizeof__(...)
     |      D.__sizeof__() -> size of D in memory, in bytes
     |  
     |  clear(...)
     |      D.clear() -> None.  Remove all items from D.
     |  
     |  copy(...)
     |      D.copy() -> a shallow copy of D
     |  
     |  fromkeys(iterable, value=None, /) from builtins.type
     |      Returns a new dict with keys from iterable and values equal to value.
     |  
     |  get(...)
     |      D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None.
     |  
     |  items(...)
     |      D.items() -> a set-like object providing a view on D's items
     |  
     |  keys(...)
     |      D.keys() -> a set-like object providing a view on D's keys
     |  
     |  pop(...)
     |      D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
     |      If key is not found, d is returned if given, otherwise KeyError is raised
     |  
     |  popitem(...)
     |      D.popitem() -> (k, v), remove and return some (key, value) pair as a
     |      2-tuple; but raise KeyError if D is empty.
     |  
     |  setdefault(...)
     |      D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D
     |  
     |  values(...)
     |      D.values() -> an object providing a view on D's values
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from builtins.dict:
     |  
     |  __hash__ = None
"""

dict_doc_2 = """|  
     |  update(self)
     |      D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.
     |      If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]
     |      If E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v
     |      In either case, this is followed by: for k in F:  D[k] = F[k]
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from builtins.dict:
     |  
     |  __contains__(self, key, /)
     |      True if D has a key k, else False.
     |  
     |  __delitem__(self, key, /)
     |      Delete self[key].
     |  
     |  __eq__(self, value, /)
     |      Return self==value.
     |  
     |  __ge__(self, value, /)
     |      Return self>=value.
     |  
     |  __getattribute__(self, name, /)
     |      Return getattr(self, name).
     |  
     |  __getitem__(...)
     |      x.__getitem__(y) <==> x[y]
     |  
     |  __gt__(self, value, /)
     |      Return self>value.
     |  
     |  __iter__(self, /)
     |      Implement iter(self).
     |  
     |  __le__(self, value, /)
     |      Return self<=value.
     |  
     |  __len__(self, /)
     |      Return len(self).
     |  
     |  __lt__(self, value, /)
     |      Return self<value.
     |  
     |  __ne__(self, value, /)
     |      Return self!=value.
     |  
     |  __new__(*args, **kwargs) from builtins.type
     |      Create and return a new object.  See help(type) for accurate signature.
     |  
     |  __repr__(self, /)
     |      Return repr(self).
     |  
     |  __setitem__(self, key, value, /)
     |      Set self[key] to value.
     |  
     |  __sizeof__(...)
     |      D.__sizeof__() -> size of D in memory, in bytes
     |  
     |  clear(...)
     |      D.clear() -> None.  Remove all items from D.
     |  
     |  copy(...)
     |      D.copy() -> a shallow copy of D
     |  
     |  fromkeys(iterable, value=None, /) from builtins.type
     |      Returns a new dict with keys from iterable and values equal to value.
     |  
     |  get(...)
     |      D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None.
     |  
     |  items(...)
     |      D.items() -> a set-like object providing a view on D's items
     |  
     |  keys(...)
     |      D.keys() -> a set-like object providing a view on D's keys
     |  
     |  pop(...)
     |      D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
     |      If key is not found, d is returned if given, otherwise KeyError is raised
     |  
     |  popitem(...)
     |      D.popitem() -> (k, v), remove and return some (key, value) pair as a
     |      2-tuple; but raise KeyError if D is empty.
     |  
     |  setdefault(...)
     |      D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D
     |  
     |  values(...)
     |      D.values() -> an object providing a view on D's values
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from builtins.dict:
     |  
     |  __hash__ = None
"""

dict_doc_3 = """     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from builtins.dict:
     |  
     |  __contains__(self, key, /)
     |      True if D has a key k, else False.
     |  
     |  __delitem__(self, key, /)
     |      Delete self[key].
     |  
     |  __eq__(self, value, /)
     |      Return self==value.
     |  
     |  __ge__(self, value, /)
     |      Return self>=value.
     |  
     |  __getattribute__(self, name, /)
     |      Return getattr(self, name).
     |  
     |  __getitem__(...)
     |      x.__getitem__(y) <==> x[y]
     |  
     |  __gt__(self, value, /)
     |      Return self>value.
     |  
     |  __iter__(self, /)
     |      Implement iter(self).
     |  
     |  __le__(self, value, /)
     |      Return self<=value.
     |  
     |  __len__(self, /)
     |      Return len(self).
     |  
     |  __lt__(self, value, /)
     |      Return self<value.
     |  
     |  __ne__(self, value, /)
     |      Return self!=value.
     |  
     |  __new__(*args, **kwargs) from builtins.type
     |      Create and return a new object.  See help(type) for accurate signature.
     |  
     |  __repr__(self, /)
     |      Return repr(self).
     |  
     |  __setitem__(self, key, value, /)
     |      Set self[key] to value.
     |  
     |  __sizeof__(...)
     |      D.__sizeof__() -> size of D in memory, in bytes
     |  
     |  clear(...)
     |      D.clear() -> None.  Remove all items from D.
     |  
     |  copy(...)
     |      D.copy() -> a shallow copy of D
     |  
     |  fromkeys(iterable, value=None, /) from builtins.type
     |      Returns a new dict with keys from iterable and values equal to value.
     |  
     |  get(...)
     |      D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None.
     |  
     |  items(...)
     |      D.items() -> a set-like object providing a view on D's items
     |  
     |  keys(...)
     |      D.keys() -> a set-like object providing a view on D's keys
     |  
     |  pop(...)
     |      D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
     |      If key is not found, d is returned if given, otherwise KeyError is raised
     |  
     |  popitem(...)
     |      D.popitem() -> (k, v), remove and return some (key, value) pair as a
     |      2-tuple; but raise KeyError if D is empty.
     |  
     |  setdefault(...)
     |      D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D
     |  
     |  update(...)
     |      D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.
     |      If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]
     |      If E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v
     |      In either case, this is followed by: for k in F:  D[k] = F[k]
     |  
     |  values(...)
     |      D.values() -> an object providing a view on D's values
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from builtins.dict:
     |  
     |  __hash__ = None
"""



if __name__ == '__main__':
    d = "/media/data/3D/projets/pymultilame/pymultilame/"
    gd = GetDoc(d)
    gd.get_doc_batch() 
