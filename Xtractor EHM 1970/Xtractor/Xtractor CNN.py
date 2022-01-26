import fitz
import cv2
import numpy as np

from numba import njit, jit

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

import csv
from itertools import zip_longest

#
convNN = load_model('C:/Users/VAIO/ML/ALPR/red2.h5')

root= tk.Tk()
root.title('ArchivoMex_Xtractor')

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

label3 = tk.Label(root, text='Número de Página:')
label3.config(font=('helvetica', 10))
canvas1.create_window(80, 120, window=label3)

entry2 = tk.Entry (root) 
canvas1.create_window(230, 120, window=entry2)

label4 = tk.Label(root, text='Sensibilidad')
label4.config(font=('helvetica', 10))
canvas1.create_window(75, 160, window=label4)

entry3 = tk.Entry (root) 
entry3.insert(0, '65')
canvas1.create_window(230, 160, window=entry3)


def Testeo(nimg, path):
    
    global convNN
    
    test2_img = np.zeros((nimg+1,30,15))
        
    for i in range(0, nimg+1):
        img = load_img(path)
        x = img_to_array(img)
        x = x[:,:,0]
        res = cv2.resize(x,(15,30))
        test2_img[i] = res
    
    test2_img = test2_img.reshape((nimg+1,30,15,1))
    test2_img = test2_img.astype('float32') / 255.
    
    predictions = convNN.predict(test2_img)
    Y_ = np.argmax(predictions, 1)
    
    return Y_

'''Recibe como parámetro la imagen de los datos'''

def dividir(_img):

#    cv2.imshow('x', _img)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()

    
    #tomar un solo canal de la imagen
    img = _img[:,:,0]
    
    #convertir a blanco y negro
    ret,thresh1 = cv2.threshold(img,125,255,cv2.THRESH_BINARY)
    
    #dimensiones de la imagen
    height = thresh1.shape[0]
    width = thresh1.shape[1]
    
    #definir tamaño de las lineas blancas
    column_total = height*255
    row_total = width*255
    
    #obtener la suma de cada columna y fila en la imagen
    img_col_aux = np.sum(thresh1,axis=0)
    img_row_aux = np.sum(thresh1,axis=1)
    
    
    flag = False
    flagrow = False
    index = 0
    indexrow = 0
    
    cont = 0
    
    flagIncomplete = False
    indexInc = 0
    
    #en el path indicar el prefijo de las imagenes para evitar sobreescribir
    path = 'C:\\Users\\VAIO\\ML\\'
    
    listaaux = []
    
    #iterar la imagen por filas
    for j in range(0, height):
        
        #se detecta si comienza una fila verificando si tiene pixeles negros 
        if img_row_aux[j] != row_total:
            #flagrow nos indica cuando comienza la fila
            if flagrow == False:
                flagrow = True
                indexrow = j
        #si la fila no tiene pixeles negros...
        else:
            #pero tenemos flag de que comenzó una fila, significa que termina de segmentar la fila
            if flagrow:
                flagrow = False
                #print(j,indexrow) #coordenadas donde comienza la fila
                column_total = (j-indexrow)*255
                #se segmenta la fila
                img_col_aux = np.sum(thresh1[indexrow:j,0:width],axis=0)
                                
                texto = ''
                
                #se itera esa segmentacion por columnas
                for i in range (0, width):
                    #si la columna tiene pixeles negros, significa que comienza a segmentar una caracter
                    if img_col_aux[i] != column_total:
                        if flag == False:
                            flag = True
                            index = i
                    #si la fila no tiene pixeles negros, termina la segmentacion
                    else:
                        if flag:
                            flag = False
                            #si el segmento tiene un ancho 'considerable' se agrega al dataset
                            if (i-index) > 6:
                                if j+2 > 0 and indexrow-2 > 0 and i > 0 and index > 0:
                                    cv2.imwrite(path + str(cont) + '.png', _img[indexrow-2:j+2,index:i])
                                    #cv2.imshow('x', _img[indexrow-2:j+2,index:i])
                                    #cv2.waitKey(0)
                                    #cv2.destroyAllWindows()
                                    
                                    result = Testeo(0, path + str(cont) + '.png')
                                    
                                    if result is not None:
                                        texto = texto + str(result[0])
                                        
                                    cont += 1
                            
                            #este segmento de codigo sirve para pegar dos segmentos pequeños, completando caracteres
#                            if (i-index) < 9:
#                                if flagIncomplete:
#                                    if i-indexInc > 0:
##                                        cv2.imshow('x', thresh1[indexrow-2:j+2,indexInc:i])
##                                        cv2.waitKey(0)
##                                        cv2.destroyAllWindows()
#
#                                        cv2.imwrite('C:\\Users\\VAIO\\ML\\Dataset Anuarios\\z_' + str(cont) + '.png', _img[indexrow-2:j+2,indexInc:i])        
#                                        cont += 1
#                                    flagIncomplete = False
#                                else:
#                                    flagIncomplete = True
#                                    indexInc = index

                listaaux.append(texto)
    
            flag = False
            index = 0
        

#    cv2.imshow('x', thresh1)
#    cv2.imwrite('x.png', thresh1)
#    cv2.waitkey(0)
    print(listaaux)
    print()
    return listaaux


#img = cv2.imread("C:/Users/VAIO/ML/dataset.png")

#dividir(img)
#segmentar(img)


'''-------------------------------'''

@jit(nopython=True)
def lines(thresh1, Sensibilidad):

    #dimensiones de la imagen
    height = thresh1.shape[0]
    width = thresh1.shape[1]
        
    listadirectriz = []

    for i in range(0, height-20):
        
        img_crop = thresh1[i:i+20,0:width]
        img_crop_col_aux = np.sum(img_crop,axis=0)
        
        c = 0
        for k in range(0, width):
            if img_crop_col_aux[k] < 255*20:
                c +=1
        
        if c > width*Sensibilidad:
            listadirectriz.append(i)
            
        c = 0
        
    return listadirectriz


lineas = []

def revisar():
    global lineas
    
    pdffile = Filename
    doc = fitz.open(pdffile)
    
    Pagina = int(entry2.get())-1
    Sensibilidad = int(entry3.get())/100
    
    page = doc.loadPage(Pagina) #number of page
    
    #Mejorar la calidad de imagen (Mayor calidad = Mayor tamaño)
    zoom = 5    # zoom factor
    mat = fitz.Matrix(zoom, zoom)
    pix = page.getPixmap(matrix = mat)
    
    #Guardar la nueva imagen
    output = "dataset.png"
    pix.writePNG(output)

    _img = cv2.imread("dataset.png")

    #tomar un solo canal de la imagen
    img = _img[:,:,0]
    
    #convertir a blanco y negro
    ret,thresh1 = cv2.threshold(img,125,255,cv2.THRESH_BINARY)
    
    cv2.imwrite('res.png', thresh1)
    
    #dimensiones de la imagen
    height = thresh1.shape[0]
    width = thresh1.shape[1]
    
    tablas = []
    
    listadirectriz = lines(thresh1, Sensibilidad)

    for k in range(0, len(listadirectriz)-1):
        if abs(listadirectriz[k] - listadirectriz[k+1])  > 25:
            tablas.append(listadirectriz[k])
            
    tablas.append(listadirectriz[len(listadirectriz)-1])
    
    print(tablas)
    
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    fontScale              = 2
    fontColor              = (0,0,255)
    lineType               = 6
    
    c = 1
    for t in tablas:
        cv2.line(_img,(0,t),(width,t),(0,255,0), 10)
        if c%2 != 0:
            cv2.putText(_img, str(c), (0,t), font, fontScale, fontColor, lineType)
        else:
            cv2.putText(_img, str(c), (width-50,t), font, fontScale, fontColor, lineType)
        c += 1
    
    lineas = tablas
    
    cv2.imwrite('lines.png', _img)
    
    result = cv2.resize(_img, (400,600))
    cv2.imshow('x', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    messagebox.showinfo(title='Convertidor', message='Segmentación de Tablas Completada!')


button3 = tk.Button(text='Procesar', command=revisar, bg='white', fg='black', font=('helvetica', 9, 'bold'))
canvas1.create_window(220, 210, window=button3)

label7 = tk.Label(root, text='Extracción de Tablas')
label7.config(font=('helvetica', 14))
canvas1.create_window(680, 25, window=label7)

label5 = tk.Label(root, text='Fila inicial:')
label5.config(font=('helvetica', 10))
canvas1.create_window(525, 80, window=label5)

entry4 = tk.Entry (root) 
entry4.insert(0, '')
canvas1.create_window(680, 80, window=entry4)

label6 = tk.Label(root, text='Fila final:')
label6.config(font=('helvetica', 10))
canvas1.create_window(525, 120, window=label6)

entry5 = tk.Entry (root) 
entry5.insert(0, '')
canvas1.create_window(680, 120, window=entry5)


@jit(nopython=True)
def linesVertical(thresh1, Sensibilidad):

    #dimensiones de la imagen
    height = thresh1.shape[0]
    width = thresh1.shape[1]
        
    listadirectriz = []

    for i in range(0, width-10):
        
        img_crop = thresh1[0:height,i:i+10]
        img_crop_row_aux = np.sum(img_crop,axis=1)
        
        c = 0
        for k in range(0, height):
            if img_crop_row_aux[k] < 255*10:
                c +=1
        
        if c > height*Sensibilidad:
            listadirectriz.append(i)
            
        c = 0
        
    return listadirectriz

def extraccion():
    global lineas
    
    Inicial = int(entry4.get())-1
    Final = int(entry5.get())-1

    img = cv2.imread("dataset.png")

    height = img.shape[0]
    width = img.shape[1]

    _img = img.copy()

    print(lineas)

    if Final == -1:
        _img = img[lineas[Inicial]:height,0:width]

        height = _img.shape[0]

        _img_crop = _img[:,:,0]

        ret,thresh1 = cv2.threshold(_img_crop,125,255,cv2.THRESH_BINARY)

        img_crop_row_aux = np.sum(thresh1,axis=1)

        for j in range(height-1, 0, -1):
            if img_crop_row_aux[j] < width*255:
                _img = _img[0:j+10,0:width]
                break
            
    else:
        _img = img[lineas[Inicial]:lineas[Final],0:width]

    height = _img.shape[0]
    width = _img.shape[1]
                
    _img_crop = _img[:,:,0]
    
    ret,thresh1 = cv2.threshold(_img_crop,125,255,cv2.THRESH_BINARY)

    listadirectriz = linesVertical(thresh1, 0.8)
    
    tablas = []
    
    for k in range(0, len(listadirectriz)-1):
        if abs(listadirectriz[k] - listadirectriz[k+1])  > 25:
            tablas.append(listadirectriz[k])
            
    tablas.append(listadirectriz[len(listadirectriz)-1])
    
    print(tablas)
        
#    for t in tablas:
#        cv2.line(_img,(t,0),(t,height),(0,255,0), 10)
        
    cv2.imwrite('lines.png', _img)

    datos = []

    for i in range(0, len(tablas)):
        if i == len(tablas)-1:
            texto = dividir(_img[0:height,tablas[i]+10:width-10])
            datos.append(texto)
#            cv2.imwrite('x.png', _img[0:height,tablas[i]:width])
#            cv2.imshow('x', _img[0:height,tablas[i]:width])
#            cv2.waitKey(0)
#            cv2.destroyAllWindows()
        else:
            texto = dividir(_img[10:height-10,tablas[i]+10:tablas[i+1]-10])
            datos.append(texto)
#            cv2.imwrite('x.png', _img[0:height,tablas[i]:tablas[i+1]])
#            cv2.imshow('x', _img[0:height,tablas[i]:tablas[i+1]])
#            cv2.waitKey(0)
#            cv2.destroyAllWindows()
        
    
#    result = cv2.resize(_img, (400,600))
#    cv2.imshow('x', result)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()

    print(datos)
    export_data = zip_longest(*datos, fillvalue = '')
    with open('Result.csv', 'w', newline=None) as file:
          write = csv.writer(file)
          write.writerow(("","","","","","","","","","","","",""))
          write.writerows(export_data)
    
    messagebox.showinfo(title='Convertidor', message='Extracción Completada!')



button4 = tk.Button(text='Procesar', command=extraccion, bg='white', fg='black', font=('helvetica', 9, 'bold'))
canvas1.create_window(690, 170, window=button4)
    
root.lift()
root.mainloop()