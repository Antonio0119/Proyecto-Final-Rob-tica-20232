import tkinter as tk
import ControlDobot as cd
import serial
import struct
import time
import os
import binascii
class DobotApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.ejecucion = True
        self.color_seleccionado = None
        self.contenedor = None
        self.estado_detener = None
        self.aux_estado = [0,0,0,0]
        self.aux_cuadrante = True
        self.offset_x = 68
        self.offset_y = 90

        # Coordenadas x, y para tapa de color azul
        self.x_pos_azul = 0
        self.y_pos_azul = 0

        # Coordenadas x, y para tapa de color amarillo
        self.x_pos_amarillo = 0
        self.y_pos_amarillo = 0

        # Coordenadas x, y para tapa de color verde
        self.x_pos_verde = 0
        self.y_pos_verde = 0

        # Coordenadas x, y para tapa de color rojo
        self.x_pos_rojo = 0
        self.y_pos_rojo = 0

        # Definicion del frame maestro y contenedores 1 y 2
        self.master = master
        self.master.geometry("540x510")
        self.config(width=700, height=800)
        
        self.container_frame = tk.LabelFrame(self.master, text="Controles", width=200, height=100)
        self.container_frame.pack(padx=15, pady=15)
        
        self.container_frame2 = tk.LabelFrame(self.master, text="Estados", width=200, height=100)
        self.container_frame2.pack( padx=5, pady=5)
        
        self.create_widgets()
        
    # Funcion para crear los widgets de la interfaz.
    def create_widgets(self):
        self.colores = ['Tapa Roja', 'Tapa Verde', 'Tapa Azul', 'Tapa Amarilla']
        self.contenedores = ['Contenedor 1', 'Contenedor 2', 'Contenedor 3', 'Contenedor 4']
        
        self.main_label = tk.Label(self.master, text="Interfaz del Dobot Clasificador de Elementos por Color",
                               font=("Arial", 12, "bold"), width=45, height=3)

       
        self.filas = [0, 1, 2, 3, 4, 5, 6]
        tk.Label(self.container_frame, text="Seleccionar Contenedor:").grid(row=self.filas[0], column=0, padx=10)
        
        #Controles contenedores
        self.contenedor1 = tk.Button(self.container_frame, text="Contenedor 1", width=10, height=2, command=lambda: self.guardar_contenedor("contenedor 1"))
        self.contenedor1.grid(row=self.filas[0], column=1, padx=1, pady=(10,1))

        self.contenedor2 = tk.Button(self.container_frame, text="Contenedor 2", width=10, height=2, command=lambda: self.guardar_contenedor("contenedor 2"))
        self.contenedor2.grid(row=self.filas[0], column=2, padx=(1,10), pady=(10,1))

        self.contenedor3= tk.Button(self.container_frame, text="Contenedor 3", width=10, height=2, command=lambda: self.guardar_contenedor("contenedor 3"))
        self.contenedor3.grid(row=self.filas[1], column=1, padx=1, pady=1)

        self.contenedor4 = tk.Button(self.container_frame, text="Contenedor 4", width=10, height=2, command=lambda: self.guardar_contenedor("contenedor 4"))
        self.contenedor4.grid(row=self.filas[1], column=2, padx=(1,10), pady=1)
        
        
        #Controles tapas
        tk.Label(self.container_frame, text="Seleccionar Color:").grid(row=self.filas[2], column=0, padx=10, pady=10)
        self.tapa_roja = tk.Button(self.container_frame, text="Tapa Roja", width=10, height=2, command=lambda: self.guardar_color("roja"))
        self.tapa_roja.grid(row=self.filas[2], column=1, padx=1, pady=(10,1))

        self.tapa_verde = tk.Button(self.container_frame, text="Tapa Verde", width=10, height=2, command=lambda: self.guardar_color("verde"))
        self.tapa_verde.grid(row=self.filas[2], column=2, padx=(1,10), pady=(10,1))

        self.tapa_azul = tk.Button(self.container_frame, text="Tapa Azul", width=10, height=2, command=lambda: self.guardar_color("azul"))
        self.tapa_azul.grid(row=self.filas[3], column=1, padx=1, pady=1)

        self.tapa_amarilla = tk.Button(self.container_frame, text="Tapa Amarilla", width=10, height=2, command=lambda: self.guardar_color("amarilla"))
        self.tapa_amarilla.grid(row=self.filas[3], column=2, padx=(1,10), pady=1)

        #Botones de acción 
        self.bt_ejecutar = tk.Button(self.container_frame, text="Ejecutar", width=10, height=2, command=lambda: self.parametros_dobot())
        self.bt_ejecutar.grid(row=self.filas[4], column=0, pady=(10, 18))

        self.bt_detener = tk.Button(self.container_frame, text="Detener", width=10, height=2, command=lambda: self.detener_programa())
        self.bt_detener.grid(row=self.filas[4], column=1,  pady=(10, 18))

        self.bt_reiniciar = tk.Button(self.container_frame, text="Reiniciar", width=10, height=2, command=lambda: self.reiniciar_programa())
        self.bt_reiniciar.grid(row=self.filas[4], column=2, padx=(1,10),  pady=(10, 18))
        self.bt_reiniciar.config(state=tk.DISABLED)
        
        
        self.bt_modo_auto = tk.Button(self.container_frame, text="Modo auto", width=10, height=2, command=lambda: self.control_modo_auto())
        self.bt_modo_auto.grid(row=self.filas[4], column=3, padx=(1,10),  pady=(10, 18))
        
        #Frame estados y coordenadas
        self.estado = tk.Text(self.container_frame2, height=3, width=51, state=tk.DISABLED)
        self.estado.grid(row=self.filas[5], column=0, padx=5, pady=10)

        self.coordenadas_texto = tk.Text(self.container_frame2, height=2, width=51, state=tk.DISABLED)
        self.coordenadas_texto.grid(row=self.filas[6], column=0,  pady=10)
        
    
    # Funcion para configurar parametros de botones segun el contenedor seleccionado.
    def guardar_contenedor(self, contenedor):
        #Control de los colores de botones contenedor
        if (contenedor == "contenedor 1"):
            self.contenedor1.config(bg='#BCAAA4')
            self.contenedor2.config(bg='SystemButtonFace')
            self.contenedor3.config(bg='SystemButtonFace')
            self.contenedor4.config(bg='SystemButtonFace')
        
        elif(contenedor == "contenedor 2"):
            self.contenedor1.config(bg='SystemButtonFace')
            self.contenedor2.config(bg='#BCAAA4')
            self.contenedor3.config(bg='SystemButtonFace')
            self.contenedor4.config(bg='SystemButtonFace')
            
        elif(contenedor == "contenedor 3"):
            self.contenedor1.config(bg='SystemButtonFace')
            self.contenedor2.config(bg='SystemButtonFace')
            self.contenedor3.config(bg='#BCAAA4')
            self.contenedor4.config(bg='SystemButtonFace')
            
        elif(contenedor == "contenedor 4"):
            self.contenedor1.config(bg='SystemButtonFace')
            self.contenedor2.config(bg='SystemButtonFace')
            self.contenedor3.config(bg='SystemButtonFace')
            self.contenedor4.config(bg='#BCAAA4')
            
        self.contenedor = contenedor

    # Funcion para configurar parametros de botones y textos segun el color seleccionado.
    def guardar_color(self, color):
        #Control de colores de botones tapa
        if (color == "roja"):
            self.tapa_roja.config(bg='#F44336')
            self.tapa_verde.config(bg='SystemButtonFace')
            self.tapa_azul.config(bg='SystemButtonFace')
            self.tapa_amarilla.config(bg='SystemButtonFace')
        
        elif(color == "verde"):
            self.tapa_roja.config(bg='SystemButtonFace')
            self.tapa_verde.config(bg='#89AC76')
            self.tapa_azul.config(bg='SystemButtonFace')
            self.tapa_amarilla.config(bg='SystemButtonFace')
            
        elif(color == "azul"):
            self.tapa_roja.config(bg='SystemButtonFace')
            self.tapa_verde.config(bg='SystemButtonFace')
            self.tapa_azul.config(bg='#2271b3')
            self.tapa_amarilla.config(bg='SystemButtonFace')
            
        elif(color == "amarilla"):
            self.tapa_roja.config(bg='SystemButtonFace')
            self.tapa_verde.config(bg='SystemButtonFace')
            self.tapa_azul.config(bg='SystemButtonFace')
            self.tapa_amarilla.config(bg='#EEFF41')
            
        
        # Texto sobre seleccion de tapa y contenedor a imprimir en la interfaz
        self.color_seleccionado = color
        self.aux_estado[0] = 1
        self.coordenadas = self.leer_coordenadas()
        self.estado_ejecutar = f"Dobot seleccionará una tapa {self.color_seleccionado} y la colocará \nen el {self.contenedor}."
        self.x_pos_azul, self.y_pos_azul, self.x_pos_rojo, self.y_pos_rojo, self.x_pos_amarillo, self.y_pos_amarillo, self.x_pos_verde, self.y_pos_verde = self.leer_coordenadas()

        
        self.coordenadas_texto.config(state=tk.NORMAL)
        self.coordenadas_texto.delete(1.0, tk.END)
        
        # Texto sobre coordenadas segun el color seleccionado
        if self.color_seleccionado == 'roja':
            self.coordenadas_texto.insert(tk.END, f"Coordenadas X, Y \n{self.x_pos_rojo}, {self.y_pos_rojo}")
        elif self.color_seleccionado == 'verde':
            self.coordenadas_texto.insert(tk.END, f"Coordenadas X, Y \n{self.x_pos_verde}, {self.y_pos_verde}")
        elif self.color_seleccionado == 'azul':
            self.coordenadas_texto.insert(tk.END, f"Coordenadas X, Y \n{self.x_pos_azul}, {self.y_pos_azul}")
        else:
            self.coordenadas_texto.insert(tk.END, f"Coordenadas X, Y \n{self.x_pos_amarillo}, {self.y_pos_amarillo}")

        self.coordenadas_texto.config(state=tk.DISABLED)
        self.estado_dobot()

    # Funcion de detencion del programa. Deshabilita botones y regresa a la posicion de origen.
    def detener_programa(self):
        self.en_ejecucion = False
        self.coordenadas_texto.config(state=tk.NORMAL)
        self.coordenadas_texto.delete(1.0, tk.END)
        self.aux_estado[1] = 1
        self.estado_detener = 'El programa ha sido detenido.'
        self.estado_dobot()
        
        # Secuencia para la detencion del programa y su vuelta al origen
        cd.ser.close()
        cd.ser.open()
        cd.pos_origen()
        cd.ser.close()
        cd.ser.open()

        # Desactivado de botoneria
        self.tapa_roja.config(state=tk.DISABLED)
        self.tapa_verde.config(state=tk.DISABLED)
        self.tapa_azul.config(state=tk.DISABLED)
        self.tapa_amarilla.config(state=tk.DISABLED)
        self.contenedor1.config(state=tk.DISABLED)
        self.contenedor2.config(state=tk.DISABLED)
        self.contenedor3.config(state=tk.DISABLED)
        self.contenedor4.config(state=tk.DISABLED)
        self.bt_modo_auto.config(state=tk.DISABLED)
        self.bt_ejecutar.config(state=tk.DISABLED)
        self.bt_reiniciar.config(state=tk.NORMAL)
        self.bt_detener.config(state=tk.DISABLED)

    # Funcion de reinicio del programa luego de la detencion.
    def reiniciar_programa(self):
        
        # Reinicio de colores originales de botones
        self.contenedor1.config(bg='SystemButtonFace')
        self.contenedor2.config(bg='SystemButtonFace')
        self.contenedor3.config(bg='SystemButtonFace')
        self.contenedor4.config(bg='SystemButtonFace')
        self.tapa_roja.config(bg='SystemButtonFace')
        self.tapa_verde.config(bg='SystemButtonFace')
        self.tapa_azul.config(bg='SystemButtonFace')
        self.tapa_amarilla.config(bg='SystemButtonFace')
        
        self.aux_estado[2] = 1
        self.en_ejecucion = True
        self.coordenadas_texto.config(state=tk.NORMAL)
        self.coordenadas_texto.delete(1.0, tk.END)
        self.estado_reiniciar = 'El programa ha sido reiniciado'
        self.estado_dobot()
        self.aux_estado = [0,0,0,0]

        # Habilitacion de la botoneria luego de haber sido detenido el programa
        self.tapa_roja.config(state=tk.NORMAL)
        self.tapa_verde.config(state=tk.NORMAL)
        self.tapa_azul.config(state=tk.NORMAL)
        self.tapa_amarilla.config(state=tk.NORMAL)
        self.contenedor1.config(state=tk.NORMAL)
        self.contenedor2.config(state=tk.NORMAL)
        self.contenedor3.config(state=tk.NORMAL)
        self.contenedor4.config(state=tk.NORMAL)
        self.bt_modo_auto.config(state=tk.NORMAL)
        self.bt_ejecutar.config(state=tk.NORMAL)
        self.bt_detener.config(state=tk.NORMAL)
        self.bt_reiniciar.config(state=tk.DISABLED)
        
    def control_modo_auto(self):
        # Colores de botones en modo automatico
        self.contenedor1.config(bg='#BCAAA4')
        self.contenedor2.config(bg='#BCAAA4')
        self.contenedor3.config(bg='#BCAAA4')
        self.contenedor4.config(bg='#BCAAA4')
        
        self.coordenadas_texto.config(state=tk.NORMAL)
        self.coordenadas_texto.delete(1.0, tk.END)
        
        self.estado_modo_auto = 'Se ha activado el modo automatico'
        self.aux_estado[3] = 1
        self.estado_dobot()
        
        # Desactivado de botoneria en modo automatico
        self.tapa_roja.config(state=tk.DISABLED)
        self.tapa_verde.config(state=tk.DISABLED)
        self.tapa_azul.config(state=tk.DISABLED)
        self.tapa_amarilla.config(state=tk.DISABLED)
        self.contenedor1.config(state=tk.DISABLED)
        self.contenedor2.config(state=tk.DISABLED)
        self.contenedor3.config(state=tk.DISABLED)
        self.contenedor4.config(state=tk.DISABLED)
        self.bt_modo_auto.config(state=tk.DISABLED)
        self.bt_ejecutar.config(state=tk.DISABLED)
        self.bt_reiniciar.config(state=tk.DISABLED)
        
        # Acciones de control en modo automatico
        cd.modo_automatico()
        
        # Habilitacion de botoneria luego de finalizar el modo automatico
        self.tapa_roja.config(state=tk.NORMAL)
        self.tapa_verde.config(state=tk.NORMAL)
        self.tapa_azul.config(state=tk.NORMAL)
        self.tapa_amarilla.config(state=tk.NORMAL)
        self.contenedor1.config(state=tk.NORMAL)
        self.contenedor2.config(state=tk.NORMAL)
        self.contenedor3.config(state=tk.NORMAL)
        self.contenedor4.config(state=tk.NORMAL)
        self.bt_modo_auto.config(state=tk.NORMAL)
        self.bt_ejecutar.config(state=tk.NORMAL)
        self.bt_detener.config(state=tk.NORMAL)

    # Funcion para leer las coordenadas obtenidas en el archivo de texto de FrameCamara.py
    def leer_coordenadas(self):
        with open("coordenadas.txt", "r") as f:
            # Obtiene las coordenadas, lo convierte en una lista y lo retorna
            archivo = f.read()

            if (archivo):
                archivo_lista = archivo.split(",")
                return int(archivo_lista[0]), int(archivo_lista[1]), int(archivo_lista[2]), int(archivo_lista[3]), int(
                    archivo_lista[4]), int(archivo_lista[5]), int(archivo_lista[6]), int(archivo_lista[7])
            else:
                return 0, 0, 0, 0, 0, 0, 0, 0
            
    # Funcion llamada en seleccion_cuadrante(). 
    # Usada para definir la accion de control segun contenedor seleccionado.
    def seleccion_caja(self, caja="contenedor 1"):
        if (caja == "contenedor 1"):
            cd.control_caja1()

        elif (caja == "contenedor 2"):
            cd.control_caja2()

        elif (caja == "contenedor 3"):
            cd.control_caja3()

        else:
            cd.control_caja4()

    # Funcion para guardar las coordenadas segun el color seleccionado.
    # Controla los 4 cuadrantes del frame y permite saber en cual de estos 
    # se encuentra el color seleccionado para aplicar la accion de control.
    def seleccion_cuadrante(self, color, caja):
        
        if (color == "azul"):
            self.x = self.x_pos_azul
            self.y = self.y_pos_azul

        elif (color == "amarilla"):
            self.x = self.x_pos_amarillo
            self.y = self.y_pos_amarillo

        elif (color == "verde"):
            self.x = self.x_pos_verde
            self.y = self.y_pos_verde

        else:
            self.x = self.x_pos_rojo
            self.y = self.y_pos_rojo
            
        cd.config_dobot()
        
        if (self.x >= 250+self.offset_x and self.y <= 150+self.offset_y):  # Cuadrante 1
            
            cd.ser.close()
            cd.ser.open()
            cd.control_tapa1()
            self.seleccion_caja(caja)
            cd.ser.close()

        elif (self.x < 250+self.offset_x and self.y <= 150+self.offset_y):  # Cuadrante 2
            cd.ser.close()
            cd.ser.open()
            cd.control_tapa2()
            self.seleccion_caja(caja)
            cd.ser.close()

        elif (self.x < 250+self.offset_x and self.y >= 150+self.offset_y):  # Cuadrante 3
            cd.ser.close()
            cd.ser.open()
            cd.control_tapa3()
            self.seleccion_caja(caja)
            cd.ser.close()

        elif (self.x >= 250+self.offset_x and self.y >= 150+self.offset_y):  # Cuadrante 4
            cd.ser.close()
            cd.ser.open()
            cd.control_tapa4()
            self.seleccion_caja(caja)
            cd.ser.close()
                  
        cd.ser.open()

    
    # Funcion para definir el estado del dobot e imprimir el mensaje de la interfaz
    # segun si se encuentra en ejecucion, detencion, reinicio o modo automatico.
    def estado_dobot(self):
        self.estado.config(state=tk.NORMAL)
        self.estado.delete(1.0, tk.END)
        
        print(f'aux estado {self.aux_estado}')
        if (self.aux_estado[0] == 1):
            self.estado.insert(tk.END, f"Estado DOBOT: \n{self.estado_ejecutar}")
        elif (self.aux_estado[1] == 1):
            self.estado.insert(tk.END, f"Estado DOBOT: \n{self.estado_detener}")
        elif (self.aux_estado[2] == 1):
            self.estado.insert(tk.END, f"Estado DOBOT: \n{self.estado_reiniciar}")
        elif (self.aux_estado[3] == 1):
            self.estado.insert(tk.END, f"Estado DOBOT: \n{self.estado_modo_auto}")
            
        self.estado.config(state=tk.DISABLED)
        
        if (self.aux_estado[1] == 1):
            self.aux_estado = [0,0,1,0]
        else:
            self.aux_estado = [0,0,0,0]

    # Funcion de ejecucion del programa en modo manual. Se selecciona color y contenedor.
    def parametros_dobot(self):
        
        if self.ejecucion:  
            if self.color_seleccionado and self.contenedor:
                self.x_pos_azul, self.y_pos_azul, self.x_pos_rojo, self.y_pos_rojo, self.x_pos_amarillo, self.y_pos_amarillo, self.x_pos_verde, self.y_pos_verde = self.leer_coordenadas()
              
                time.sleep(0.5)
                self.seleccion_cuadrante(self.color_seleccionado, self.contenedor)

            else:
                self.aux_estado[0] = 1
                self.estado_ejecutar = 'Por favor, selecciona un color y un contenedor.'
                self.estado_dobot()
        else:
            self.estado_ejecutar = 'El programa se ha detenido'

if __name__ == "__main__":
    root = tk.Tk()
    root.wm_title('Interfaz de control DOBOT')
    app = DobotApp(root)
    app.mainloop()