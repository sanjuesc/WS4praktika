from tkinter import messagebox
import time

import requests
from bs4 import BeautifulSoup

import helper

class eGela:
    _login = 0
    _cookiea = ""
    _refs = []
    _root = None

    def __init__(self, root):
        self._root = root

    def check_credentials(self, username, password, event=None):
        popup, progress_var, progress_bar = helper.progress("check_credentials", "Logging into eGela...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        print("##### 1. ESKAERA #####")

        metodo = 'POST'
        uri = "https://egela.ehu.eus/login/index.php"
        print(datuak)
        goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded',
                     'Content-Length': str(len(datuak))}
        erantzuna = requests.request(metodo, uri, data=datuak, headers=goiburuak, allow_redirects=False)
        print(str(erantzuna.status_code) + " " + erantzuna.reason)

        if erantzuna.status_code == 303:  ## berbideraketa egin
            # print(uneko_uria + " hurrengo orria eramango gaitu " + erantzuna.headers['Location'])
            uri = erantzuna.headers['Location']
        if "Set-Cookie" in erantzuna.headers:  ## cookiea gorde
            cookie = erantzuna.headers["Set-Cookie"].split(';')[0]  # soilik cookie berria interesatzen zaigu, ezabatzen dena ez

        progress = 33
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)

        print("\n##### 2. ESKAERA #####")
        print(uri)
        goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded',
                     'Content-Length': str(len(datuak)), "Cookie": cookie}
        erantzuna = requests.request(metodo, uri, data=datuak, headers=goiburuak, allow_redirects=False)
        print(str(erantzuna.status_code) + " " + erantzuna.reason)

        if erantzuna.status_code == 303:  ## berbideraketa egin
            # print(uneko_uria + " hurrengo orria eramango gaitu " + erantzuna.headers['Location'])
            uri = "https://egela.ehu.eus"
        if "Set-Cookie" in erantzuna.headers:  ## cookiea gorde
            cookie = erantzuna.headers["Set-Cookie"].split(';')[0]  # soilik cookie berria interesatzen zaigu, ezabatzen dena ez

        progress = 66
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)

        print("\n##### 3. ESKAERA #####")
        print(uri)
        goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded',
                     'Content-Length': str(len(datuak)), "Cookie": cookie}
        erantzuna = requests.request(metodo, uri, data=datuak, headers=goiburuak, allow_redirects=False)
        print(str(erantzuna.status_code) + " " + erantzuna.reason)

        progress = 100
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)
        popup.destroy()

        if erantzuna.status_code==200:
            _cookiea = cookie
            _login = 1
            self._root.destroy()
            soup = BeautifulSoup(erantzuna.content, "html.parser")

        else:
            messagebox.showinfo("Alert Message", "Login incorrect!")
            print(erantzuna.status_code)
            print(erantzuna.reason)


    def get_pdf_refs(self):
        popup, progress_var, progress_bar = helper.progress("get_pdf_refs", "Downloading PDF list...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        uri="https://egela.ehu.eus"
        print("\n##### 4. ESKAERA (Ikasgairen eGelako orrialde nagusia) #####")
        metodoa = 'POST'
        datuak = ""
        global _cookiea
        cookie = _cookiea
        goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded',
                     'Content-Length': str(len(datuak)), "Cookie": cookie}
        erantzuna = requests.request(metodoa, uri, data=datuak, headers=goiburuak, allow_redirects=False)
        soup = BeautifulSoup(erantzuna.content, "html.parser")
        ikasgaiak = soup.find_all("a", {"class": "ehu-visible"})
        for x in ikasgaiak:  # web sistemak irakasgaiaren URI-a lortu
            if ("Web Sistemak" in x):
                uri = x["href"]
                break
        erantzuna = requests.request(metodoa, uri, data=datuak, headers=goiburuak, allow_redirects=False)

        progress_step = float(100.0 / len(self._refs))

        print("\n##### HTML-aren azterketa... #####")
        #############################################
        # ANALISIS DE LA PAGINA DEL AULA EN EGELA
        # PARA BUSCAR PDFs
        #############################################

            # ACTUALIZAR BARRA DE PROGRESO
            # POR CADA PDF ANIADIDO EN self._refs
        progress += progress_step
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)

        popup.destroy()
        return self._refs

    def get_pdf(self, selection):
        print("##### PDF-a deskargatzen... #####")
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################

        return pdf_name, pdf_file