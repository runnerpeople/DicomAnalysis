#!python
# -*- coding: utf-8 -*-

import json

class Study(object):

    study_instance_uid_tag = 0x0020000D
    study_id_tag = 0x00200010
    study_date_tag = 0x00080020
    study_time_tag = 0x00080030
    accession_number_tag = 0x00080050
    study_description_tag = 0x00081030
    institution_name_tag = 0x00080090

    referring_physician_name_tag = 0x00080090


    def __init__(self,parent_id,study_instance_uid,study_id,study_date,study_time,accession_number,
                 study_description,institution_name,referring_physician_name):
        self.parent_id = parent_id
        self.study_instance_uid = study_instance_uid
        self.study_id = study_id
        self.study_date = study_date
        self.study_time = study_time
        self.accession_number = accession_number
        self.study_description = study_description
        self.institution_name = institution_name
        self.referring_physician_name = referring_physician_name
        self.series = list()
        self.series_hash = dict()

    def add_serie(self,serie):
        if serie.serie_instance_uid in self.series_hash:
            hs = self.series_hash[serie.serie_instance_uid]
            img = hs.image_list

            for i in range(len(img)):
                hs.add_image(img[i])
        else:
            self.series.append(serie)
            self.series_hash[serie.serie_instance_uid] = serie

    def to_json(self):
        result = self.__dict__
        if "series" in result:
            result.pop("series")
        if "series_hash" in result:
            result.pop("series_hash")
        return result

    def __str__(self):
        return json.dumps(self, default=self.to_json(), sort_keys=True, indent=4)
