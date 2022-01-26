import fitz
import cv2
import numpy as np

'''Recibe como parámetro la imagen de los datos'''
def dividir(_img):

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
    path = 'C:\\Users\\VAIO\\ML\\Dataset Anuarios\\c_v_'
    
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
                #print('')
                column_total = (j-indexrow)*255
                #se segmenta la fila
                img_col_aux = np.sum(thresh1[indexrow:j,0:width],axis=0)
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
                                cv2.imwrite(path + str(cont) + '.png', _img[indexrow-2:j+2,index:i])
#                                cv2.imshow('x', _img[indexrow-2:j+2,index:i])
#                                cv2.waitKey(0)
#                                cv2.destroyAllWindows()

                                #Testeo(0, path + str(cont) + '.png')
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
    
            flag = False
            index = 0

#    cv2.imshow('x', thresh1)
#    cv2.imwrite('x.png', thresh1)
#    cv2.waitkey(0)

img = cv2.imread("C:/Users/VAIO/ML/dataset.png")



'''---------------------------------'''
'''Se crea una imagen con escala de 5 de la página del PDF indicada'''
'''IMPORTANTE: Mantener el zoom de 5 para integridad del dataset'''
def escalar():
    
    
    pdffile = "C:\\Users\\VAIO\\Desktop\\Archivomex2\\702825140564_4.pdf"
    doc = fitz.open(pdffile)
    page = doc.loadPage(30) #number of page
    
    
    #Mejorar la calidad de imagen (Mayor calidad = Mayor tamaño)
    zoom = 5    # zoom factor
    mat = fitz.Matrix(zoom, zoom)
    pix = page.getPixmap(matrix = mat)
    
    #Guardar la nueva imagen
    output = "dataset.png"
    pix.writePNG(output)



'''-------------------------------'''

escalar() 
dividir(img)
