#!python
# -*- coding: utf-8 -*-

import json
import bcrypt

class Physician(object):

    # not necessary (Can create anything name)
    physician_name_tag = 0x00080090

    def __init__(self,login,password,phone,name):
        self.name = name
        self.login = login
        self.phone = phone
        self.password = bcrypt.hashpw(password.encode(),bcrypt.gensalt())

    def to_json(self):
        result = self.__dict__
        return result

    def __str__(self):
        return json.dumps(self, default=self.to_json(), sort_keys=True, indent=4)