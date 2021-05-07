from socket import AF_INET, socket, SOCK_STREAM

import requests

import helper
import urllib
import webbrowser
import json


app_key = ''
app_secret = ''
server_addr = "localhost"
server_port = 8090
redirect_uri = "http://" + server_addr + ":" + str(server_port)

class Dropbox:
    _access_token = ""
    _path = "/"
    _files = []
    _root = None
    _msg_listbox = None

    def __init__(self, root):
        self._root = root

    def local_server(self):
        # 8090. portuan entzuten dagoen zerbitzaria sortu
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind((server_addr, server_port))
        server_socket.listen(1)
        print("\tLocal server listening on port " + str(server_port))

        # nabitzailetik 302 eskaera jaso
        client_connection, client_address = server_socket.accept()
        eskaera = client_connection.recv(1024)
        print("\tRequest from the browser received at local server:")
        print (eskaera)

        # eskaeran "auth_code"-a bilatu
        lehenengo_lerroa = eskaera.decode("UTF8").split('\n')[0]
        aux_auth_code = lehenengo_lerroa.split(' ')[1]
        auth_code = aux_auth_code[7:].split('&')[0]
        print ("\tauth_code: " + auth_code)

        # erabiltzaileari erantzun bat bueltatu
        http_response = "HTTP/1.1 200 OK\r\n\r\n" \
                        "<html>" \
                        "<head><title>Proba</title></head>" \
                        "<body>The authentication flow has completed. Close this window.</body>" \
                        "</html>"
        client_connection.sendall(http_response.encode(encoding="utf-8"))
        client_connection.close()
        server_socket.close()

        return auth_code

    def do_oauth(self):
        print("do_oauth")
        scope = "https://www.googleapis.com/auth/calendar.readonly"
        uri = "https://accounts.google.com/o/oauth2/v2/auth"
        cabeceras = {'Host': 'accounts.google.com'}
        datos = {'client_id': client_id,
                 'redirect_uri': redirect_uri,
                 'response_type': 'code',
                 'scope': scope}
        datos_encoded = urllib.parse.urlencode(datos)
        webbrowser.open_new((uri + '?' + datos_encoded))
        auth_code = self.local_server()
        uri = 'https://oauth2.googleapis.com/token'
        cabeceras = {'Host': 'oauth2.googleapis.com',
                     'Content-Type': 'application/x-www-form-urlencoded'}
        datos = {'code': auth_code,
                 'client_id': client_id,
                 'client_secret': client_secret,
                 'redirect_uri': redirect_uri,
                 'grant_type': 'authorization_code'}
        respuesta = requests.post(uri, headers=cabeceras, data=datos, allow_redirects=False)
        status = respuesta.status_code
        print("\tStatus: " + str(status))

        # Google responds to this request by returning a JSON object
        # that contains a short-lived access token and a refresh token.
        contenido = respuesta.text
        print("\tCotenido:")
        print(contenido)
        contenido_json = json.loads(contenido)
        access_token = contenido_json['access_token']
        print("\taccess_token: " + access_token)
        self._access_token= access_token
        self._root.destroy()

    def list_folder(self, msg_listbox):
        print("/list_folder")
        # https://www.dropbox.com/developers/documentation/http/documentation#files-list_folder
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################

        self._files = helper.update_listbox2(msg_listbox, self._path, edukia_json_dict)

    def transfer_file(self, file_path, file_data):
        print("/upload " + file_path)
        # https://www.dropbox.com/developers/documentation/http/documentation#files-upload
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################

    def delete_file(self, file_path):
        print("/delete_file " + file_path)
        # https://www.dropbox.com/developers/documentation/http/documentation#files-delete
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################

    def create_folder(self, path):
        print("/create_folder " + path)
        # https://www.dropbox.com/developers/documentation/http/documentation#files-create_folder
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################
