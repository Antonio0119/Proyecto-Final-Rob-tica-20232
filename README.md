# Proyecto-Final-Robotica-20232
Proyecto Final del Curso Robótica Industrial Semestre 20232
<br>Ingeniería Electrónica - Facultad de Ingeniería - Universidad de Antioquia
<br>Creado por Antonio José Aristizábal y David Felipe Vélez

<h2>Instrucciones para el uso del Dobot Clasificador de Elementos por Color</h2>

<h4>Hardware necesario:</h4>
	*PC o Laptop básicas
	<br>*Dobot V1
	<br>*Cable de conexión USB
	<br>*Cámara Web
	<br>*Tapas de colores

<h4>Software necesario:</h4>
	*Python
	<br>*Arduino

<h4>Librerías Python necesarias:</h4>
	*cv2 (opencv)
	<br>*tkinter
	<br>*numpy
	<br>*pyserial
	<br>*time
	<br>*os
 	<br>*struc
  	<br>*binascii
	
<h4>Procedimiento para utilizar los programas:</h4>
	1) Disponer las tapas o piezas en la zona designada.
	<br>2) Ejecutar el programa FrameCamara.py en una consola de python(Necesario tener la camara conectada)
	<br>3) Organizar las tapas dentro del frame de la camara (en cada cuadrante)
	<br>4) Ejecutar el programa InterfazDobot.py en una consola de python diferente.
	<br>5) Utilizar los botones de la interfaz desplegada para accionar el Dobot.
	<br>6) La interfaz presenta dos modos:
		*Modo Manual: seleccionar un contenedor y una tapa de color, luego presionar ejecutar para que se realice la acción del dobot.
		*Modo Automático: seleccionar el botón Modo auto, el robot hará un recorrido y recogera las cuatro tapas para almacenarlas en los cuatro contenedores.
	
<br><b>Nota</b>: Es posible que el dobot se bloquee al estar mucho tiempo sin realizar acciones, ya que el serial tiene un tiempo de timeout en el cual se desconecta. En caso de que esto suceda, reiniciar el kernel y volver a ejecutar InterfazDobot.py
