#!python
# -*- coding: utf-8 -*-

import logging

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from window.designer import *
import window.designer2 as sign_up
import window.designer3 as forget
from window.designer4 import *
import window.designer5 as del_window
import window.designer6 as storage_window
import window.designer7 as image_storage_window
import window.designer8 as about_window
import window.designer9 as search_window

from window.modelQt import CustomModel

from mongo import *
from util.sms import *

import bcrypt
import threading
from functools import partial
import copy
import sys
import json

current_user = None

def merge_two_dicts(x, y):
    z = copy.deepcopy(x)
    z.update(y)
    return z

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.sign_in_button.clicked.connect(self.sign_in)
        clickable(self.sign_up_label).connect(self.sign_up)
        clickable(self.forgot_password_label).connect(self.forget_password)
        self.app_window = None
        self.sign_up_window = None
        self.forget_password_window = None

    def sign_in(self):
        global current_user
        username = self.username_edit.text()
        password = self.password_edit.text()

        physician = find_physician_and_return(username)
        if physician is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(
                "User with this username doesn't exist")
            msg.setWindowTitle("No user found")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        elif not bcrypt.checkpw(password.encode(),physician["password"]):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(
                "Invalid login/password")
            msg.setWindowTitle("Invalid user")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            current_user = physician
            if self.app_window is None:
                self.app_window = AppWindow()
            self.app_window.show()
            self.close()


    def sign_up(self):
        if self.sign_up_window is None:
            self.sign_up_window = Sign_Up_Window()
        self.sign_up_window.show()
        self.close()

    def forget_password(self):
        if self.forget_password_window is None:
            self.forget_password_window= Forget_Password_Window()
        self.forget_password_window.show()
        self.close()

class Sign_Up_Window(QtGui.QMainWindow, sign_up.Ui_Form):
    def __init__(self, parent=None):
        super(Sign_Up_Window, self).__init__(parent)
        self.setupUi(self)

        self.sign_in_button.clicked.connect(self.verify)
        self.confirm_button.clicked.connect(self.check_otp)

        self.app_window = None

    def verify(self):
        full_name = self.full_name_edit.text()
        username = self.username_edit.text()
        password = self.password_edit.text()
        phone = self.phone_edit.text()

        if len(full_name.split("^")) == 1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)

            msg.setText("Full name of doctor contains symbol '^' between surname and first name, because of format DICOM")
            msg.setWindowTitle("Error validation")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        elif username is None or len(username) < 6 or len(username) > 60:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(
                "Username must contains between 6 and 60 characters")
            msg.setWindowTitle("Error validation")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        elif password is None or len(password) < 7 or len(password) > 60:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(
                "Password must contains between 7 and 60 characters")
            msg.setWindowTitle("Error validation")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        elif len(phone) != 16:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(
                "Invalid phone")
            msg.setWindowTitle("Error validation")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        elif not find_physician_by_login(username):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(
                "User with this username already exists")
            msg.setWindowTitle("Not unique username")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        else:

            self.phone_edit_2.setEnabled(True)
            self.confirm_button.setEnabled(True)

            self.full_name_edit.setEnabled(False)
            self.username_edit.setEnabled(False)
            self.password_edit.setEnabled(False)
            self.phone_edit.setEnabled(False)

            phone = phone.replace("(","").replace(")","").replace("-","")


            if not send_otp(phone,"Confirmation code for creating new doctor " + full_name + ": "):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(
                    "Confirmation code was generated lately. Please wait a minute for generating new code")
                msg.setWindowTitle("Too many requests")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()

    def check_otp(self):
        global current_user
        otp_password = self.phone_edit_2.text()
        if otp_password is None or not check_otp(otp_password):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Error password")
            msg.setWindowTitle("Error confirmation password")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            full_name = self.full_name_edit.text()
            username = self.username_edit.text()
            password = self.password_edit.text()
            phone = self.phone_edit.text()

            insert_physician(full_name,username,password,phone)
            physician = find_physician_and_return(username)
            current_user = physician

            if self.app_window is None:
                self.app_window = AppWindow()
            self.app_window.show()
            self.close()


class Forget_Password_Window(QtGui.QMainWindow, forget.Ui_Form):
    def __init__(self, parent=None):
        super(Forget_Password_Window, self).__init__(parent)
        self.setupUi(self)

        self.otp_button.clicked.connect(self.verify_and_get_otp)
        self.confirm_button.clicked.connect(self.check_otp)
        self.change_button.clicked.connect(self.change_password)

        self.main_window = None

    def verify_and_get_otp(self):
        username = self.username_edit.text()

        if username is None or len(username) < 6 or len(username) > 60:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(
                "Username must contains between 6 and 60 characters")
            msg.setWindowTitle("Error validation")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        elif find_physician_by_login(username):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(
                "User with this username doesn't exist")
            msg.setWindowTitle("No user found")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            self.otp_password_edit.setEnabled(True)
            self.confirm_button.setEnabled(True)

            physician = find_physician_and_return(username)
            phone = physician["phone"]

            if not send_otp(phone, "Confirmation code for restoring password:"):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(
                    "Confirmation code was generated lately. Please wait a minute for generating new code")
                msg.setWindowTitle("Too many requests")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()

    def check_otp(self):
        otp_password = self.otp_password_edit.text()
        if otp_password is None or not check_otp(otp_password):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Error password")
            msg.setWindowTitle("Error confirmation password")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            self.new_password_edit.setEnabled(True)
            self.repeat_new_password_edit.setEnabled(True)
            self.change_button.setEnabled(True)

            self.username_edit.setEnabled(False)
            self.otp_password_edit.setEnabled(False)
            self.confirm_button.setEnabled(False)
            self.otp_button.setEnabled(False)

    def change_password(self):
        global current_user
        new_password = self.new_password_edit.text()
        repeat_new_password = self.repeat_new_password_edit.text()

        if new_password is None or len(new_password) < 7 or len(new_password) > 60:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(
                "Password must contains between 7 and 60 characters")
            msg.setWindowTitle("Error validation")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        elif new_password != repeat_new_password:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(
                "Passwords don't match")
            msg.setWindowTitle("Error validation")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            result = update_physician(self.username_edit.text(),self.new_password_edit.text())
            current_user = result
            if result is not None:
                if self.main_window is None:
                    self.main_window = MainWindow()
                self.main_window.show()
                self.close()
            else:
                logging.error("Some errors")

class AppWindow(QtGui.QMainWindow, Ui_AppWindow):

    def __init__(self, parent=None):
        global current_user
        super(AppWindow, self).__init__(parent)
        self.setupUi(self)

        patient_keys = ["_id","patient_name","patient_id","patient_birth","patient_sex"]
        study_keys = ["_id","parent_id","study_instance_uid","study_id","study_date","study_time","accession_number",
                 "study_description","institution_name","referring_physician_name"]
        serie_keys = ["_id","parent_id","serie_instance_uid","series_description","serie_number","modality","series_date",
                 "series_time","protocol_name","laterality","body_part_thickness","compression_force","body_part_examined","view_position"]
        image_keys = ["_id","parent_id", "instance_number","patient_orientation","content_date","content_time","image_type",
                 "samples_per_pixel","photometric_interpretation","rows","columns","bits_allocated","bits_stored","high_bit",
                 "pixel_representation","pixel_aspect_ratio","planar_configuration"]

        image_keys_edit = ["_id","name_file", "modified", "user_info"]

        dicom_keys = ["_id","parent_id","name_file","modified","user_info"]

        self.patient_model = CustomModel(patient_keys,self.patientTable)
        self.study_model = CustomModel(study_keys,self.studyTable)
        self.serie_model = CustomModel(serie_keys,self.serieTable)
        self.image_model = CustomModel(image_keys,self.imageTable)
        self.image_edit_model = CustomModel(image_keys_edit, self.imageTable2)
        self.dicom_model = CustomModel(dicom_keys,self.dicomTable)
        self.patientTable.setModel(self.patient_model)
        self.studyTable.setModel(self.study_model)
        self.serieTable.setModel(self.serie_model)
        self.imageTable.setModel(self.image_model)
        self.imageTable2.setModel(self.image_edit_model)
        self.imageTable2.setSelectionBehavior(QTableView.SelectRows)
        self.imageTable2.clicked.connect(self.load_image)
        self.dicomTable.setModel(self.dicom_model)

        self.color = None
        self.paint_mode = 0

        self.point_button.clicked.connect(partial(self.choose_color,"point"))
        self.line_button.clicked.connect(partial(self.choose_color,"line"))
        self.polyline_button.clicked.connect(partial(self.choose_color,"polyline"))
        self.polygon_button.clicked.connect(partial(self.choose_color,"polygon"))

        self.graphicsView.mousePressEvent = self.paint

        self.points = []
        self._points = []
        self.last_index = 0
        self.last_mode = None

        self.undo_button.clicked.connect(self.undo_data)
        self.redo_button.clicked.connect(self.redo_data)
        self.save_button.clicked.connect(self.save_data)

        self.pixmap_original = None
        self.file = None

        self.actionAdd_dicom.triggered.connect(self.add_dicom)
        self.actionAdd_dicom_dir_DICOMDIR.triggered.connect(self.add_dicomdir)
        self.actionDelete_dicom_file.triggered.connect(self.delete_dicom)
        self.actionQuery.triggered.connect(partial(self.search,False))
        self.actionQuery_For_Advanced_User.triggered.connect(partial(self.search,True))
        self.actionStorage.triggered.connect(self.storage_url)
        self.actionImage_Storage.triggered.connect(self.image_storage_url)
        self.actionAbout_app.triggered.connect(self.about_app)

        lock = threading.Lock()
        with lock:
            self.update_table()


    def update_table(self):
        self.dicom_model.datatable = []
        self.image_edit_model.datatable = []
        self.image_model.datatable = []
        self.study_model.datatable = []
        self.serie_model.datatable = []
        self.patient_model.datatable = []

        dicom_files_db = get_dicom({"modified": {"$in": [current_user["_id"], None]}})
        image_list = []
        serie_list = []
        study_list = []
        patient_list = []

        for dicom_file in dicom_files_db:
            self.dicom_model.datatable.append(dicom_file)
            self.image_edit_model.datatable.append(dicom_file)
            image_list.append(dicom_file["parent_id"])

        images_db = get_image({"_id": {"$in": image_list}})
        for image in images_db:
            self.image_model.datatable.append(image)
            serie_list.append(image["parent_id"])

        series_db = get_serie({"_id": {"$in": serie_list}})
        for serie in series_db:
            self.serie_model.datatable.append(serie)
            study_list.append(serie["parent_id"])

        study_db = get_study({"_id": {"$in": study_list}})
        for study in study_db:
            self.study_model.datatable.append(study)
            patient_list.append(study["parent_id"])

        patients_db = get_patient({"_id": {"$in": patient_list}})
        for patient in patients_db:
            self.patient_model.datatable.append(patient)

        self.patientTable.model().layoutChanged.emit()
        self.studyTable.model().layoutChanged.emit()
        self.serieTable.model().layoutChanged.emit()
        self.imageTable.model().layoutChanged.emit()
        self.imageTable2.model().layoutChanged.emit()
        self.dicomTable.model().layoutChanged.emit()



    def load_image(self,clicked_index):
        row = clicked_index.row()
        model = clicked_index.model()

        image_file = join(JPG_DIRECTORY,str(model.datatable[row]['parent_id']) + ".jpg")
        self.file = str(model.datatable[row]['name_file'])
        pixmap = QPixmap(image_file)


        self.graphicsView.setPixmap(pixmap.scaled(self.graphicsView.size(), QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))
        self.pixmap_original = pixmap.scaled(self.graphicsView.size(), QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation)

    def choose_color(self,mode):
        self.color = QtGui.QColorDialog.getColor()
        if mode == "point":
            self.paint_mode = 1
        elif mode == "line":
            self.paint_mode = 2
        elif mode == "polyline":
            self.paint_mode = 3
        elif mode == "polygon":
            self.paint_mode = 4

    def update_pixmap(self):
        pixmap = QPixmap(self.pixmap_original)
        painter = QPainter(pixmap)

        for info in self.points:
            painter.setPen(info["color"])
            if info["mode"]=="point":
                painter.drawPoint(*tuple(info["data"]))
            elif info["mode"]=="line":
                if len(info["data"])==4:
                    painter.drawLine(*tuple(info["data"]))
            elif info["mode"]=="polyline":
                painter.drawPolyline(QPolygon(info["data"]))
            elif info["mode"]=="polygon":
                painter.drawPolygon(QPolygon(info["data"]))

        painter.end()

        self.graphicsView.setPixmap(pixmap)



    def paint(self, event):

        if event is not None:
            x = event.pos().x()
            y = event.pos().y()

            if self.paint_mode == 1:
                if self.last_mode is not None and (self.last_mode == "polygon" or self.last_mode == "polyline"):
                    self.last_index += 1
                info = dict()
                info["mode"]="point"
                info["data"]=[x,y]
                info["color"] = self.color
                self.points.append(info)
                self.last_index += 1
                self.last_mode = "point"
            elif self.paint_mode == 2:
                if self.last_mode is not None and (self.last_mode == "polygon" or self.last_mode == "polyline"):
                    self.last_index += 1
                if self.last_index >= len(self.points):
                    info = dict()
                    info["mode"]="line"
                    info["data"]=[x,y]
                    info["color"] = self.color
                    self.points.append(info)
                else:
                    self.points[self.last_index]["data"].extend((x,y))
                    self.last_index += 1
                self.last_mode = "line"
            elif self.paint_mode == 3:
                if self.last_mode is not None and self.last_mode == "polygon":
                    self.last_index += 1
                if self.last_index >= len(self.points):
                    info = dict()
                    info["mode"] = "polyline"
                    info["data"] = [x, y]
                    info["color"] = self.color
                    self.points.append(info)
                else:
                    self.points[self.last_index]["data"].extend((x,y))
                self.last_mode = "polyline"
            elif self.paint_mode == 4:
                if self.last_mode is not None and self.last_mode == "polyline":
                    self.last_index += 1
                if self.last_index >= len(self.points):
                    info = dict()
                    info["mode"] = "polygon"
                    info["data"] = [x, y]
                    info["color"] = self.color
                    self.points.append(info)
                else:
                    self.points[self.last_index]["data"].extend((x,y))
                self.last_mode = "polygon"

        self.update_pixmap()
        self._points = copy.deepcopy(self.points)

    def undo_data(self):
        if len(self.points)> 0 and (self.last_mode != 'polygon' and self.last_mode != 'polyline') and (self.points[self.last_index-1]["mode"]=='line' or self.points[self.last_index-1]["mode"] == 'point'):
            self.points.pop()
            self.last_index -= 1
        elif len(self.points) > 0:
            if len(self.points[self.last_index]["data"]) > 4:
                self.points[self.last_index]["data"].pop()
                self.points[self.last_index]["data"].pop()
            else:
                self.points.pop()
                self.last_index -= 1
        self.update_pixmap()

    def redo_data(self):
        if self._points is not None and len(self._points)>len(self.points):
            self.points.append(self._points[self.last_index])
            self.last_index += 1
        else:
            self.points[self.last_index]["data"].append(self._points[self.last_index]["data"][-2])
            self.points[self.last_index]["data"].append(self._points[self.last_index]["data"][-1])
        self.update_pixmap()

    def save_data(self):
        global current_user
        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        buffer.open(QIODevice.WriteOnly)
        pixmap = self.graphicsView.pixmap()
        pixmap.save(buffer,"jpg")

        update_dicomfile(self.file,byte_array,current_user["_id"],self.points)

    def add_dicom(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', dirname(__file__),"Dicom file (*.dcm)")

        try:
            if filename is not None and filename != "":
                process(filename)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(
                    "Successfully add DICOM [" + filename + "]" + "to MongoDB")
                msg.setWindowTitle("MongoDB_Add")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                self.update_table()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(
                "Unsuccessfully add DICOM [" + filename + "]" + "to MongoDB. Cause: " + str(sys.exc_info()[0]))
            msg.setWindowTitle("MongoDB_Add")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()



    def add_dicomdir(self):
        filename = QFileDialog.getOpenFileName(self, 'Open dir', dirname(__file__),"Dicom dir (DICOMDIR)")

        try:
            if filename is not None and filename != "":
                process(filename)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(
                    "Successfully add DICOMDIR [" + filename + "]" + " to MongoDB")
                msg.setWindowTitle("MongoDB_Add")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                self.update_table()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(
                "Unsuccessfully add DICOMDIR [" + filename + "]" + " to MongoDB. Cause: " + str(sys.exc_info()[0]))
            msg.setWindowTitle("MongoDB_Add")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def delete_dicom(self):
        self.delete_window = Delete_Window(self)
        self.delete_window.show()

    def storage_url(self):
        self.storage_window = Storage_Window(self)
        self.storage_window.show()

    def image_storage_url(self):
        self.image_storage_window = Image_Storage_Window()
        self.image_storage_window.show()

    def about_app(self):
        self.about_app_window = About_Window()
        self.about_app_window.show()

    def search(self,isAdvanced):
        self.search_window = Search_Window(isAdvanced=isAdvanced)
        self.search_window.show()


class Delete_Window(QtGui.QMainWindow, del_window.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Delete_Window, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent

        self.confirm_button.clicked.connect(self.delete_file)

        dicom_files_db = get_dicom({"modified": {"$in": [current_user["_id"], None]}})
        for dicom_file in dicom_files_db:
            self.comboBox.addItem(dicom_file["name_file"])


    def delete_file(self):
        try:
            deleted_dicom = find_dicom_and_delete_by_filename(self.comboBox.currentText())
            deleted_image = find_image_and_delete(deleted_dicom["parent_id"])

            if isfile(join(JPG_DIRECTORY,str(deleted_image["_id"])+".jpg")):
                os.remove(join(JPG_DIRECTORY,str(deleted_image["_id"])+".jpg"))

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(
                "Successfully delete DICOM [" + deleted_dicom["name_file"] + "]" + " from MongoDB")
            msg.setWindowTitle("MongoDB_Delete")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

            self.parent.update_table()

            self.close()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(
                "Unsuccessfully delete DICOM [" + self.comboBox.currentText() + "]" + " from MongoDB. Cause: " + str(sys.exc_info()[0]))
            msg.setWindowTitle("MongoDB_Delete")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

class Storage_Window(QtGui.QMainWindow, storage_window.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Storage_Window, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent

        self.url_edit.setText(MONGO_DB_URL)

        self.check_button.clicked.connect(self.check_url)
        self.confirm_button.clicked.connect(self.change_url)


    def check_url(self):
        try:
            check_client = MongoClient(self.url_edit.text(),serverSelectionTimeoutMS=10000)
            check_client.server_info()

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(
                "You can change URL")
            msg.setWindowTitle("MongoDB_ChangeURL")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return True

        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(
                "You can't change URL. Cause: " + str(sys.exc_info()[0]))
            msg.setWindowTitle("MongoDB_ChangeURL")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return False

    def change_url(self):
        global MONGO_DB_URL
        global client
        global db
        global patients
        global studies
        global series
        global images
        global physicians
        global dicom_files

        if self.check_url():

            MONGO_DB_URL = self.url_edit.text()
            client = MongoClient()
            db = client['DICOM']

            patients = db['patient']
            studies = db['study']
            series = db['serie']
            images = db['image']
            physicians = db['physician']
            dicom_files = db['dicom']

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(
                "Success change URL to " + MONGO_DB_URL)
            msg.setWindowTitle("MongoDB_ChangeURL")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

            self.parent.update_table()

            self.close()

class Image_Storage_Window(QtGui.QMainWindow, image_storage_window.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Image_Storage_Window, self).__init__(parent)
        self.setupUi(self)

        self.url_edit.setText(JPG_DIRECTORY)

        self.choose_button.clicked.connect(self.choose_dir)
        self.confirm_button.clicked.connect(self.change_dir)


    def choose_dir(self):
        filename = QFileDialog.getExistingDirectory(self, 'Select a directory', JPG_DIRECTORY)
        self.url_edit.setText(filename)

    def change_dir(self):
        global JPG_DIRECTORY

        JPG_DIRECTORY = self.url_edit.text()

        self.close()

class About_Window(QtGui.QMainWindow, about_window.Ui_MainWindow):
    def __init__(self, parent=None):
        super(About_Window, self).__init__(parent)
        self.setupUi(self)

class Search_Window(QtGui.QMainWindow, search_window.Ui_AppWindow):
    def __init__(self, parent=None,isAdvanced=False):
        super(Search_Window, self).__init__(parent)
        self.setupUi(self)

        self.isAdvanced = isAdvanced

        self.advanced_condition_edit.setEnabled(isAdvanced)
        self.search_button.clicked.connect(self.search)


    def search(self):
        patient_keys = ["patient_name", "patient_id", "patient_birth", "patient_sex"]
        study_keys = ["study_instance_uid", "study_id", "study_date", "study_time",
                      "accession_number",
                      "study_description", "institution_name", "referring_physician_name"]
        serie_keys = ["serie_instance_uid", "series_description", "serie_number", "modality",
                      "series_date",
                      "series_time", "protocol_name", "laterality", "body_part_thickness", "compression_force",
                      "body_part_examined", "view_position"]
        image_keys = ["instance_number", "patient_orientation", "content_date", "content_time",
                      "image_type",
                      "samples_per_pixel", "photometric_interpretation", "rows", "columns", "bits_allocated",
                      "bits_stored", "high_bit",
                      "pixel_representation", "pixel_aspect_ratio", "planar_configuration"]
        dicom_keys = ["name_file", "modified", "user_info"]

        result_keys = []

        if self.patientBox.isChecked() == True:
            result_keys.extend(patient_keys)
        if self.studyBox.isChecked() == True:
            result_keys.extend(study_keys)
        if self.serieBox.isChecked() == True:
            result_keys.extend(serie_keys)
        if self.imageBox.isChecked() == True:
            result_keys.extend(image_keys)
        if self.dicomBox.isChecked() == True:
            result_keys.extend(dicom_keys)

        self.search_model = CustomModel(result_keys, self.result_table)
        self.result_table.setModel(self.search_model)

        self.search_model.datatable = []

        patient_filter = dict()
        study_filter = dict()
        serie_filter = dict()
        image_filter = dict()
        dicom_filter = dict()

        user_filter_str = self.advanced_condition_edit.toPlainText()
        user_filter = dict()

        if self.patient_gender_edit.text() is not None and self.patient_gender_edit.text() != "":
            patient_filter = merge_two_dicts(patient_filter,{"patient_id" : self.patient_gender_edit.text()})
        if self.patientGender_box.currentText() != "All":
            patient_filter = merge_two_dicts(patient_filter,{"patient_sex": self.patientGender_box.currentText()})
        if self.physician_edit.text() is not None and self.physician_edit.text() != "":
            study_filter = merge_two_dicts(study_filter,{"referring_physician_name": self.physician_edit.text()})
        if self.instituition_name_edit.text() is not None and self.instituition_name_edit.text() != "":
            study_filter = merge_two_dicts(study_filter,{"institution_name": self.instituition_name_edit.text()})
        if self.modality_box.currentText() != "All":
            serie_filter = merge_two_dicts(serie_filter,{"modality": self.modality_box.currentText().encode()})
        if self.image_date_edit.date().toPyDate() != datetime.date(2000,1,1):
            image_filter = merge_two_dicts(image_filter,{"content_date": self.image_date_edit.date().toPyDate()})

        if self.isAdvanced:
            try:
                user_filter = json.loads(user_filter_str)
            except:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(
                    "Not valid BSON for filter")
                msg.setWindowTitle("MongoDB_Search")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()

            for key, value in user_filter.items():
                if key in patient_keys:
                    patient_filter = merge_two_dicts(patient_filter,{key: value})
                elif key in study_keys:
                    study_filter = merge_two_dicts(study_filter,{key:value})
                elif key in serie_keys:
                    serie_filter = merge_two_dicts(serie_filter,{key:value})
                elif key in image_keys:
                    image_filter = merge_two_dicts(image_filter,{key:value})
                elif key in dicom_keys:
                    dicom_filter = merge_two_dicts(dicom_filter,{key:value})


        dicom_files_db = get_dicom(merge_two_dicts({"modified": {"$in": [current_user["_id"], None]}},dicom_filter))

        for dicom_file in dicom_files_db:

            images_db = get_image(merge_two_dicts(image_filter,{"_id": dicom_file["parent_id"]}))
            for image in images_db:
                series_db = get_serie(merge_two_dicts(serie_filter,{"_id": image["parent_id"]}))
                for serie in series_db:
                    study_db = get_study(merge_two_dicts(study_filter,{"_id": serie["parent_id"]}))
                    for study in study_db:
                        patients_db = get_patient(merge_two_dicts(patient_filter,{"_id": study["parent_id"]}))
                        for patient in patients_db:
                            result = dicom_file
                            result = merge_two_dicts(result,image)
                            result = merge_two_dicts(result,serie)
                            result = merge_two_dicts(result,study)
                            result = merge_two_dicts(result,patient)
                            self.search_model.datatable.append(result)

        self.result_table.model().layoutChanged.emit()



