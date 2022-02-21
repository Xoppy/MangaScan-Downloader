import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
from tkinter import *
import threading
from PIL import Image
from PIL import ImageFile
import os
ImageFile.LOAD_TRUNCATED_IMAGES = True

#Initialisation de la fenetre
window = Tk()

#Customisation de la fenetre
window.title("MangaScan Downloader")
window.geometry("480x550")
window.minsize(480, 550)
window.maxsize(480, 550)
window.config(background="black")

#Creer une frame
frame = Frame(window, bg="black")

#Ajouter un premier texte
label_title = Label(frame, text="Bienvenue sur le tool MangaScan Downloader", font=("Helvetica", 16), bg="black", fg="white")
label_title.pack(pady=(5,20))

label_site = Label(frame, text="Selectionner le site", font=("Helvetica", 14), bg="black", fg="white")
label_site.pack(pady=(0, 10))

#Ajouter une liste de selection
selectionSites = ("ScansManga", "FrScan", "Lelscan")
selection_var = StringVar(value=selectionSites)
liste = Listbox(frame, listvariable=selection_var, height=len(selectionSites), selectmode="single", exportselection=False, bd=0, font=("Helvetica", 12), selectbackground="#515151")
liste.pack(pady=(0, 10))

label_manga_name = Label(frame, text="Nom du Manga", font=("Helvetica", 14), bg="black", fg="white")
label_manga_name.pack(pady=(0, 10))

textFieldMangaName = Entry(frame, width=25, bd=0, font=("Helvetica", 12))
textFieldMangaName.pack(pady=(0,10))

label_link = Label(frame, text="Insérer le lien de la première page du chapitre", font=("Helvetica", 14), bg="black", fg="white")
label_link.pack(pady=(0,10))

#Ajouter un text field
textFieldOne = Entry(frame, width=50, bd=0, font=("Helvetica", 12))
textFieldOne.pack(pady=(0,10))

label_chapNumber = Label(frame, text="Indiquer le nombre de chapitres/pages à télécharger", font=("Helvetica", 14), bg="black", fg="white")
label_chapNumber.pack(pady=(0,10))

#Ajouter un text field
textFieldTwo = Entry(frame, width=50, bd=0, font=("Helvetica", 12))
textFieldTwo.pack(pady=(0,10))

mangaName = "Manga"
imagelist = []

#
# Fonction qui lance le téléchargement
#

def downloadFunc (img_list_final, mangaName, url):
    print ("Début du téléchargement")
    pageNumber = 1
    
    #Loop qui télécharge chauqe élément de la liste img_list_final
    for image in img_list_final:
        img_data = requests.get(image).content
        with open(mangaName + "_" + str(pageNumber) + ".jpg", 'wb') as handler:
            handler.write(img_data)
            imagelist.append(mangaName + "_" + str(pageNumber) + ".jpg")
        pageNumber +=1

    print("Téléchargement términé")
    print ("Voici le lien de la dérniere page téléchargée : " + url)

#
# Fonction qui crée le PDF --- MAX 2000 Pages sur 16GB de RAM
#

def pdfMaker(imagelist, mangaName):
    len(imagelist)
    images =[]
    w = 1
    
    if (len(imagelist) > 2000):
        while w < 2000:
            images.append(Image.open(imagelist[w]).convert('RGB'))
            w +=1
    else:
        while w < len(imagelist):
            images.append(Image.open(imagelist[w]).convert('RGB'))
            w +=1
            
    firstImage = Image.open(imagelist[0])
    firstImage.save(mangaName + ".pdf", save_all=True, append_images=images)
    
    #Efface les images
    for item in imagelist:
        os.remove(item)


#
# Scansmanga.xyz scraper
#

def scansManga (url, chapterNumber, mangaName):
    #Initialisation de plusieurs variables necessaires dans les loop et les listes suivantes
    i = 1
    page_url = []
    page_list = []

    #Création de la liste des pages du site 
    print("Collection de la liste des pages du site")
    #Premier chapitre
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    soup_div = soup.find("div", {"class":"nav_apb"})
    for link in soup_div.find_all('a'):
        page_url.append(link.get('href'))
    page_list = page_url[:-1]
    url = page_url.pop()

    #Loop du deuxième chapite et suivant
    while i < chapterNumber:
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        soup_div = soup.find("div", {"class":"nav_apb"})
        for link in soup_div.find_all('a'):
            page_url.append(link.get('href'))
        url = page_url.pop()
        i += 1

    #Exctraction des lien source des images individuelles
    print("Exctraction des liens source des images")
    img_links = []
    for link in page_url:
        response = requests.get(link)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        soup_img_div = soup.find("div", {"class" : "area"})
        soup_img = soup_img_div.find_all("img")
        for image in soup_img:
            img_links.append(image['src'])
    
    #Modification des liens pour les rendres homogenes
    print("Modification des liens")
    img_list_final = [s.replace("\n", "") for s in img_links]

    #Début du téléchargement
    downloadFunc(img_list_final, mangaName, url)
    
    #Création du pdf
    print("creation du pdf")
    pdfMaker(imagelist, mangaName)
    print("pdf términé")

#
#lelscans.net
#

def lelscans (url, chapterNumber, mangaName):
    #Initialisation de plusieurs variables necessaires dans les loop et les listes suivantes
    i = 0
    page_url = []
    img_list_final = []

    #Création de la liste des pages du site
    print("Collection de la liste des pages du site")
    while i < chapterNumber:
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        soup_div = soup.find("div", {"id":"navigation"}).find_all("a")
        del soup_div[-2]
        del soup_div[0]
        for item in soup_div:
            page_url.append(item.get('href'))

        url = page_url.pop()
        i += 1

    #Exctraction des lien source des images individuelles
    print("Exctraction des liens source des images")
    for link in page_url:
        response = requests.get(link)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        soup_img_div = soup.find("td", attrs={'style':"min-width:895px;"})
        soup_img = soup_img_div.find_all("img")
        for image in soup_img:
            img_list_final.append(image['src'])

    #Modification des liens pour les rendres homogenes
    print("Modification des liens")
    x = 0
    for item in img_list_final:
        img_list_final[x] = "https://lelscans.net" + item
        x +=1
        
    #Début du téléchargement
    downloadFunc(img_list_final, mangaName, url)
    
    #Création du pdf
    print("creation du pdf")
    pdfMaker(imagelist, mangaName)
    print("pdf términé")
    
    
#
# FRSCAN.CC scraper
#
    
def frscancc (url, pageNumber, mangaName):
    #Initialisation de plusieurs variables necessaires dans les loop et les listes suivantes
    i = 1
    page_url = [url]

    #Création de la liste des pages du site
    print("Collection de la liste des pages du site")
    while i < pageNumber:
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        soup_div = soup.find("div", {"id":"ppp"})
        for link in soup_div.find_all("a"):
            page_url.append(link.get('href'))
            nextPage = page_url

        for ele in page_url:
            if ele == None:
                page_url.remove(ele)

        url = page_url[-1]
        i+=1

    #Exctraction des lien source des images individuelles
    print("Exctraction des liens source des images")
    img_links = []
    for link in page_url:
        response = requests.get(link)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        soup_img_div = soup.find("div", {"id" : "ppp"})
        soup_img = soup_img_div.find_all("img")
        for image in soup_img:
            img_links.append(image['src'])

    #Modification des liens pour les rendres homogenes
    print("Modification des liens")
    img_list_final = [s.replace("http:", "") for s in img_links]
    img_list_final = [s.replace(" ", "") for s in img_list_final]

    x = 0
    for item in img_list_final:
        img_list_final[x] = "http:" + item
        x += 1

    #Début du téléchargement
    downloadFunc(img_list_final, mangaName, url)
    
    #Création du pdf
    print("creation du pdf")
    pdfMaker(imagelist, mangaName)
    print("pdf términé")
    
#
# IF / ELSE SELECTION SITE
#

def startProcess ():
    if liste.curselection()[0] == 0:
        url = textFieldOne.get()
        chapterNumber = textFieldTwo.get()
        chapterNumber = int(chapterNumber)
        mangaName = textFieldMangaName.get()
        scansManga(url, chapterNumber, mangaName)
    elif liste.curselection()[0] == 1:
        url = textFieldOne.get()
        pagenumber = textFieldTwo.get()
        pagenumber = int(pagenumber)
        mangaName = textFieldMangaName.get()
        frscancc(url, pagenumber, mangaName)
    elif liste.curselection()[0] == 2:
        url = textFieldOne.get()
        chapterNumber = textFieldTwo.get()
        chapterNumber = int(chapterNumber)
        mangaName = textFieldMangaName.get()
        lelscans (url, chapterNumber, mangaName)
        

#Ajouter un bouton
testBtn = Button(frame, text="Valider", font=("Helvetica", 14), bg="white", fg="black", command=startProcess)
testBtn.pack(pady=20)

disclaimerText = Label(frame, wraplength=460, text="La structure de Frscan ne permet pas le téléchargement par chapitres, il faut donc indiquer le nombre de pages souhaitées.", font=("Helvetica", 11), bg="black", fg="white")
disclaimerText.pack(side=BOTTOM)

#Ajouter la frame à la fenetre
frame.pack(fill=BOTH, expand=TRUE, padx=10, pady=25)

#Lancement de la fenetre
window.mainloop()