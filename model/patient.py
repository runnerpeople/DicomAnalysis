#!python
# -*- coding: utf-8 -*-

import json

class Patient(object):

    patient_name_tag = 0x00100010
    patient_id_tag = 0x00100020
    patient_birth_tag = 0x00100030
    patient_sex_tag = 0x00100040

    def __init__(self,patient_name,patient_id,patient_birth,patient_sex):
        self.patient_name = patient_name
        self.patient_id = patient_id
        self.patient_birth = patient_birth
        self.patient_sex = patient_sex
        self.studies = list()
        self.studies_hash = dict()

    def add_study(self,study):
        if study.study_instance_uid in self.studies_hash:
            hs = self.studies_hash[study.study_instance_uid]
            hs.study_description = study.study_description
            for serie in study.series:
                hs.add_serie(serie)
        else:
            self.studies.append(study)
            self.studies_hash[study.study_instance_uid] = study

    def to_json(self):
        result = self.__dict__
        if "studies" in result:
            result.pop("studies")
        if "studies_hash" in result:
            result.pop("studies_hash")
        return result

    def __str__(self):
        return json.dumps(self, default=self.to_json(), sort_keys=True, indent=4)
