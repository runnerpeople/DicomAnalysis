#!python
# -*- coding: utf-8 -*-

import json

class DICOM(object):

    def __init__(self,parent_id,name_file,modified=None,user_info=None):
        self.parent_id = parent_id
        self.name_file = name_file
        self.modified = modified
        self.user_info = user_info


    def to_json(self):
        result = self.__dict__
        return result

    def __str__(self):
        return json.dumps(self, default=self.to_json(), sort_keys=True, indent=4)
