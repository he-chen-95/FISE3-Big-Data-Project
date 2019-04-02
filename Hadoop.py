from hdfs import InsecureClient

def getData():
	#9870:NameNode web¹ÜÀí¶Ë¿Ú
	client = InsecureClient("http://localhost:9870", user="user")
	client.list("/") 
	client.status("/") 
	client.download("/test/dataset.csv",".","True")