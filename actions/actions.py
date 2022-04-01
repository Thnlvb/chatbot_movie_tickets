from types import DynamicClassAttribute
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import feedparser
import mysql.connector
import re
import datetime
from datetime import timedelta
import json
from rasa_sdk.events import SlotSet
from connect import DataUpdate

class Tl_phim_co_khong(Action):
    def name(self) -> Text:
        return "Tl_phim_co_khong"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        mv_name = tracker.get_slot("movie_name")  
        print(mv_name)      
        # Lấy nội dung entity từ câu truy vấn
        myconn = mysql.connector.connect(host = "localhost", user = "root", passwd = "", database="nienluan")
        moive_db = myconn.cursor()
        codeOfMovie = "SELECT category_name FROM tbl_category_movie WHERE category_name LIKE '{}'".format(mv_name)
        moive_db.execute(codeOfMovie)
        result = moive_db.fetchall()
        print(result)
        if (result == []):
            dispatcher.utter_message("Hiện không có phim này") 
        else:
            dispatcher.utter_message("Hiện rạp đang có phim này")
        myconn.rollback()
        myconn.close()
        return []

class Tl_phim_hom_nay(Action):
    def name(self) -> Text:
        return "Tl_phim_hom_nay"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        myconn = mysql.connector.connect(host = "localhost", user = "root", passwd = "", database="nienluan")
        mv_db = myconn.cursor()
        # yesterday.strftime('%m%d%y')
        #print(yesterday.strftime('%m'))
        today1 = datetime.datetime.now().date() 
        search = "SELECT DISTINCT category_name FROM tbl_category_movie WHERE category_id IN (SELECT schedule_movie FROM tbl_movie_schedule WHERE schedule_times IN (SELECT times_id FROM tbl_times WHERE day_times LIKE '{}'))".format(today1)
        mv_db.execute(search)
        result = mv_db.fetchall()
        if (result == []):
            dispatcher.utter_message("Hôm nay không có lịch chiếu")
        else:
            for x in result:
                dispatcher.utter_message(x[0])
        myconn.rollback()
        myconn.close()
        return []

class Tl_phim_ngay_mai(Action):
    def name(self) -> Text:
        return "Tl_phim_ngay_mai"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        myconn = mysql.connector.connect(host = "localhost", user = "root", passwd = "", database="nienluan")
        mv_db = myconn.cursor()
        # tomorrow = tracker.get_slot("tomorrow")
        tomorrow1 = datetime.datetime.now() + datetime.timedelta(days = 1)
        search = "SELECT DISTINCT category_name FROM tbl_category_movie WHERE category_id IN (SELECT schedule_movie FROM tbl_movie_schedule WHERE schedule_times IN (SELECT times_id FROM tbl_times WHERE day_times LIKE '{}'))".format(tomorrow1.date())
        mv_db.execute(search)
        result = mv_db.fetchall()
        if (result == []):
            dispatcher.utter_message("Ngày mai không có lịch chiếu")
        else:
            for x in result:
                    dispatcher.utter_message(x[0])
        myconn.rollback()
        myconn.close()
        return []

class Tl_phim_ngay_bat_ki(Action):
    def name(self) -> Text:
        return "Tl_phim_ngay_bat_ki"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        myconn = mysql.connector.connect(host = "localhost", user = "root", passwd = "", database="nienluan")
        mv_db = myconn.cursor()
        day = tracker.get_slot("day")
        search = "SELECT DISTINCT category_name FROM tbl_category_movie WHERE category_id IN (SELECT schedule_movie FROM tbl_movie_schedule WHERE schedule_times IN (SELECT times_id FROM tbl_times WHERE day_times LIKE '{}'))".format(day)
        mv_db.execute(search)
        result = mv_db.fetchall()
        for x in result:
            dispatcher.utter_message(x[0])
        myconn.rollback()
        myconn.close()
        return [] 

class Liet_ke_suat_chieu(Action):
    def name(self) -> Text:
        return "Liet_ke_suat_chieu"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:      
        myconn = mysql.connector.connect(host = "localhost", user = "root", passwd = "", database="nienluan")
        mv_db = myconn.cursor()
        mv_name = tracker.get_slot("movie_name")  
        search = "SELECT start_times, day_times FROM tbl_times WHERE times_id IN (SELECT schedule_times FROM tbl_movie_schedule WHERE schedule_movie IN (SELECT category_id FROM tbl_category_movie WHERE category_name LIKE '{}'))".format(mv_name)
        mv_db.execute(search)
        result = mv_db.fetchall()
        if (result == []):
            dispatcher.utter_message("Phim " + mv_name + " hiện không có lịch chiếu.")
        else:
            dispatcher.utter_message("Phim " + mv_name + " có những suất chiếu:")
            for x in result:
                #c = x[0].strftime('%M:%H')
                hour = datetime.datetime.strftime(datetime.datetime.strptime(str(x[0]), "%H:%M:%S"), "%H:%M")
                date = datetime.datetime.strftime(datetime.datetime.strptime(str(x[1]), "%Y-%m-%d"), "%d/%m/%Y")
                #dispatcher.utter_message("Phim " + mv_name + " có những xuất chiếu: " + x[0])
                #dispatcher.utter_message(a)
                dispatcher.utter_message("Ngày " + date + " lúc "+ hour)
        myconn.rollback()
        myconn.close()
        return []

class Tl_poster(Action):
    def name(self) -> Text:
        return "Tl_poster"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:      
        myconn = mysql.connector.connect(host = "localhost", user = "root", passwd = "", database="nienluan")
        mv_db = myconn.cursor()
        mv_name = tracker.get_slot("movie_name")  
        search = "SELECT category_img FROM tbl_category_movie WHERE category_name LIKE '{}'".format(mv_name)
        mv_db.execute(search)
        result = mv_db.fetchall()
        dispatcher.utter_message("Dưới đây là poster phim " + mv_name)
        for x in result:
            dispatcher.utter_message(image = "/nien_luan/public/upload/movie/{}".format(x[0]))
        myconn.rollback()
        myconn.close()
        return []

class Chon_loai_phim(Action):
    def name(self) -> Text:
        return "Chon_loai_phim"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:      
        buttons = [
            {"title":"Hành Động", "payload":'/hd{"content_type":"hd"}'},
            {"title":"Nhạc Kịch", "payload":'/nk{"content_type":"nk"}'},
            {"title":"Kinh Dị", "payload":'/kd{"content_type":"kd"}'},
            {"title":"Phiêu Lưu","payload":'/pl{"content_type":"pl"}'},
            {"title":"Gia Đình", "payload":'/gd{"content_type":"gd"}'},
            {"title":"Hài", "payload":'/h{"content_type":"h"}'},
            {"title":"Hoạt Hình", "payload":'/hh{"content_type":"hh"}'},
            {"title":"Tâm Lý", "payload":'/tl{"content_type":"tl"}'},
            {"title":"Tình Cảm", "payload":'/tc{"content_type":"tc"}'},
            {"title":"Hồi Hợp", "payload":'/hoh{"content_type":"hoh"}'},
            {"title":"Lịch Sử", "payload":'/ls{"content_type":"ls"}'},
            {"title":"Thần Thoại", "payload":'/tt{"content_type":"tt"}'}
        ]
        dispatcher.utter_message("Vui lòng chọn loại phim", buttons= buttons)
        return []

class Nhap_ten_phim(Action):
    def name(self) -> Text:
        return "Nhap_ten_phim"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        text = tracker.latest_message['text']
        return [SlotSet("nhaptenphim", text)]

class Chon_suat_chieu(Action):
    def name(self) -> Text:
        return "Chon_suat_chieu"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:      
        myconn = mysql.connector.connect(host = "localhost", user = "root", passwd = "", database="nienluan")
        mv_db = myconn.cursor()
        mv_name = tracker.get_slot("nhaptenphim")  
        search = "SELECT start_times, day_times FROM tbl_times WHERE times_id IN (SELECT schedule_times FROM tbl_movie_schedule WHERE schedule_movie IN (SELECT category_id FROM tbl_category_movie WHERE category_name LIKE '{}'))".format(mv_name)
        mv_db.execute(search)
        result = mv_db.fetchall()
        dispatcher.utter_message("Vui lòng nhập giờ chiếu bạn chọn.")
        dispatcher.utter_message("Phim " + mv_name + " có những suất chiếu:")
        for x in result:
            hour = datetime.datetime.strftime(datetime.datetime.strptime(str(x[0]), "%H:%M:%S"), "%H:%M")
            date = datetime.datetime.strftime(datetime.datetime.strptime(str(x[1]), "%Y-%m-%d"), "%d/%m/%Y")
            dispatcher.utter_message("Ngày " + date + " lúc "+ hour)
        myconn.rollback()
        myconn.close()
        return []

class Chon_ghe(Action):
    def name(self) -> Text:
        return "Chon_ghe"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:      
        myconn = mysql.connector.connect(host = "localhost", user = "root", passwd = "", database="nienluan")
        mv_db = myconn.cursor()
        mv = tracker.get_slot("nhaptenphim")
        time = tracker.get_slot("nhapsuatchieu")
        search = "SELECT chair_name FROM tbl_chair WHERE chair_status = 1 AND chair_theater IN (SELECT schedule_theater FROM tbl_movie_schedule WHERE schedule_times IN (SELECT times_id FROM tbl_times WHERE start_times = '{}' AND (SELECT category_id FROM tbl_category_movie WHERE category_name = '{}')))".format(time, mv)
        mv_db.execute(search)
        result = mv_db.fetchall()
        dispatcher.utter_message("Vui lòng nhập tên ghế bạn chọn.")
        dispatcher.utter_message("Phim " + mv + " suất chiếu lúc " + time + " còn những ghế trống sau: ")
        for x in result:
            dispatcher.utter_message(x[0])
        myconn.rollback()
        myconn.close()
        return []

class Nhap_ghe(Action):
    def name(self) -> Text:
        return "Nhap_ghe"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        text = tracker.latest_message['text']
        print(text)
        return [SlotSet("nhapghe", text)]

class Nhap_suat_chieu(Action):
    def name(self) -> Text:
        return "Nhap_suat_chieu"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        text = tracker.latest_message['text']
        print(text)
        return [SlotSet("nhapsuatchieu", text)]

class Submit(Action): 
    def name(self) -> Text:
        return "Submit"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        DataUpdate(tracker.get_slot("nhaptenphim"), tracker.get_slot("nhapsuatchieu"), tracker.get_slot("nhapghe")) 
        dispatcher.utter_message("Cảm ơn bạn đã đặt vé!") 
        return []

class Xemlaive(Action): 
    def name(self) -> Text:
        return "Xemlaive"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        myconn = mysql.connector.connect(host = "localhost", user = "root", passwd = "", database="nienluan")
        mv_db = myconn.cursor()
        search = "SELECT * FROM tbl_bottickets WHERE bottickets_id = (SELECT MAX(bottickets_id) FROM tbl_bottickets)"
        mv_db.execute(search)
        result = mv_db.fetchall()
        for x in result:
            print(x[1])             
            print(x[2])             
            print(x[3])           
        dispatcher.utter_message("Thông tin vé của bạn đặt là:  \n\nTên phim: {}  \n\nSuất chiếu: {} \n\nSố ghế: {}".format(x[1], x[2], x[3]))
        myconn.rollback()
        myconn.close()
        return []
