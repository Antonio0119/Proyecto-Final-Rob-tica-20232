# Proyecto-Final-Robotica-20232
Proyecto Final del Curso Robótica Industrial de la Universidad de Antioquia semestre 20232
Creado por Antonio José Aristizábal y David Felipe Vélez

Instrucciones para el uso del Dobot clasificador de elementos por color

Hardware necesario:
	*PC o Laptop básicas
	*Dobot V1
	*Cable de conexión USB
	*Cámara Web
	*Tapas de colores

Software necesario:
	*Python
	*Arduino

Librerías Python necesarias:
	*cv2 (opencv)
	*tkinter
	*numpy
	*serial
	*time
	*os
	
Procedimiento para utilizar los programas:
	1) Disponer las tapas o piezas en la zona designada.
	2) Ejecutar el programa FrameCamara.py en una consola de python(Necesario tener la camara conectada)
	2) Organizar las tapas dentro del frame de la camara (en cada cuadrante)
	3) Ejecutar el programa InterfazDobot.py en una consola de python diferente.
	4) Utilizar los botones de la interfaz desplegada para accionar el Dobot.
	5) La interfaz presenta dos modos:
		*Modo Manual: seleccionar un contenedor y una tapa de color, luego presionar ejecutar para que se realice la acción del dobot.
		*Modo Automático: seleccionar el botón Modo auto, el robot hará un recorrido y recogera las cuatro tapas para almacenarlas en los cuatro contenedores.
	
Nota: Es posible que el dobot se bloquee al estar mucho tiempo sin realizar acciones, ya que el serial tiene un tiempo de timeout en el cual se desconecta. En caso de que esto suceda, reiniciar el kernel y volver a ejecutar InterfazDobot.py
