# -*- coding: utf-8 -*-
"""
Created on Sun May  2 15:30:07 2021

@author: VAIO
"""

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import fitz
import cv2
from PIL import Image
import os
import pytesseract
import numpy as np

import csv
from itertools import zip_longest

from numba import njit, jit

root= tk.Tk()
root.title('CensoHospitales_Extractor')

canvas1 = tk.Canvas(root, width = 950, height = 320,  relief = 'raised')
canvas1.pack()

label1 = tk.Label(root, text='Segmentación de Tablas')
label1.config(font=('helvetica', 14))
canvas1.create_window(230, 25, window=label1)

label2 = tk.Label(root, text='Nombre del Archivo:')
label2.config(font=('helvetica', 10))
canvas1.create_window(75, 80, window=label2)

entry1 = tk.Entry (root) 
entry1.config(state='disabled')
canvas1.create_window(230, 80, window=entry1)

Filename = 'aux'

def seleccionarArchivo():
    global Filename
    root.filename =  filedialog.askopenfilename(initialdir = "",title = "Buscador")
    Filename = str(root.filename)
    entry1.config(state='normal')
    entry1.delete(0,"end")
    entry1.insert(0, Filename)
    entry1.config(state='disabled')
    

button2 = tk.Button(text='Abrir Archivo', command=seleccionarArchivo, bg='white', fg='black', font=('helvetica', 9, 'bold'))
canvas1.create_window(385, 80, window=button2)

label3 = tk.Label(root, text='Número de Página (PDF):')
label3.config(font=('helvetica', 10))
canvas1.create_window(80, 120, window=label3)

entry2 = tk.Entry (root) 
canvas1.create_window(230, 120, window=entry2)

label4 = tk.Label(root, text='Página (1,2):')
label4.config(font=('helvetica', 10))
canvas1.create_window(75, 160, window=label4)

entry3 = tk.Entry (root) 
entry3.insert(0, '1')
canvas1.create_window(230, 160, window=entry3)


label5 = tk.Label(root, text='Rotar:')
label5.config(font=('helvetica', 10))
canvas1.create_window(75, 200, window=label5)

entry4 = tk.Entry (root)
entry4.insert(0, '0')
canvas1.create_window(230, 200, window=entry4)


def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
 
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
 
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
 
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
 
    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))

@jit(nopython=True)
def find(r,c,img,mat):
    n = img.shape[1]
    p = int((r*n)+c)
    
    if mat[r][c] == p:
        return p
    else:
        r2 = int(mat[r][c]/n)
        c2 = int(mat[r][c]%n)
        
        mat[r][c] = find(r2,c2,img,mat)
        return mat[r][c]

@jit(nopython=True)
def union(r1,c1,r2,c2,img,mat):
    n = img.shape[1]
    pa = find(r1,c1,img,mat)
    pb = find(r2,c2,img,mat)
    
    raux = int(pa/n)
    caux = int(pa%n)
    
    mat[raux][caux] = int(pb)


@jit(nopython=True)
def uf(img,mat):
    n = img.shape[1]
    m = img.shape[0]
    c = 0
    
    for i in range (0,m):
        for j in range (0,n):
            mat[i][j] = int(c)
            c += 1 

    for i in range (0,m):
        for j in range (0,n):
            if j<n-1 and img[i][j] == img[i][j+1]:
                union(i,j,i,j+1,img,mat)
            if i<m-1 and img[i][j] == img[i+1][j]:
                union(i,j,i+1,j,img,mat)
            
    for i in range (0,m):
        for j in range (0,n):
            find(i,j,img,mat)


@jit(nopython=True)
def segmentar(m,n,x,mat,pts,XL,XH,YL,YH):
    
    for i in range(0,m):
        for j in range(0,n):
            for k in range (len(x)):
                if(mat[i][j] != 1000000 and mat[i][j] == pts[k]):
                    if XL[k] < i:
                        XL[k] = i                    
                    if XH[k] > i:
                        XH[k] = i
                    if YL[k] < j:
                        YL[k] = j                        
                    if YH[k] > j:
                        YH[k] = j



def Extraer():
    global Rotar
    
    PaginaPDF = int(entry2.get())-1
    Pagina = int(entry3.get())
    Angulo = int(entry4.get())
    
    pdffile = Filename
    doc = fitz.open(pdffile)
    page = doc.loadPage(PaginaPDF) #number of page
    
    #Mejorar la calidad de imagen (Mayor calidad = Mayor tamaño)
    zoom = 1    # zoom factor
    mat = fitz.Matrix(zoom, zoom)
    pix = page.getPixmap(matrix = mat)
    
    #Guardar la nueva imagen
    output = "outfile.png"
    pix.writePNG(output)

    #Mejorar la calidad de imagen (Mayor calidad = Mayor tamaño)
    zoom = 5    # zoom factor
    mat = fitz.Matrix(zoom, zoom)
    pix = page.getPixmap(matrix = mat)
    
    #Guardar la nueva imagen
    output = "outfileMax.png"
    pix.writePNG(output)

    if Angulo != 0:
        image = cv2.imread('outfile.png')
        image = rotate_bound(image, Angulo)
        cv2.imwrite('outfile.png', image)
        
        image2 = cv2.imread('outfileMax.png')
        image2 = rotate_bound(image2, Angulo)
        cv2.imwrite('outfileMax.png', image2)

    aux = cv2.imread('outfile.png')
    auxMax = cv2.imread('outfileMax.png')

    n = aux.shape[1]
    m = aux.shape[0]
    
    nMax = auxMax.shape[1]
    mMax = auxMax.shape[0]

    if Pagina == 1:
        aux = aux[0:m,0:int(n/2)]
        auxMax = auxMax[0:mMax,0:int(nMax/2)]
    else:
        aux = aux[0:m,int(n/2):n]
        auxMax = auxMax[0:mMax,int(nMax/2):nMax]
    
    cv2.imwrite('outfile.png', aux)
    
    im_gray = cv2.imread('outfile.png', cv2.IMREAD_GRAYSCALE)
    (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imwrite('bw_image.png', im_bw)    
    
    mat = np.zeros((im_bw.shape[0],im_bw.shape[1]))
    
    n = im_bw.shape[1]
    m = im_bw.shape[0]
    
    uf(im_bw,mat)
    
    for i in range (0,m):
        for j in range (0,n):
            if(im_bw[i][j] == 255):
                mat[i][j] = 1000000
    
    x = np.unique(mat)
    
    pts = []
    
    for k in range (len(x)):
        pts.append(x[k])
    
    XL = np.ones(len(x))*-100
    XH = np.ones(len(x))*1000000
    YL = np.ones(len(x))*-100
    YH = np.ones(len(x))*1000000
    
    segmentar(m,n,x,mat,pts,XL,XH,YL,YH)
    
    cont2 = 0
    for p,xl_,xh_,yl_,yh_ in zip(pts,XL,XH,YL,YH):
        if abs(yh_-yl_) > 15 and abs(xh_-xl_) > 15 and xh_ > 0 and xl_ > 0:
            cv2.imwrite(str(cont2) + '___hospital.png', auxMax[int(xh_)*5:int(xl_)*5, int(yh_)*5:int(yl_)*5])
            cont2 += 1
    
    messagebox.showinfo(title='Convertidor', message='Segmentación de Tablas Completada!')
    
button3 = tk.Button(text='Procesar', command=Extraer, bg='white', fg='black', font=('helvetica', 9, 'bold'))
canvas1.create_window(220, 250, window=button3)

'''------------'''

label6 = tk.Label(root, text='Extracción de Tablas')
label6.config(font=('helvetica', 14))
canvas1.create_window(680, 25, window=label6)

label7 = tk.Label(root, text='Nombre del Archivo:')
label7.config(font=('helvetica', 10))
canvas1.create_window(525, 80, window=label7)

entry5 = tk.Entry (root) 
entry5.config(state='disabled')
canvas1.create_window(680, 80, window=entry5)

Filename2 = 'aux'

def seleccionarArchivo():
    global Filename2
    root.filename =  filedialog.askopenfilename(initialdir = "",title = "Buscador")
    Filename2 = str(root.filename)
    entry5.config(state='normal')
    entry5.delete(0,"end")
    entry5.insert(0, Filename2)
    entry5.config(state='disabled')
    

button4 = tk.Button(text='Abrir Archivo', command=seleccionarArchivo, bg='white', fg='black', font=('helvetica', 9, 'bold'))
canvas1.create_window(835, 80, window=button4)

label8 = tk.Label(root, text='Columnas Dobles:')
label8.config(font=('helvetica', 10))
canvas1.create_window(525, 120, window=label8)

entry6 = tk.Entry (root) 
canvas1.create_window(680, 120, window=entry6)

label12 = tk.Label(root, text='Separar por comas')
label12.config(font=('helvetica', 10))
canvas1.create_window(850, 120, window=label12)

label10 = tk.Label(root, text='Columnas Texto:')
label10.config(font=('helvetica', 10))
canvas1.create_window(525, 160, window=label10)

entry7 = tk.Entry (root) 
canvas1.create_window(680, 160, window=entry7)

label11 = tk.Label(root, text='Separar por comas')
label11.config(font=('helvetica', 10))
canvas1.create_window(850, 160, window=label11)

label9 = tk.Label(root, text='Extracción 2:')
label9.config(font=('helvetica', 10))
canvas1.create_window(525, 210, window=label9)

Extraccion2 = tk.IntVar()
c2 = tk.Checkbutton(root,variable=Extraccion2, onvalue=1, offvalue=0)
c2.pack()
c2.place(x=620,y=200)

def rotar(im_bw, original, angT, ang):
    
    for i in range (0,360):
        
        image2 = rotate_bound(im_bw, angT)
        angT += ang
        
        n = image2.shape[1]
        m = image2.shape[0]
        
        for j in range(0,int(m/4)):
            if np.sum(image2[j]) > n*.90*255:
                cv2.imwrite('outfileRecta.png', image2)
                
                originalRotated = rotate_bound(original, angT-ang)
                cv2.imwrite('outfileOriginalRecta.png', originalRotated)
                
                return True, image2, originalRotated
    return False, None, None
    
def Extraer2():
    
    original = cv2.imread(Filename2)
    
    im_gray = cv2.imread(Filename2, cv2.IMREAD_GRAYSCALE)
    (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    im_bw =  cv2.bitwise_not(im_bw)

    angT = 0.0
    ang = 0.1

    flag, image2, originalRotated = rotar(im_bw, original, angT, ang)
    
    if flag:
        pass
    else:
        ang = -0.1
        flag, image2, originalRotated = rotar(im_bw, original, angT, ang)

    Final = cv2.imread('outfileOriginalRecta.png')

    m = image2.shape[0]
    n = image2.shape[1]
    
    lineas = []
    linea = 0
    prev = 0
    
    for j in range(0,m):
        if np.sum(image2[j]) > n*.75*255:
            if j > linea:
                prev = linea
                linea = j
                if linea - prev > 15:
                    lineas.append(prev)
    lineas.append(linea)
    print(lineas)
    
    if len(lineas) == 3:
        if(lineas[0] > 20):
            lineas.insert(0,0)
        elif(abs(lineas[len(lineas)-1]-m) > 30):
            lineas.insert(len(lineas),m)
        else:
            lineas.insert(0,0)
    elif len(lineas) == 2:        
        lineas.insert(0,0)
    elif len(lineas) == 1:
        if lineas[0] > 20:
            lineas.insert(0,0)
        if (abs(lineas[0]-m) < 30):
            lineas.insert(len(lineas),int(m*.08))
        
    print(lineas)
    encabezado = image2[lineas[1]:lineas[2],0:n]
    cv2.imwrite('encabezado.png',encabezado)
    mE = encabezado.shape[0]
    nE = encabezado.shape[1]
    
    columnas = np.sum(encabezado, axis=0)
    
    lineas2 = []
    lineas2.append(0)
    prev = 0
    
    for i in range(0,len(columnas)):
        if columnas[i] > mE*255*.95:
            if abs(i-prev) > 15:
                lineas2.append(i)
                prev = i
                
    cont = 0
    lineas2.append(len(columnas)-1)
    print(lineas2)
    
    columnaDoble = str(entry6.get()).replace(' ','').split(',')
    
    for i in range(0,len(lineas2)-1):
        if abs(lineas2[i]-lineas2[i+1]) > 25:
            if(len(lineas) > 3):
                
                if str(cont+1) in columnaDoble:

                    cv2.imwrite('columna' + str(cont) + '.png', originalRotated[lineas[2]:lineas[3],lineas2[i]:int((lineas2[i+1]+lineas2[i])/2)])
                    cont += 1
                    cv2.imwrite('columna' + str(cont) + '.png', originalRotated[lineas[2]:lineas[3],int((lineas2[i+1]+lineas2[i])/2):lineas2[i+1]])
                    
                    Final = cv2.line(Final,(int((lineas2[i+1]+lineas2[i])/2),lineas[2]),(int((lineas2[i+1]+lineas2[i])/2),lineas[3]),(0,0,0),2)
                    
                    columnaDobleAux = []
                    for value in columnaDoble:
                        columnaDobleAux.append(str(int(value)+1))
                    columnaDoble = columnaDobleAux
                    
                else:
                    cv2.imwrite('columna' + str(cont) + '.png', originalRotated[lineas[2]:lineas[3],lineas2[i]:lineas2[i+1]])
                if cont == 0:
                    cv2.imwrite('columnaaux.png', image2[lineas[2]:lineas[3],lineas2[i]:lineas2[i+1]])
            else:
                if str(cont+1) in columnaDoble:
                    #print(lineas2[i],int(lineas2[i+1]/2))
                    cv2.imwrite('columna' + str(cont) + '.png', originalRotated[lineas[2]:nE,lineas2[i]:int((lineas2[i+1]+lineas2[i])/2)])
                    cont += 1
                    #print(int(lineas2[i+1]/2),lineas2[i+1])
                    cv2.imwrite('columna' + str(cont) + '.png', originalRotated[lineas[2]:nE,int((lineas2[i+1]+lineas2[i])/2):lineas2[i+1]])

                    Final = cv2.line(Final,(int((lineas2[i+1]+lineas2[i])/2),lineas[2]),(int((lineas2[i+1]+lineas2[i])/2),nE),(0,0,0),2)

                    columnaDobleAux = []
                    for value in columnaDoble:
                        columnaDobleAux.append(str(int(value)+1))
                    columnaDoble = columnaDobleAux

                    
                else:
                    cv2.imwrite('columna' + str(cont) + '.png', originalRotated[lineas[2]:nE,lineas2[i]:lineas2[i+1]])
                if cont == 0:
                    cv2.imwrite('columnaaux.png', image2[lineas[2]:nE,lineas2[i]:lineas2[i+1]])

            cont += 1


    filas = []

    columna1 = cv2.imread('columnaaux.png')
    
    m = columna1.shape[0]
    n = columna1.shape[1]
        
    a = int((n/2)-(n/3))
    b = int((n/2)+(n/3))
    
    flagBlanco = False
    print(m,n)
    for i in range(0,m):
        if np.sum(columna1[i][a:b]) > 0:
            if flagBlanco == False:
                flagBlanco = True
                filas.append(i)
        else:
            if flagBlanco:
                flagBlanco = False
                #filas.append(i+3)
    
    print(filas)
    
    pytesseract.pytesseract.tesseract_cmd = '/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'
    
    columnaTexto = str(entry7.get()).replace(' ','').split(',')
    
    datos = []
    
    for i in range(0,cont):
        columna = cv2.imread('columna' + str(i) + '.png')
        
        n = columna.shape[1]
        
        listaAux = []
        
        for j in range(0,len(filas)-1):
            if filas[j+1]-filas[j] > 25:
                
                Final = cv2.line(Final,(0,filas[j]-3+lineas[2]),(Final.shape[1],filas[j]-3+lineas[2]),(0,0,0),2)
                
                if str(i+1) in columnaTexto:
                    
                    if  Extraccion2.get() == 1:
                        cv2.imwrite('celda.png',columna[filas[j]-3:filas[j+1],5:n-5])
#                        cv2.imshow('x', columna[filas[j]-3:filas[j+1],5:n-5])
#                        cv2.waitKey(0)
                        im_gray = cv2.imread('celda.png', cv2.IMREAD_GRAYSCALE)
                        (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY)
                        cv2.imwrite('celda.png',im_bw)
                        text = pytesseract.image_to_string(Image.open('celda.png'), lang='spa').replace('  |','').replace(' |','').replace('|','')
                    else:
                        cv2.imwrite('celda.png',columna[filas[j]-3:filas[j+1],5:n-5])
                        text = pytesseract.image_to_string(Image.open('celda.png'), lang='spa').replace('  |','').replace(' |','').replace('|','')
                    
                else:
                    
                    if Extraccion2.get() == 1:
                        cv2.imwrite('celda.png',columna[filas[j]-3:filas[j+1],15:n-10])
#                        cv2.imshow('x', columna[filas[j]-3:filas[j+1],5:n-15])
#                        cv2.waitKey(0)
                        im_gray = cv2.imread('celda.png', cv2.IMREAD_GRAYSCALE)
                        (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY)
                        cv2.imwrite('celda.png',im_bw)
                        text = pytesseract.image_to_string(Image.open('celda.png'), lang='spa',config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
                    else:
                        cv2.imwrite('celda.png',columna[filas[j]-3:filas[j+1],15:n-10])
                        text = pytesseract.image_to_string(Image.open('celda.png'), lang='spa',config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
                        
                if len(text) == 0 or text == '':
                    text = '.'
                    
                listaAux.append(text)                    
                
        datos.append(listaAux)
#            if filas[j+1]-filas[j] > 20:
#                cv2.imshow('x',columna[filas[j]-3:filas[j+1],5:n-15])
#                cv2.waitKey(0)
    
    
    export_data = zip_longest(*datos, fillvalue = '')
    with open(Filename2[:-4] + '.csv', 'w', newline='') as file:
          write = csv.writer(file)
          write.writerow(("","","","","","","","","","","","",""))
          write.writerows(export_data)
    
    cv2.imwrite('Final.png',Final)
    messagebox.showinfo(title='Convertidor', message='Segmentación por columnas completada!')    
    
button5 = tk.Button(text='Procesar', command=Extraer2, bg='white', fg='black', font=('helvetica', 9, 'bold'))
canvas1.create_window(690, 260, window=button5)

root.lift()
root.mainloop()