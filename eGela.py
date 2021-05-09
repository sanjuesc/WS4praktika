import urllib
from tkinter import messagebox
import time

import requests
from bs4 import BeautifulSoup

import helper
import os


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
        datuak = {'username': username.get(), 'password': password.get()}
        metodo = 'POST'
        uri = "https://egela.ehu.eus/login/index.php"

        goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded',
                     'Content-Length': str(len(datuak))}

        edukia_encoded = urllib.parse.urlencode(datuak)
        goiburuak['Content-Length'] = str(len(edukia_encoded))

        erantzuna = requests.request(metodo, uri, data=edukia_encoded, headers=goiburuak, allow_redirects=False)

        if erantzuna.status_code == 303:
            uri = erantzuna.headers['Location']
            print("Location : " + uri)
        if "Set-Cookie" in erantzuna.headers:
            self._cookiea = erantzuna.headers["Set-Cookie"].split(';')[0]
            print("Cookie : " + self._cookiea)

        print(str(erantzuna.status_code) + " " + erantzuna.reason)

        progress = 33
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)

        print("\n##### 2. ESKAERA #####")
        print(uri)
        goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded',
                     'Content-Length': str(len(datuak)), "Cookie": self._cookiea}

        edukia_encoded = urllib.parse.urlencode(datuak)
        goiburuak['Content-Length'] = str(len(edukia_encoded))

        erantzuna = requests.request(metodo, uri, data=edukia_encoded, headers=goiburuak, allow_redirects=False)

        if erantzuna.status_code == 303:
            uri = erantzuna.headers['Location']
            print("Location : " + uri)
        if "Set-Cookie" in erantzuna.headers:
            self._cookiea = erantzuna.headers["Set-Cookie"].split(';')[0]
            datuak = ""

        print(str(erantzuna.status_code) + " " +erantzuna.reason)

        progress = 66
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)

        print("\n##### 3. ESKAERA #####")
        print(uri)
        goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded',
                     'Content-Length': str(len(datuak)), "Cookie": self._cookiea}

        edukia_encoded = urllib.parse.urlencode(datuak)
        goiburuak['Content-Length'] = str(len(edukia_encoded))

        erantzuna = requests.request(metodo, uri, data=edukia_encoded, headers=goiburuak, allow_redirects=False)

        print(str(erantzuna.status_code) + " " + erantzuna.reason)


        progress = 100
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)
        popup.destroy()

        if erantzuna.status_code == 200:
            self._login = 1
            self._root.destroy()
        else:
            messagebox.showinfo("Alert Message", "Login incorrect!")

    def get_pdf_refs(self):

        popup, progress_var, progress_bar = helper.progress("get_pdf_refs", "Downloading PDF list...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        print("\n##### 4. ESKAERA (Ikasgairen eGelako orrialde nagusia) #####")
        metodo = 'POST'
        datuak = ""
        goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded',
                     'Content-Length': str(len(datuak)), "Cookie": self._cookiea}

        uri = "https://egela.ehu.eus/course/view.php?id=42336&section=1"  # goian lortutako uri azken sekzioan sartzen da eta hor soilik pdf 1 dago, beraz, eskuz sartu dut lehen sekzioaren uria
        erantzuna = requests.request(metodo, uri, data=datuak, headers=goiburuak, allow_redirects=False)

        if (erantzuna.status_code == 200):
            print("Ikasgaiaren orria ondo lortu da")
            soup = BeautifulSoup(erantzuna.content, "html.parser")
            pdf_results = soup.find_all("div", {"class": "activityinstance"})
            kop = str(pdf_results).count("pdf")

        print("PDF kopurua " + str(kop))
        # print("PDF kopurua " + str(len(self._refs)))
        progress_step = float(100.0 / kop)
        # progress_step = float(100.0 / len(self._refs))
        print("\n##### HTML-aren azterketa... #####")

        for pdf in pdf_results:
            if pdf.find("img", {"src": "https://egela.ehu.eus/theme/image.php/fordson/core/1619589309/f/pdf"}):  # egelako elementuetatik, pdf bezala agertzen direnak bilatu
                # ACTUALIZAR BARRA DE PROGRESO
                # POR CADA PDF ANIADIDO EN self._refs
                progress += progress_step
                progress_var.set(progress)
                progress_bar.update()
                time.sleep(0.1)

                uri = pdf.find("a")["href"]+"&redirect=1"
                metodo = 'POST'
                datuak = ""
                goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded',
                             'Content-Length': str(len(datuak)), "Cookie": self._cookiea}
                erantzuna = requests.request(metodo, uri, data=datuak, headers=goiburuak, allow_redirects=False)

                pdf_uri = erantzuna.headers['Location']
                pdf_link = pdf_uri.split("mod_resource/content/")[1].split("/")[1].replace("%20", "_")
                self._refs.append({"pdf_name": pdf_link, "pdf_link": pdf_uri})

        for elem in self._refs:
            print(elem)
        popup.destroy()
        return self._refs

    def get_pdf(self, selection):
        print("##### PDF-a deskargatzen... #####")
        pdf_name = self._refs[selection]['pdf_name']
        pdf_link = self._refs[selection]['pdf_link']


        goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded',
                     'Content-Length': '0', "Cookie": self._cookiea}
        erantzuna = requests.request('GET', pdf_link, headers=goiburuak, allow_redirects=False)

        pdf_file = erantzuna.content
        print(pdf_name + " downloaded !")

        return pdf_name, pdf_file


    def download_pdf(self, pdf_name):
        print(pdf_name)
        for each in self._refs:
            if each["pdf_name"]==pdf_name:
                uri = each["pdf_link"]
                break
        print(uri)
        metodoa = 'POST'
        datuak = ""
        goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded',
                     'Content-Length': str(len(datuak)), "Cookie": self._cookiea}

        erantzuna = requests.request(metodoa, uri, data=datuak, headers=goiburuak, allow_redirects=False)
        with open(pdf_name,'wb') as fd:  # https://stackoverflow.com/questions/34503412/download-and-save-pdf-file-with-python-requests-module
            for chunk in erantzuna.iter_content():
                fd.write(chunk)
        os.startfile(pdf_name)

