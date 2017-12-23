#The Execution File for Pictures Identification

# coding=utf-8
# 要加上面這行才可在程式碼裡面打中文，包含註解也是，要不然會出錯
# 按S鍵照相程式
# 還有點小bug

import tensorflow as tf
import sys
import time
import cv2
import os
#arduino用函式庫
#import signal
#from PyMata.pymata import PyMata

# Digital pin 13 is connected to an LED. If you are running this script with
# an Arduino UNO no LED is needed (Pin 13 is connected to an internal LED).
#BOARD_LED = 13


# Create a PyMata instance
#board = PyMata("COM3", verbose=True) #定義板子跟阜 #開啟前先看好

#signal.signal(signal.SIGINT, signal_handler)
#board.set_pin_mode(BOARD_LED, board.OUTPUT, board.DIGITAL)
#time.sleep(2)

#資料庫連接
import pymysql.cursors
connection = pymysql.connect(host='localhost',
							 user='root',
							 password='',
							 db='plant_system',
							 charset='utf8',
							 cursorclass=pymysql.cursors.DictCursor)
							 
cursor = connection.cursor()
print('')
print('connection start')

# webcam拍照存檔
video_capture = cv2.VideoCapture(0) #改變括號內數字可選擇webcam

i = 0;
while True:
	ret, frame = video_capture.read()
	cv2.imshow('Video', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'): #按q退出
		
		connection.close()	#關閉連線
		print('')
		print('connection finish')
		break;				#跳出迴圈
		
	elif cv2.waitKey(1) & 0xFF == ord('s'): #按s存檔
		i = i + 1;
		photo_name = time.strftime("%g%m%d%H%M%S")
		dirname = 'pictures'
		cv2.imwrite( os.path.join(dirname, photo_name) + '.jpg',frame)
		print('')
		print ('Save the picture')
		time.sleep(0.5) #暫停執行1秒
		print('Done')
		
		
		# 開始辨識
		jpg = photo_name + '.jpg'

		tStart = time.time() #計時開始

		# change this as you see fit
		image_path = "C:/Users/yueve/Desktop/Tensorflow/pictures/"+jpg	#讀取圖片的路徑

		# Read in the image_data
		image_data = tf.gfile.FastGFile(image_path, 'rb').read() #讀取圖片檔案

		# Loads label file, strips off carriage return #讀取模型標籤檔，並將每個標籤分割回傳

		label_lines = [line.rstrip() for line 
						   in tf.gfile.GFile("C:/Users/yueve/Desktop/Tensorflow/retrained_labels.txt")]

		# Unpersists graph from file
		with tf.gfile.FastGFile("C:/Users/yueve/Desktop/Tensorflow/retrained_graph.pb", 'rb') as f:
			graph_def = tf.GraphDef()
			graph_def.ParseFromString(f.read())
			_ = tf.import_graph_def(graph_def, name='')

		with tf.Session() as sess:
			# Feed the image_data as input to the graph and get first prediction
			softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
			
			predictions = sess.run(softmax_tensor, \
					 {'DecodeJpeg/contents:0': image_data})
			
			# Sort to show labels of first prediction in order of confidence
			top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
			
			for node_id in top_k:
				human_string = label_lines[node_id]
				score = predictions[0][node_id]
							   
				#print('%s (score = %.5f)' % (human_string, score))
				#print('%s' % (top_k))
				
			finall_num = predictions[0][top_k [0]]
			finall_name = label_lines[top_k [0]]
			
			print('')			
			print('%s	score = %.5f' % (finall_name, finall_num))			
			print ( 'photo Name : '+ time.strftime("%g%m%d%H%M%S")) #年分後兩位 2017的17 #月份 #日期 #小時 #分鐘 #秒數
			cursor.execute("SELECT * FROM plant_info WHERE type LIKE " + finall_name +";")

			
		tEnd = time.time()#計時結束
		
#列印結果
		print ("It cost %f sec" % (tEnd - tStart)) #會自動做近位

	elif cv2.waitKey(1) & 0xFF == ord('p'): #按p 上傳資料
	
		####資料庫部分
		# Connect to the database

		try: 
			with connection.cursor() as cursor:
				# Create a new record
				sql = "INSERT INTO `save_photo` (`file_name`, `kind`) VALUES (%s, %s)"
				cursor.execute(sql, (photo_name, finall_name))

			# connection is not autocommit by default. So you must commit to save
			# your changes.
			connection.commit()

			with connection.cursor() as cursor:
				# Read a single record
				sql = "SELECT `file_name`, `kind` FROM `save_photo` WHERE `file_name`=%s"
				cursor.execute(sql, (photo_name,))
				result = cursor.fetchone()
				print('')
				print(result)
		finally:

		
		
		
		
			#connection.close()
			print('')
			print('Upload finish')
		
		
		
		#cmd = "python C:/Users/yueve/Desktop/Tensorflow/label_image.py"
		#os.system(cmd)


	





# When everything is done, release the capture

video_capture.release()
cv2.destroyAllWindows()
