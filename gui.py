from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from fillpdf import fillpdfs
import webbrowser
import re
import sys
import os
import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog
from pathlib import Path
from PIL import ImageTk, Image
import serial
import cv2
import ctypes
from FPIAnalysisWindow import FPIAnalysis

import cv2
import requests

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

#Mebuat Canvas Halaman
window = Tk()
window.geometry("1078x600")
window.configure(bg = "#FFFFFF")
canvas = Canvas(
    window, bg = "#FFFFFF", height = 647, width = 1078, bd = 0, highlightthickness = 0, relief = "ridge"
)

#Icon dan Label
myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
logo = tk.PhotoImage(file="./assets/telkom.png")
window.call('wm', 'iconphoto', window._w, logo)
window.title("Pengembangan Sistem Penilaian Postur Kaki Otomatis Menggunakan Metode FPI-6 Berbasis Fotogrametri")

#Judul Halaman
canvas.place(x = 0, y = 0)
canvas.create_rectangle(0.0, 0.0, 1078.0, 70.0, fill="#3A7FF6", outline="")
canvas.create_text(
    405.0, 10.0, anchor="nw", text="Panel Pemantauan",
    fill="#FFFFFF", font=("RobotoRoman ExtraBold", 40 * -1)
)

#Background Graphic
blueRect = PhotoImage(file=relative_to_assets("blueRect.png"))
rectBlue1 = canvas.create_image(381.0, 202.0, image=blueRect)
rectBlue2 = canvas.create_image(655.0, 202.0, image=blueRect)
rectBlue3 = canvas.create_image(929.0, 202.0, image=blueRect)
rectBlue4 = canvas.create_image(381.0, 450.0, image=blueRect)
rectBlue5 = canvas.create_image(655.0, 450.0, image=blueRect)
rectBlue6 = canvas.create_image(929.0, 450.0, image=blueRect)

canvas.create_rectangle(447.0, 276.0, 503.0, 312.0, fill="#FFFFFF", outline="")
canvas.create_rectangle(259.0, 276.0, 447.0, 312.0, fill="#EEEEEE", outline="")
canvas.create_text(300.0, 282.0, anchor="nw", text="Karakteristik 1", fill="#000000", font=("Roboto", 17 * -1))
canvas.create_rectangle(533.0, 276.0, 721.0, 312.0, fill="#EEEEEE", outline="")
canvas.create_rectangle(721.0, 276.0, 777.0, 312.0, fill="#FFFFFF", outline="")
canvas.create_text(574.0, 282.0, anchor="nw", text="Karakteristik 2", fill="#000000", font=("Roboto", 17 * -1))
canvas.create_rectangle(807.0, 276.0, 995.0, 312.0, fill="#EEEEEE", outline="")
canvas.create_rectangle(995.0, 276.0, 1051.0, 312.0, fill="#FFFFFF", outline="")
canvas.create_text(848.0, 282.0, anchor="nw", text="Karakteristik 3", fill="#000000", font=("Roboto", 17 * -1))
canvas.create_rectangle(259.0, 523.0, 447.0, 559.0, fill="#EEEEEE", outline="")
canvas.create_rectangle(447.0, 523.0, 503.0, 559.0, fill="#FFFFFF", outline="")
canvas.create_text(300.0, 529.0, anchor="nw", text="Karakteristik 4", fill="#000000", font=("Roboto", 17 * -1))
canvas.create_rectangle(533.0, 523.0, 721.0, 559.0, fill="#EEEEEE", outline="")
canvas.create_rectangle(721.0, 523.0, 777.0, 559.0, fill="#FFFFFF", outline="")
canvas.create_text(574.0, 529.0, anchor="nw", text="Karakteristik 5", fill="#000000", font=("Roboto", 17 * -1))
canvas.create_rectangle(807.0, 523.0, 995.0, 559.0, fill="#EEEEEE", outline="")
canvas.create_rectangle(995.0, 523.0, 1051.0, 559.0, fill="#FFFFFF", outline="")
canvas.create_text(848.0, 529.0, anchor="nw", text="Karakteristik 6", fill="#000000", font=("Roboto", 17 * -1))

#Karakteristik 1 dan 4 (Filler 3D)
filler3D = PhotoImage(file=relative_to_assets("3dFiller.png"))
canvas.create_image(381.0, 181.0, image=filler3D)
canvas.create_image(381.0, 428.0, image=filler3D)

#Karakteristik 2
imageChar2 = tk.PhotoImage(file=relative_to_assets("dummyChar2.png"))
# imageMin2 = PhotoImage(file=relative_to_assets("image8.png"))
# imageChar2 = imageMin2.subsample(8)

# path2 = Path("hasilVideo/image8.jpg")
# if os.path.isfile(path2):
#     imageMin2 = tk.PhotoImage(file="hasilVideo/image8.jpg")
#     imageChar2 = imageMin2.subsample(8)
# else:
#     imageChar2 = tk.PhotoImage(file=relative_to_assets("dummyChar2.png"))

char2 = canvas.create_image(655.0, 181.0, image=imageChar2)

#Karakteristik 3
imageChar3 = PhotoImage(file=relative_to_assets("dummyChar3.png"))
char3 = canvas.create_image(929.0, 181.0, image=imageChar3)

#Karakteristik 5
imageChar5 = PhotoImage(file=relative_to_assets("dummyChar5.png"))
char5 = canvas.create_image(655.0, 428.0, image=imageChar5)

#Karakteristik 6
imageChar6 = PhotoImage(file=relative_to_assets("dummyChar6.png"))
char6 = canvas.create_image(929.0, 428.0, image=imageChar6)

#Kumpulan Input
namaLengkapEntry = tk.Entry(bd=0, bg="#FFFFFF", highlightthickness=0,font=12)        #Input Nama Lengkap
namaLengkapEntry.place(x=27.0, y=133, width=200.0, height=30)

tanggalPemeriksaanEntry = tk.Entry(bd=0, bg="#FFFFFF", highlightthickness=0,font=12) #Tanggal Pemeriksaan
tanggalPemeriksaanEntry.place(x=27.0, y=224, width=200.0, height=30)

karakteristik1Entry = tk.Entry(bd=0, bg="#FFFFFF", highlightthickness=0,font=12)     #Karakteristik 1
karakteristik1Entry.place(x=463.0, y=279, width=40.0, height=30)
karakteristik2Entry = tk.Entry(bd=0, bg="#FFFFFF", highlightthickness=0,font=12)     #Karakteristik 2
karakteristik2Entry.place(x=737.0, y=279, width=40.0, height=30)
karakteristik3Entry = tk.Entry(bd=0, bg="#FFFFFF", highlightthickness=0,font=12)     #Karakteristik 3
karakteristik3Entry.place(x=1011.0, y=279, width=40.0, height=30)
karakteristik4Entry = tk.Entry(bd=0, bg="#FFFFFF", highlightthickness=0,font=12)     #Karakteristik 4
karakteristik4Entry.place(x=463.0, y=526, width=40.0, height=30)
karakteristik5Entry = tk.Entry(bd=0, bg="#FFFFFF", highlightthickness=0,font=12)     #Karakteristik 5
karakteristik5Entry.place(x=737.0, y=526, width=40.0, height=30)
karakteristik6Entry = tk.Entry(bd=0, bg="#FFFFFF", highlightthickness=0,font=12)     #Karakteristik 6
karakteristik6Entry.place(x=1011.0, y=526, width=40.0, height=30)

#Kumpulan Button
def btnPrintCertificate():
    namaLengkap = namaLengkapEntry.get()
    tanggalPemeriksaan = tanggalPemeriksaanEntry.get()
    kar1 = int(karakteristik1Entry.get())
    kar2 = int(karakteristik2Entry.get())
    kar3 = int(karakteristik3Entry.get())
    kar4 = int(karakteristik4Entry.get())
    kar5 = int(karakteristik5Entry.get())
    kar6 = int(karakteristik6Entry.get())

    if not namaLengkap:
        tk.messagebox.showerror(
            title="Data Kosong!", message="Tolong Masukan Nama Lengkap")
        return

    if not tanggalPemeriksaan:
        tk.messagebox.showerror(
            title="Data Kosong!", message="Tolong Masukan Tanggal Pemeriksaan!")
        return

    skorNilaiKarakteristik = kar1+kar2+kar3+kar4+kar5+kar6

    if -13 < skorNilaiKarakteristik <= -5:
        hasilPemeriksaan = "Over Supinated"
    elif -5 < skorNilaiKarakteristik <= -1:
        hasilPemeriksaan = "Supinated"
    elif -1 < skorNilaiKarakteristik <= 5 :
        hasilPemeriksaan = "Neutral"
    elif 5 < skorNilaiKarakteristik <= 9:
        hasilPemeriksaan = "Pronated"
    elif 9 < skorNilaiKarakteristik <= 12:
        hasilPemeriksaan = "Over Pronated"

    fillpdfs.get_form_fields("templateHasilTest.pdf")
    data_dict = {
        'namaLengkap': namaLengkap,
        'karakteristik1': str(kar1),
        'karakteristik2': str(kar2),
        'karakteristik3': str(kar3),
        'karakteristik4': str(kar4),
        'karakteristik5': str(kar5),
        'karakteristik6': str(kar6),
        'hasilPemeriksaan': hasilPemeriksaan,
        'tanggalPemeriksaan': tanggalPemeriksaan
    }
    fillpdfs.write_fillable_pdf('templateHasilTest.pdf', 'hasilTestRW.pdf', data_dict)

def btnConvertVideo2Image(): 
    directory = filedialog.askdirectory()
    filename=directory+"/output.mp4"
    vidcap = cv2.VideoCapture(filename)
    def getFrame(sec):
        vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*500)
        hasFrames,image = vidcap.read()
        if hasFrames:
            cv2.imwrite(directory+"/image"+str(count)+".jpg", image)
        return hasFrames
    sec = 0
    frameRate = 1.3
    count=1
    success = getFrame(sec)
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        success = getFrame(sec)
    print("Video Converted!!")

def btnClassify(self):
    self.title.pack_forget()
    self.menu.pack_forget()
    self.processMenu.pack_forget()
    directory = filedialog.askdirectory()
    FPIAnalysis(self.root, main_title=self.title, main_menu = self.menu, directory=directory, processMenu=self.processMenu)

def btnHardware():
    video = cv2.VideoCapture(0) # Create an object to read from camera

    if (video.isOpened() == False):         # We need to check if camera is opened previously or not
        print("Error reading video file")

    size = (1920,1080)
    result = cv2.VideoWriter('hasilVideo/output.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30, size)
    bluetoothTrigger()
    
    while(True):
        ret, frame = video.read()

        if ret == True:
            result.write(frame)
            resized = cv2.resize(frame, (960, 540))   
            cv2.imshow('Frame', resized)
            
            if cv2.waitKey(1) & 0xFF == ord('a'):
                break
        else:
            break

    video.release()
    result.release()
    cv2.destroyAllWindows() # Closes all the frames
    print("The video was successfully saved")

def bluetoothTrigger():
    ser = serial.Serial("COM6", 9600, timeout = 1)

    def retrieveData():
        ser.write(b'2')
        data = ser.readline().decode('ascii')
        return data
    
    print(retrieveData())

def updateImage():
    python = sys.executable
    os.execl(python, python, * sys.argv)

#Form Data Diri
canvas.create_rectangle(15.0, 84.0, 235.0, 260.0, fill="#EEEEEE", outline="")
canvas.create_rectangle(15.0, 84.0, 235.0, 126.0, fill="#3A7FF6", outline="")
canvas.create_text(69, 95, anchor="nw", text="Nama Lengkap", fill="#FFFFFF", font=("RobotoRoman Bold", 17*-1))
canvas.create_rectangle(15, 173, 235.0, 215.0, fill="#3A7FF6", outline="")
canvas.create_text(43, 184, anchor="nw", text="Tanggal Pemeriksaan", fill="#FFFFFF", font=("RobotoRoman Bold", 17*-1))
canvas.create_rectangle(22.0, 132.0, 230.0, 167.0, fill="#FFFFFF", outline="")
canvas.create_rectangle(22.0, 221.0, 230.0, 256.0, fill="#FFFFFF", outline="")
#Tombol Start Hardware
startHardwareButton = PhotoImage(file=relative_to_assets("startHardware.png"))
startHardware = Button(
    image=startHardwareButton,borderwidth=0,highlightthickness=0,
    command=btnHardware, relief="flat", cursor="hand2"
)
startHardware.place(x=15.0, y=275.0, width=220.0, height=45.0)

#Tombol Convert Video to Image
convertVid2ImButton = PhotoImage(file=relative_to_assets("convertVid2Im.png"))
convertVid2Im = Button(
    image=convertVid2ImButton, borderwidth=0, highlightthickness=0, 
    command=btnConvertVideo2Image, relief="flat", cursor="hand2"
)
convertVid2Im.place(x=15.0, y=335.0, width=220.0,height=45.0)

#Tombol Classification
classificationButton = PhotoImage(file=relative_to_assets("classification.png"))
classification = Button(
    image=classificationButton, borderwidth=0, highlightthickness=0,
    command=btnClassify, relief="flat", cursor="hand2"
)
classification.place(x=15.0, y=395.0, width=220.0, height=45.0)

#Tombol Print Certificate
printCertificateButton = PhotoImage(file=relative_to_assets("printCertificate.png"))
printCertificate = tk.Button(
    image=printCertificateButton, borderwidth=0, highlightthickness=0, 
    command=btnPrintCertificate, relief="flat", cursor="hand2"
)
printCertificate.place(x=15.0, y=455.0, width=220.0, height=45.0)

window.resizable(False, False)
window.mainloop()