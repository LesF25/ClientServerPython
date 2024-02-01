from socket import *
import json

class Client:
	def __init__(self, ip, port):
		self.client = socket(AF_INET, SOCK_STREAM)
		self.client.connect(
			(ip, port)
		)

	def connect(self):
		try:
			message = self.client.recv(1024).decode("utf-8")
		except Exception as e:
			print(f"ERROR: {str(e)}")
			exit()

		if message == "YOU ARE CONNECTED!":
			self.listen()
		else:
			exit()

	def send(self, message):
		self.client.send(message.encode("utf-8"))
		while self.client.recv(1024).decode("utf-8") != "SERVER GOT DATA!":
			self.client.send(message.encode("utf-8"))

	def listen(self):
		is_work = True
		while is_work:
			request = input("Type SQL request: ")

			if request:
				if request == "disconnect":
					self.send(request)
					print(self.client.recv(1024).decode("utf-8"))
				else:
					self.send(request)
					data = json.loads(self.client.recv(1024).decode("utf-8"))

					if (data["answer"]):
						print(f"SERVER ANSWER:\n\t{data['answer']}")
					elif data["error"]:
						print(f"SERVER ERROR:\n\t{data['error']}")

Client("127.0.0.1", 1111).connect()