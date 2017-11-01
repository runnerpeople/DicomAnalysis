#!python
# -*- coding: utf-8 -*-

import json

class ImageD(object):

    instance_number_tag = 0x00200013
    patient_orientation_tag = 0x00200020
    content_date_tag = 0x00080023
    content_time_tag = 0x00080033
    image_type_tag = 0x00080008

    samples_per_pixel_tag = 0x00280002
    photometric_interpretation_tag = 0x00280004
    rows_tag = 0x00280010
    columns_tag = 0x00280011
    bits_allocated_tag = 0x00280100
    bits_stored_tag = 0x00280101
    high_bit_tag = 0x00280102
    pixel_representation_tag = 0x00280103
    pixel_aspect_ratio_tag = 0x00280034
    planar_configuration_tag = 0x00280006
    pixel_data_tag = 0x7FE00010
    sop_class_uid_tag = 0x00080016
    sop_instance_class_uid_tag = 0x00080018

    def __init__(self,parent_id, instance_number,patient_orientation,content_date,content_time,image_type,
                 samples_per_pixel,photometric_interpretation,rows,columns,bits_allocated,bits_stored,high_bit,
                 pixel_representation,pixel_aspect_ratio,pixel_data,planar_configuration):
        self.parent_id = parent_id
        self.instance_number = instance_number
        self.patient_orientation = patient_orientation
        self.content_date = content_date
        self.content_time = content_time
        self.image_type = image_type
        self.samples_per_pixel = samples_per_pixel
        self.photometric_interpretation = photometric_interpretation
        self.rows = rows
        self.columns = columns
        self.bits_allocated = bits_allocated
        self.bits_stored = bits_stored
        self.high_bit = high_bit
        self.pixel_representation = pixel_representation
        self.pixel_data = pixel_data
        self.pixel_aspect_ratio = pixel_aspect_ratio
        self.planar_configuration = planar_configuration

    def to_json(self):
        result = self.__dict__
        return result

    def __str__(self):
        return json.dumps(self, default=self.to_json(), sort_keys=True, indent=4)
