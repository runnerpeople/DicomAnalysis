#!python
# -*- coding: utf-8 -*-

import json

class Serie(object):

    serie_instance_uid_tag = 0x0020000E
    series_description_tag = 0x0008103E
    serie_number_tag = 0x00200011
    modality_tag = 0x00080060
    series_date_tag = 0x00080021
    series_time_tag = 0x00080031
    protocol_name_tag = 0x00181030
    laterality_tag = 0x00200062

    body_part_thickness_tag = 0x001811A0
    compression_force_tag = 0x001811A2


    body_part_examined_tag = 0x00180015
    view_position_tag = 0x00185101

    def __init__(self,parent_id,serie_instance_uid,series_description,serie_number,modality,series_date,
                 series_time,protocol_name,laterality,body_part_thickness, compression_force,body_part_examined,view_position):
        self.parent_id = parent_id
        self.serie_instance_uid = serie_instance_uid
        self.series_description = series_description
        self.serie_number = serie_number
        self.modality = modality
        self.series_date = series_date
        self.series_time = series_time
        self.protocol_name = protocol_name
        self.laterality = laterality
        self.body_part_thickness = body_part_thickness
        self.compression_force = compression_force
        self.body_part_examined = body_part_examined
        self.view_position = view_position
        self.image_list = list()
        self.image_hash = dict()

    def add_image(self,image):
        if image.serie_instance_uid not in self.image_hash:
            self.image_list.append(image)
            self.image_hash[image.sop_uid] = image

    def to_json(self):
        result = self.__dict__
        if "image_list" in result:
            result.pop("image_list")
        if "image_hash" in result:
            result.pop("image_hash")
        return result

    def __str__(self):
        return json.dumps(self, default=self.to_json(), sort_keys=True, indent=4)
