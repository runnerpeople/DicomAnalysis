#!python
# -*- coding: utf-8 -*-

from os.path import *
import logging
import datetime
from time import *
import io
import numpy
import random
import base64

import pymongo
from pydicom import read_file
from pydicom.filereader import *
from pymongo import MongoClient,ReturnDocument
from bson.objectid import ObjectId

from dicom.dicom_standard import *
from model.patient import *
from model.serie import *
from model.study import *
from model.image import *
from model.dicom import *
from model.physician import *

from util.med2image import *
from util.image import *

client = MongoClient('mongodb://localhost:27017/')
db = client['DICOM']

patients = db['patient']
studies = db['study']
series = db['serie']
images = db['image']
physicians = db['physician']
dicom_files = db['dicom']

JPG_DIRECTORY = join(dirname(__file__),"Image")

def time_to_int(time):
    return time.hour * 3600 + time.hour * 60 + time.second

def int_to_time(time_int):
    hours = time_int / 3600
    minutes = time_int - hours * 3600
    seconds = time_int - hours * 3600 - minutes * 60
    return datetime.time(hours,minutes,seconds)

def get_value(ds,tag,type):
    if type == required:
        return ds.get_item(tag)
    else:
        return ds.get(tag,None)
    # Another types for different tags

def convert_value(value,type_):
    if value is None or value.value == "":
        return None
    value_ = value.value
    if type_ == person_name:
        return value_.original_string
    elif type_ == date:
        return datetime.datetime.strptime(value_,"%Y%m%d")
    elif type_ == time_:
        return time_to_int(datetime.datetime.strptime(value_,"%H%M%S").time())
    elif type_ == decimal_string:
        return float(value_)
    elif type_ == integer_string:
        return int(value_)
    elif type_ == unsigned_short:
        if isinstance(value_,int):
            return int(value_)
        elif isinstance(value,bytes):
            return value.value_tell
    else:
        return value_

def insert_patient(ds):
    patient_name = convert_value(get_value(ds,Patient.patient_name_tag,required_or_empty),person_name)
    patient_id = convert_value(get_value(ds,Patient.patient_id_tag,required_or_empty),long_string)
    patient_birth = convert_value(get_value(ds,Patient.patient_birth_tag,required_or_empty),date)
    patient_sex = convert_value(get_value(ds,Patient.patient_sex_tag,required_or_empty),code_string)

    patient = Patient(patient_name,patient_id,patient_birth,patient_sex)
    patientFind = patients.find_one(patient.to_json())
    if patientFind is None:
        insert = patients.insert_one(patient.to_json())
        return patients.find_one({"_id":insert.inserted_id})
    else:
        return patientFind

def insert_study(ds,parent_id):
    study_instance_uid = convert_value(get_value(ds,Study.study_instance_uid_tag,required),unique_identifier)
    study_id = convert_value(get_value(ds,Study.study_id_tag,required_or_empty),short_string)
    study_date = convert_value(get_value(ds,Study.study_date_tag,required_or_empty),date)
    study_time = convert_value(get_value(ds,Study.study_time_tag,required_or_empty),time_)

    accession_number = convert_value(get_value(ds,Study.accession_number_tag,required_or_empty),short_string)

    study_description = convert_value(get_value(ds,Study.study_description_tag,optional),long_string)
    institution_name = convert_value(get_value(ds,Study.institution_name_tag,optional),long_string)
    referring_physician_name = convert_value(get_value(ds,Study.referring_physician_name_tag,required_or_empty),person_name)

    study = Study(parent_id,study_instance_uid,study_id,study_date,study_time,accession_number,study_description,
                  institution_name,referring_physician_name)
    studyFind = studies.find_one(study.to_json())
    if studyFind is None:
        insert = studies.insert_one(study.to_json())
        return studies.find_one({"_id": insert.inserted_id})
    else:
        return studyFind

def insert_series(ds,parent_id):

    serie_instance_uid = convert_value(get_value(ds, Serie.serie_instance_uid_tag, required), unique_identifier)
    series_description = convert_value(get_value(ds, Serie.series_description_tag, optional), long_string)
    serie_number = convert_value(get_value(ds, Serie.serie_number_tag, required_or_empty), integer_string)
    modality = convert_value(get_value(ds, Serie.modality_tag, required), code_string)
    series_date = convert_value(get_value(ds,Serie.series_date_tag,optional),date)
    series_time = convert_value(get_value(ds,Serie.series_time_tag, optional), time_)

    protocol_name = convert_value(get_value(ds,Serie.protocol_name_tag,optional),long_string)
    laterality = convert_value(get_value(ds,Serie.laterality_tag,conditionally_required_or_empty),code_string)

    body_part_thickness = convert_value(get_value(ds,Serie.body_part_thickness_tag,optional),decimal_string)
    compression_force = convert_value(get_value(ds, Serie.compression_force_tag, optional),decimal_string)

    body_part_examined = convert_value(get_value(ds, Serie.body_part_examined_tag, optional),code_string)
    view_position = convert_value(get_value(ds,Serie.view_position_tag,conditionally_required_or_empty),code_string)


    serie = Serie(parent_id, serie_instance_uid,series_description,serie_number,modality,
                  series_date,series_time,protocol_name,laterality,body_part_thickness,compression_force,
                  body_part_examined,view_position)
    serieFind = series.find_one(serie.to_json())
    if serieFind is None:
        insert = series.insert_one(serie.to_json())
        return series.find_one({"_id": insert.inserted_id})
    else:
        return serieFind

def insert_image(ds,parent_id,name_file):
    instance_number = convert_value(get_value(ds, ImageD.instance_number_tag, required_or_empty), integer_string)
    patient_orientation = convert_value(get_value(ds, ImageD.patient_orientation_tag, conditionally_required_or_empty), code_string)
    content_date = convert_value(get_value(ds, ImageD.content_date_tag, conditionally_required_or_empty), date)
    content_time = convert_value(get_value(ds, ImageD.content_time_tag, conditionally_required_or_empty), time_)
    image_type = convert_value(get_value(ds, ImageD.image_type_tag, optional), code_string)
    samples_per_pixel = convert_value(get_value(ds, ImageD.samples_per_pixel_tag, conditionally_required_or_empty), unsigned_short)
    photometric_interpretation = convert_value(get_value(ds, ImageD.photometric_interpretation_tag, conditionally_required_or_empty), code_string)
    rows = convert_value(get_value(ds, ImageD.rows_tag, conditionally_required), unsigned_short)
    columns = convert_value(get_value(ds, ImageD.columns_tag, conditionally_required), unsigned_short)
    bits_allocated = convert_value(get_value(ds, ImageD.bits_allocated_tag, conditionally_required), unsigned_short)
    bits_stored = convert_value(get_value(ds, ImageD.bits_stored_tag, conditionally_required), unsigned_short)
    high_bit = convert_value(get_value(ds, ImageD.high_bit_tag, conditionally_required), unsigned_short)
    pixel_representation = convert_value(get_value(ds, ImageD.pixel_representation_tag, conditionally_required), unsigned_short)
    pixel_data = convert_value(get_value(ds, ImageD.pixel_data_tag, conditionally_required), word_string)
    planar_configuration = convert_value(get_value(ds, ImageD.planar_configuration_tag, conditionally_required), unsigned_short)
    pixel_aspect_ratio = convert_value(get_value(ds, ImageD.pixel_aspect_ratio_tag, conditionally_required), unsigned_short)

    image = ImageD(parent_id,instance_number,patient_orientation,content_date,content_time,image_type,samples_per_pixel,
                  photometric_interpretation,rows,columns,bits_allocated,bits_stored,high_bit,pixel_representation,
                  pixel_aspect_ratio,pixel_data,planar_configuration)
    imageFind = images.find_one(image.to_json())
    if imageFind is None:
        insert = images.insert_one(image.to_json())
        if get_value(ds, ImageD.pixel_data_tag, conditionally_required) is not None:
            image_dicom = med2image_dcm(inputFile=name_file,
                                    outputDir=JPG_DIRECTORY,
                                    outputFileStem=str(insert.inserted_id),
                                    outputFileType="jpg",sliceToConvert='0')
            image_dicom.run()
        return images.find_one({"_id": insert.inserted_id})
    else:
        return imageFind

def insert_DICOM(parent_id,name_file,modified=None,user_info=None):

    dicom_file = DICOM(parent_id,name_file,modified,user_info)
    dicom_file_find = dicom_files.find_one({"parent_id":parent_id,"name_file":name_file})
    if dicom_file_find is None:
        insert = dicom_files.insert_one(dicom_file.to_json())
        return dicom_files.find_one({"_id": insert.inserted_id})
    else:
        return dicom_file_find

# Work with model physician #

def find_physician_by_login(login):
    physician = physicians.find_one({"login":login})
    if physician is None:
        return True
    else:
        return False

def find_physician_and_return(login):
    physician = physicians.find_one({"login": login})
    return physician


def update_physician(login,new_password):
    return physicians.find_one_and_update({"login":login},
                                          {"$set": { "password": bcrypt.hashpw(new_password.encode(),bcrypt.gensalt())}},
                                          return_document=ReturnDocument.AFTER)

def insert_physician(full_name,username,password,phone):
    physician = Physician(username,password,phone,full_name)
    insert = physicians.insert_one(physician.to_json())
    return insert.inserted_id

# ========================== #

def find_image_and_delete(_id):
    return images.find_one_and_delete({"_id":_id})

def find_dicom_and_delete_by_filename(filename):
    return dicom_files.find_one_and_delete({"name_file":filename})

# ========================== #

def get_data(collection,filter):
    return collection.find(filter)

def get_patient(filter):
    return get_data(patients,filter)

def get_study(filter):
    return get_data(studies,filter)

def get_serie(filter):
    return get_data(series,filter)

def get_image(filter):
    return get_data(images,filter)

def get_dicom(filter):
    return get_data(dicom_files,filter)

# ========================== #

def process_dicomfile(filename):
    ds = read_file(filename)
    patient_info = insert_patient(ds)
    study_info = insert_study(ds, patient_info["_id"])
    serie_info = insert_series(ds, study_info["_id"])
    image_info = insert_image(ds, serie_info["_id"],filename)
    dicom_info = insert_DICOM(image_info["_id"], filename)

def update_dicomfile(filename_dicom,file_data,modified=None,user_data=None):
    ds = read_file(filename_dicom)

    im = Image.open(io.BytesIO(file_data))

    new_pixel_data = numpy.asarray(im)

    old_pixel_data = ds.get(0x7FE00010)
    old_pixel_data.value = new_pixel_data.tobytes()

    new_file_name = None
    if filename_dicom.index(".") != -1:
        new_file_name = filename_dicom.replace(".","v%s." % (strftime("%d%m%y%H%M", localtime())))
    else:
        new_file_name = filename_dicom + strftime("%d%m%y%H%M", localtime())

    ds.save_as(new_file_name)
    process(new_file_name)

    image = images.find_one({"pixel_data":new_pixel_data.tobytes()})
    im.save(join(JPG_DIRECTORY,str(image["_id"]) + ".jpg"))

    info = ""
    for data in user_data:
        print(data)
        info = info + data["mode"] + "("
        for point in data["data"]:
            info += (str(point) + ",")
        info += "rgba=["
        info += (str(data["color"].red()) + "," + str(data["color"].green()) + "," +
                 str(data["color"].blue()) + "," + str(data["color"].alpha()) + "]")
        info += ")"
        info += ";"
    info = info[:len(info)-1]


    return dicom_files.find_one_and_update({"name_file":new_file_name},
                                 {"$set": { "modified": modified, "user_info": base64.b64encode(info.encode('ascii'))}},
                                return_document=ReturnDocument.AFTER)

def process_dicomdir(filename):
    dicom_dir = read_dicomdir(filename)
    for patient in dicom_dir.patient_records:
        for study in patient.children:
            for serie in study.children:
                for image in serie.children:
                    image_filename = join(dirname(filename), * image.ReferencedFileID)
                    process_dicomfile(image_filename)


def process(filename):
    if not exists(filename):
        logging.error(filename + 'isn\'t exist')
        return None
    if isfile(filename) and filename[filename.rindex("/"):].find("DICOMDIR") != -1:
        process_dicomdir(filename)
    elif isfile(filename) and filename[filename.rindex("."):].find(".dcm") != -1:
        process_dicomfile(filename)
    else:
        logging.error('FileName[' + filename + '] isn\'t correct')

# process(join(dirname(__file__),"Data","dicomdirtests","DICOMDIR"))
# process(join(dirname(__file__),"Data2","korean_agfa_infinitt_2008-3.dcm"))
# edit_image(join(join(JPG_DIRECTORY),"59f5f7b4cb6ab31fa03218e1.jpg"),None)
# update_dicomfile(join(dirname(__file__),"Data2","korean_agfa_infinitt_2008-3.dcm"),join(join(JPG_DIRECTORY),"59f5f7b4cb6ab31fa03218e1v1.jpg"))