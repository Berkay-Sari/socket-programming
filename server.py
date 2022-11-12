from socket import *
import math
import os

serverPort = 8080
serverSocket = socket(AF_INET,SOCK_STREAM) #IPv4 - TCP
serverSocket.bind(("localhost", serverPort))
serverSocket.listen(1)
print("The server is ready to receive")

# efficiently checks if the given parameter (num) is prime
def isPrime(num):
    if num < 2:
        return False
    i=2
    while i<=math.sqrt(num):
        if num%i<1:
            return False
        i+=1
    return num>1

while True:
    # Wait for client connections
    client_connection, client_address = serverSocket.accept()
    print("New Connection\n----------------")
    print(client_address)
    print("----------------")
    # Get the client request
    request = client_connection.recv(1024).decode()

    # parse HTTP request message
    request_line = request.split('\r\n')[0] # for ex: req_line -> GET /isPrime?number=5 HTTP/1.1
    metot = request_line.split()[0] # GET, POST, PUT, DELETE
    url = request_line.split()[1] #/isPrime?number=5, upload, rename/..., remove?fileName=file1.png, download/...
    response = 'HTTP/1.1 404 NOT FOUND\n\n'
    isDownload = False
    if metot == 'GET':
        correctEndPoint = False
        hasParam = True
        try:
            endpoint, parameters = url.split('?')
        except:
            hasParam = False
        if hasParam:
            if endpoint == '/isPrime':
                correctEndPoint = True
                response = 'HTTP/1.1 200 OK\nContent-Type: application/json\n\n'
                containsNumber = False
                for param in parameters.split('&'):
                    try:
                        key, value = param.split('=')
                    except:
                        continue
                    if key == 'number':
                        containsNumber = True
                        try: 
                            result = isPrime(int(value))
                            response += '{"number": ' + value + ', "isPrime": ' + str(result) + '}'
                        except:
                            response = 'HTTP/1.1 400 Bad Request\nContent-Type: application/json\n\n{"message": "Lutfen tam sayi giriniz"}\r\n\r\n'

                if not containsNumber: 
                    response = 'HTTP/1.1 400 Bad Request\nContent-Type: application/json\n\n{"message": "Parametreler arasinda number yok!"}\r\n\r\n'
            
            if endpoint == '/download':
                correctEndPoint = True
                containsFile = False
                for param in parameters.split('&'):
                    try:
                        key, value = param.split('=')
                    except:
                        continue
                    if key == 'fileName':
                        containsFile = True
                        if not os.path.exists(value):
                            response = 'HTTP/1.1 200 OK\nContent-Type: application/json\n\n{"filename": "' + value + '", "message": "Dosya bulunamadi"}\r\n\r\n'
                        else: 
                            isDownload = True
                            response = 'HTTP/1.1 200 OK\nContent-Type: application/octet-stream\nContent-Disposition: attachment; filename="' + value + '"\n\n'
                            client_connection.sendall(response.encode())
                            with open(value, 'rb') as file_to_send:
                                for data in file_to_send:
                                    client_connection.sendall(data)
                            
                if not containsFile: 
                    response = 'HTTP/1.1 400 Bad Request\nContent-Type: application/json\n\n{"message": "Parametreler arasinda fileName yok!"}\r\n\r\n'
        elif correctEndPoint: 
            response = 'HTTP/1.1 400 Bad Request\nContent-Type: application/json\n\n{"message": "Eksik parametre!"}\r\n\r\n'

        

    if metot == 'POST':        
        if url == '/upload':
            print(request)
            #some hard-code for extract filename and boundary value from request message
            boundary_start = request.find("boundary=")+9
            boundary_end = request.find("\r", boundary_start)
            boundary = request[boundary_start:boundary_end]
            start_index = request.find("filename=")
            if start_index != -1:
                end_index = request.find("\"", start_index+10)
                file_name = request[start_index+10:end_index]
                data = client_connection.recv(4096)
                while True:
                    incoming_packet = client_connection.recv(4096)
                    x = incoming_packet.find(bytes(boundary, 'ascii'))
                    if x != -1:
                        new_packet = incoming_packet.replace(bytes(boundary, 'ascii'), b'')
                        data += new_packet[:-8]
                        break
                    data += incoming_packet
                file = open(file_name, "wb")
                print(data)
                file.write(data)    
                file.close()
                response = 'HTTP/1.1 200 OK\nContent-Type: application/json\n\n{"message": "Dosya basariyla yuklendi!"}\r\n\r\n'
            else:
                response = 'HTTP/1.1 400 Bad Request\nContent-Type: application/json\n\n{"message": "Dosya gonderilmedi!"}\r\n\r\n'
    
    if metot == 'PUT':
        hasParam = True
        try:
            endpoint, parameters = url.split('?')
        except:
            hasParam = False
        if hasParam:
            if endpoint == '/rename':
                oldExist = False
                newExist = False
                oldName, newName = "", ""
                for param in parameters.split('&'):
                    try:
                        key, value = param.split('=')
                    except:
                        continue
                    if key == "oldFileName":
                        oldExist = True
                        oldName = value
                    if key == "newName":
                        newExist = True
                        newName = value
                if oldExist and newExist:
                    if not os.path.exists(oldName):
                        response = 'HTTP/1.1 200 OK\nContent-Type: application/json\n\n{"filename": "' + oldName + '", "message": "Dosya bulunamadi!"}\r\n\r\n'
                    elif os.path.isfile(newName):
                        response = 'HTTP/1.1 200 OK\nContent-Type: application/json\n\n{"message": "Yeni dosya ismi zaten mevcut!"}\r\n\r\n'
                    else:
                        os.rename(oldName, newName)
                        response = 'HTTP/1.1 200 OK\nContent-Type: application/json\n\n' + \
                        '{"oldName": "' + oldName + '", "newName": "' + newName + '", "message": "Dosya ismi basariyla degistirildi!"}\r\n\r\n'
                else: 
                    response = 'HTTP/1.1 400 Bad Request\nContent-Type: application/json\n\n{"message": "Eksik query parametresi!"}\r\n\r\n'
        else:
            response = 'HTTP/1.1 400 Bad Request\nContent-Type: application/json\n\n{"message": "Eksik query parametresi!"}\r\n\r\n'

    if metot == 'DELETE':   
        hasParam = True
        try:
            endpoint, parameters = url.split('?')
        except:
            hasParam = False
        if hasParam:    
            fileNameExist = False
            if endpoint == '/remove':    
                for param in parameters.split('&'):
                    try:
                        key, value = param.split('=')
                    except:
                        continue
                    if key == "fileName":
                        fileNameExist = True
                        if not os.path.exists(value):
                            response = 'HTTP/1.1 200 OK\nContent-Type: application/json\n\n{"filename": "' + oldName + '", "message": "Dosya bulunamadi"}\r\n\r\n'
                        else: 
                            os.remove(value)
                            response = 'HTTP/1.1 200 OK\nContent-Type: application/json\n\n{"message": "Dosya basarili bir sekilde silindi"}\r\n\r\n'
                if not fileNameExist:
                    response = 'HTTP/1.1 400 Bad Request\nContent-Type: application/json\n\n{"message": "fileName parametresi eksik"}\r\n\r\n'   
        else:
            response = 'HTTP/1.1 400 Bad Request\nContent-Type: application/json\n\n{"message": "fileName parametresi eksik"}\r\n\r\n'   
    
    print("Client send " + metot + " request to endpoint " + url)
    # Send HTTP response
    if not isDownload:
        print('Server response...\n' + response)
        client_connection.sendall(response.encode())
    print('Connection closing...')
    client_connection.close()