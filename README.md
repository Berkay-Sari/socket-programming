# socket-programming
An HTTP server over TCP socket programming with python. The server is running on port 8080 and localhost.

# endpoints 

- GET /isPrime:
o This endpoint returns a json response whether a number it takes as a parameter is prime or not. If the incoming parameter is not an integer, a 400 Bad Request error is returned and a warning message "Please enter an integer" is added to the returned packet.
o Parameter name: “number”. If there is no "number" among the parameters, the server returns a 400 Bad Request response.
o As a result of successful requests, it returns an appropriate json response and http status code 200 OK.
o Example response: {number: 5, isPrime: True}

- POST /upload:
o Bu endpointte ise client, sunucumuza bir dosya upload edebilir. Sunucumuz ise bu dosyayı gönderilen dosyanın isminde kaydetmektedir. Dosya uzantısını gönderilen dosyaya göre belirlenir.
o Eğer dosya gönderilmedi ise yine 400 Bad Request hatası verir.
o Dosyanın sunucuya yüklenme işlemi başarılı bir şekilde gerçekleştirildikten sonra uygun bir json cevabıyla birlikte 200 OK durum kodu döner.

- PUT /rename:
o This endpoint has two parameters: “oldFileName” and “newName”.
o What Endpoint does is to change the name of a file that was previously uploaded to the server.
o If a file given in the oldFileName parameter is not found, a 200 OK http response is returned with a json response explaining the situation.
o When the file name is changed successfully, a 200 OK http response is returned with an appropriate json response.

- DELETE /remove:
o At this endpoint, the file given with the "fileName" parameter is deleted from the server.
o If the fileName is not found on the server, the {message: “File not found”} response is returned with a 200 OK code.
o If the file is deleted successfully, {message: “File succesfully deleted”} is returned.
o If the fileName parameter is not given, {message: "fileName parameter is missing"} response is returned with a 400 Bad Request code.

- GET /download:
o In this endpoint, the file given with the "fileName" parameter is sent to the client by the server, that is, the client downloads the file from the server.
o Like the previous endpoints, appropriate messages are returned for the missing parameter and at the end of the successful download, the file returns with a 200 OK code.
