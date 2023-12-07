import cv2
import numpy as np
import sys

# Guarda las coordenadas en un archivo de texto
def envio_coordenadas(x_azul, y_azul, x_rojo, y_rojo, x_amarillo, y_amarillo, x_verde, y_verde):
    with open("coordenadas.txt", "w") as f:
        f.write(str(x_azul))
        f.write(",")
        f.write(str(y_azul))
        f.write(",")
        f.write(str(x_rojo))
        f.write(",")
        f.write(str(y_rojo))
        f.write(",")
        f.write(str(x_amarillo))
        f.write(",")
        f.write(str(y_amarillo))
        f.write(",")
        f.write(str(x_verde))
        f.write(",")
        f.write(str(y_verde))
        

# Argumentos: imagen binaria mask, color bgr para los contornos y frame
def dibujar_rojo(mask,color):
  # Se buscan los contornos de la imagen binaria
  contornos,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
      cv2.CHAIN_APPROX_SIMPLE)
  
  # Inicializacion de variables globales con coordenadas del objeto rojo
  global x_pos_rojo, y_pos_rojo
  x_pos_rojo = 0 
  y_pos_rojo = 0
  
  for c in contornos: # Recorre cada uno de los contornos
    area = cv2.contourArea(c) # Determina el área del contorno
    if area > 5000: # Se verifica si el área es mayor a 5000 para no tomar objetos pequeños
      # Se determinan las coordenadas centrales del contorno
      M = cv2.moments(c) 
      if (M["m00"]==0): M["m00"]=1
      x = int(M["m10"]/M["m00"])
      y = int(M['m01']/M['m00'])
      
      x_pos_rojo, y_pos_rojo = x, y # Guarda las coordenadas del objeto rojo

      # Obtencion del convexHull del contorno, lo que permite obtener un contorno más suave
      nuevoContorno = cv2.convexHull(c)
      
      # Se dibuja el circulo en el punto central del contorno y se escriben las coordenadas
      cv2.circle(frame,(x,y),7,(0,255,0),-1)
      cv2.putText(frame,'{},{}'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
      cv2.drawContours(frame, [nuevoContorno], 0, color, 3)
      
def dibujar_azul(mask,color):
  contornos,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
      cv2.CHAIN_APPROX_SIMPLE)
  
  # Inicializacion de variables globales con coordenadas del objeto azul
  global x_pos_azul, y_pos_azul
  x_pos_azul = 0 
  y_pos_azul = 0
  
  
  for c in contornos:
    area = cv2.contourArea(c)
    # print("area azul", area)
    if area > 1700:
      M = cv2.moments(c)
      if (M["m00"]==0): M["m00"]=1
      x = int(M["m10"]/M["m00"])
      y = int(M['m01']/M['m00'])
      
      x_pos_azul, y_pos_azul = x, y # Guarda las coordenadas del objeto azul

      nuevoContorno = cv2.convexHull(c)
      cv2.circle(frame,(x,y),7,(0,255,0),-1)
      cv2.putText(frame,'{},{}'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
      cv2.drawContours(frame, [nuevoContorno], 0, color, 3)

def dibujar_verde(mask,color):
  contornos,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
      cv2.CHAIN_APPROX_SIMPLE)
  
  # Inicializacion de variables globales con coordenadas del objeto azul
  global x_pos_verde, y_pos_verde
  x_pos_verde = 0 
  y_pos_verde = 0
  
  for c in contornos:
    area = cv2.contourArea(c)
    if area > 500:
      M = cv2.moments(c)
      if (M["m00"]==0): M["m00"]=1
      x = int(M["m10"]/M["m00"])
      y = int(M['m01']/M['m00'])
      
      x_pos_verde, y_pos_verde = x, y # Guarda las coordenadas del objeto azul

      nuevoContorno = cv2.convexHull(c)
      cv2.circle(frame,(x,y),7,(0,255,0),-1)
      cv2.putText(frame,'{},{}'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
      cv2.drawContours(frame, [nuevoContorno], 0, color, 3)
      
      
def dibujar_amarillo(mask,color):
  contornos,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
      cv2.CHAIN_APPROX_SIMPLE)
  
  # Inicializacion de variables globales con coordenadas del objeto azul
  global x_pos_amarillo, y_pos_amarillo
  x_pos_amarillo = 0 
  y_pos_amarillo = 0
  
  for c in contornos:
    area = cv2.contourArea(c)
    if area > 2000:
      M = cv2.moments(c)
      if (M["m00"]==0): M["m00"]=1
      x = int(M["m10"]/M["m00"])
      y = int(M['m01']/M['m00'])
      
      x_pos_amarillo, y_pos_amarillo = x, y # Guarda las coordenadas del objeto azul

      nuevoContorno = cv2.convexHull(c)
      cv2.circle(frame,(x,y),7,(0,255,0),-1)
      cv2.putText(frame,'{},{}'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
      cv2.drawContours(frame, [nuevoContorno], 0, color, 3)


cap = cv2.VideoCapture(0)
# --- Arreglos con valores para espacio de color HSV -----------------

# Rango del color Amarillo en HSV
amarilloBajo = np.array([15,200,20],np.uint8) 
amarilloAlto = np.array([45,255,255],np.uint8)

# Rango del color Azul en HSV
azulBajo = np.array([100,100,20],np.uint8)
azulAlto = np.array([125,255,255],np.uint8)

# Rango del color Verde en HSV
verdeBajo = np.array([42,50,20],np.uint8)
verdeAlto = np.array([65,255,255],np.uint8)

# Rango del color Rojo en HSV
redBajo1 = np.array([0, 50, 50], np.uint8)
redAlto1 = np.array([10, 255, 255], np.uint8)
redBajo2 = np.array([160, 50, 50], np.uint8)
redAlto2 = np.array([179, 255, 255], np.uint8)
font = cv2.FONT_HERSHEY_SIMPLEX


# -- Ciclo infinito con el juego -------------------------------------
try:
    while True:
        # Retorna un booleano si el frame es leído correctamente o no
        ret,frame = cap.read()
        
        # Si el frame es leído correctamente, ret es True
        if not ret:
            print("No se puede recibir frame, cerrando...")
            break
        
        
        """
        ----------------------------------------------------------------
        -- Conversión de espacio de color y detección de colores -------
        ----------------------------------------------------------------
        """
        # -- Conversión de espacio de color BGR a HSV --------------------
        frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        
        # -- Binarizacion del frame HSV con rango de color rojo y amarillo --
        maskAzul = cv2.inRange(frameHSV,azulBajo,azulAlto)
        maskVerde = cv2.inRange(frameHSV,verdeBajo,verdeAlto)
        maskAmarillo = cv2.inRange(frameHSV,amarilloBajo,amarilloAlto)
        maskRed1 = cv2.inRange(frameHSV,redBajo1,redAlto1)
        maskRed2 = cv2.inRange(frameHSV,redBajo2,redAlto2)
        
        # Suma de máscaras de los dos rangos de rojo
        maskRed = cv2.add(maskRed1,maskRed2)
        
        # -- Funciones de dibujo para obtener contorno y coordenadas -----
        dibujar_azul(maskAzul,(255,0,0))
        dibujar_verde(maskVerde, (0, 255, 0))
        dibujar_amarillo(maskAmarillo,(0,255,255))
        dibujar_rojo(maskRed,(0,0,255))
        
        # Cambia el tamaño del frame
        frame = cv2.resize(frame, (500, 300))
        
        # Dibuja la línea para separar el centro del vídeo
        cv2.line(frame, (250, 0), (250, 300), (255, 0, 45), thickness = 2)
        cv2.line(frame, (0, 150), (500, 150), (255, 0, 45), thickness = 2)
    
        
        # -- Muestra la imagen con los contornos detectados en una ventana --
        cv2.imshow('frame', frame)
        
        # Obtencion y envio de coordenadas
        envio_coordenadas(x_pos_azul, y_pos_azul, 
                          x_pos_rojo, y_pos_rojo, 
                          x_pos_amarillo, y_pos_amarillo, 
                          x_pos_verde, y_pos_verde)
        
        
        
        if cv2.waitKey(1) & 0xFF == ord('s'):
          break
    
# Cerrado de cámara
except KeyboardInterrupt:
    # quit
    cap.release()
    cv2.destroyAllWindows()
    sys.exit() 