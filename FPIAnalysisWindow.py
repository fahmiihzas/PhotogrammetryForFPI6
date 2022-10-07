import tkinter as tk
from PIL import ImageTk, Image
from Analysis import analysis1, analysis2, analysis3, analysis4, analysis5, analysis6
import pyvista as pv
from pyvista import examples
import numpy as np
from vtk import vtkRenderWindowInteractor
from tkinter import ttk

classify_img = []

class FPIAnalysis(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        global analysis_image

        self.directory = kwargs['directory']

        self.analysis_image = [
            0, #not defined, dummy
            self.directory+"/belakangk3.png",
            self.directory+"/belakangk3.png",
            0, #not defined, dummy
            self.directory+"/samping.png",
            self.directory+"/belakangk3.png"
        ]

        self.main_menu = kwargs['main_menu']
        self.main_title = kwargs['main_title']
        self.processMenu = kwargs['processMenu']
        self.quitBtn = tk.Button(master=root, text="Back", command=self.quit)
        self.quitBtn.pack(side="top", fill="x")


        self.index_result = [
            analysis1.process(self.directory),
            analysis2.process(self.directory),
            analysis3.process(self.directory),
            analysis4.process(self.directory),
            analysis5.process(self.directory),
            analysis6.process(self.directory)

        ]

        root.title("Classification Window")

        #left right frame
        self.left = tk.Frame(root)
        self.left.pack(side="left")
        self.right = tk.Frame(root)
        self.right.pack(side="right")

        #sub frame in every left and right
        score = tk.Frame(self.left)
        score.pack()
        criteria = tk.Frame(self.right)
        criteria.pack()

        def findConclusion(value):
            if (value in range(-12, -4)):
                return "Postur kaki: Supinasi berlebih"
            elif (value in range(-4, 0)):
                return "Postur kaki: Supinasi ringan"
            elif (value in range(0, 6)):
                return "Postur kaki: Normal"
            elif (value in range(6, 10)):
                return "Postur kaki: Pronasi ringan"
            elif (value in range(10, 13)):
                return "Postur kaki: Pronasi berlebih"
            else:
                return "Kesimpulan tidak dapat diambil"

        #detailed components in score frame
        currentAnalysisLabel = tk.Label(score, text="Nama", background="blue", fg="white", height=1, width=10)
        currentAnalysisLabel.pack()
        currentAnalysisValue = tk.Label(score, text=self.directory.split('/')[-1])
        currentAnalysisValue.pack()
        br = tk.Label(score, text="\n", height=1)
        br.pack()
        scoreLabel = tk.Label(score, text="Total Skor", background="blue", fg="white", height=1, width=10)
        scoreLabel.pack(side="top")
        scoreValue = tk.Label(score, text=sum(self.index_result))
        scoreValue.pack()
        br = tk.Label(score, text="\n", height=1)
        br.pack()
        conclusionLabel = tk.Label(score, text="Kesimpulan", background="blue", fg="white", height=1, width=10)
        conclusionLabel.pack()
        conclusionValue = tk.Label(score, text=findConclusion(sum(self.index_result)))
        conclusionValue.pack()

        criteriaLabel = tk.Label(criteria, text="Kriteria")
        criteriaLabel.pack()

        for i in range (6):
            if(i%3 == 0):
                criteriaLoc = tk.Frame(criteria)
                criteriaLoc.pack()
                separator = ttk.Separator(criteriaLoc, orient='horizontal')
                separator.pack(fill='x', pady=15)


            criteriaType = tk.Frame(criteriaLoc, background="white", width=250, height=250)
            if (i==2 or i==5):    
                criteriaType.pack(side="right", fill="y")
            else:
                criteriaType.pack(side="left", fill="y")
            self.createAnalysis(criteriaType, i)

    #detailed components in criteria frame
    def createAnalysis(self, criteriaType, i):
        global classify_img
        criteriaSublabel = tk.Label(criteriaType, text=f"{i+1} Analysis", background="white")
        criteriaSublabel.pack()
        if(i not in [0, 3]):
            image = Image.open(self.analysis_image[i]).resize((250, 190), Image.ANTIALIAS) #not defined, dummy
            image = ImageTk.PhotoImage(image)
            classify_img.append(image)
            criteriaImage = tk.Label(criteriaType, image=classify_img[i])
            criteriaImage.pack()
        else:
            classify_img.append(0)
            btn = tk.Button(criteriaType, text="Open 3D", height=9)
            if(i==0):
                btn = tk.Button(criteriaType, text="Open 3D", command=lambda: analysis1.show(self.directory))
            elif(i==3):
                btn = tk.Button(criteriaType, text="Open 3D", command=lambda: analysis4.show(self.directory))
            btn.pack(expand=True, fill="y")
        criteriaScore = tk.Label(criteriaType, width=7, text=self.index_result[i])
        criteriaScore.pack()


    def quit(self):
        self.left.pack_forget()
        self.right.pack_forget()
        self.quitBtn.pack_forget()
        self.main_title.pack()
        self.main_menu.pack(fill = 'both', expand = True, padx = 50, pady = 100)
        self.processMenu.pack()

        return False