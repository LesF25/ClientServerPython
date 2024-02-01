from socket import *
import sqlite3 as sql
import json

class Server:
	def __init__(self, ip, port, database_name):
		print(f"SERVER IP: {ip}\nSERVER PORT: {port}\n")
		self.database_name = database_name
		self.server = socket(AF_INET, SOCK_STREAM)
		self.server.bind(
			(ip, port)
		)
		self.server.listen(1)

	def send(self, client, message):
		client.send(message.encode("utf-8"))
		
	def start(self):
		while True:
			client, addr = self.server.accept()
			print(f"CLIENT CONNECTED:\n\tIP: {addr[0]}\n\tPORT: {addr[1]}")
			self.listen(client)

	def listen(self, client):
		self.send(client, "YOU ARE CONNECTED!")
		is_work = True

		while is_work:
			try:
				data = client.recv(1024)
				self.sender(client, "SERVER GOT DATA!")
			except Exception as e:
				is_work = False
				data = ""
			
			if len(data) > 0:
				message = data.decode("utf-8")
				if message == "disconnect":
					self.send(client, "YOU ARE DISCONNECTED!")
					client.close()
					is_work = False
				else:
					con_db = sql.connect(self.database_name)
					cur_db = con_db.cursor()
					try:
						answer = [x for x in cur_db.execute(message)]
						error = ""
					except Exception as e:
						error = str(e)
						answer = ""

					con_db.commit()
					cur_db.close()
					con_db.close()

					ans = json.dumps(
						{ "answer" : answer, "error" : error}
					)

					self.send(client, ans)

				data = b""
				message = ""
			else:
				print("CLIENT DISCONNECTED!")
				is_work = False

Server("127.0.0.1", 1111, "data.db").start()