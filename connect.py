import mysql.connector

def DataUpdate(bottickets_movie, bottickets_time, bottickets_chair): 
	mydb = mysql.connector.connect(host = "localhost", user = "root", passwd = "", database = "nienluan")
	mycursor = mydb.cursor()
	# now = datetime.datetime.now()
	sql='INSERT INTO tbl_bottickets (bottickets_movie, bottickets_time, bottickets_chair) VALUES ("{0}","Ngày 09/11/2021 lúc {1}","{2}");'.format(bottickets_movie, bottickets_time, bottickets_chair)
	mycursor.execute(sql)
	mydb.commit()

# if __name__=="__main__":
# 	DataUpdate("Trạng Tí", "Ngày 09/11/2021 lúc 20:20", "P1A1")