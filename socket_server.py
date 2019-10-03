import socket
import threading
import time
import json
server_ip = '0.0.0.0'
server_port = 8091
is_accepted = False
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_ip, server_port))
server.listen(10)
        # print('[*] listening on ' + self.server_ip + ':' + str(self.server_port))


def handle_client(client, port):
    
    from database import db
    import json
    request = client.recv(1024).decode()
    this_data = json.loads(request)
    print('json date from : ',this_data["date_from"],'date to : '+this_data["date_to"])
    this_db = db()
    report = this_db.reportConsumption(this_data['date_from'],this_data['date_to'])
    print('report is : ' ,report)
    this_db.closedb()
    json_report = json.dumps(report,sort_keys=True)
    print( json_report)
    client.send(json_report)
    client.close()
        # time.sleep(2)

while True:
    client, port = server.accept()
    is_accepted = True
    client,port = client, port
            # print('connection acceped!')
    handler_client = threading.Thread(
        target=handle_client, args=(client, port))
    handler_client.run()

