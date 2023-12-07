import serial
import struct
import time
import os
import binascii

# Apertura del puerto serial
cmd_str_10 = [0 for i in range(10)]
cmd_str_42 = ['\x00' for i in range(42)]
ser = serial.Serial(  # serial connection
    port='COM4',
    baudrate=9600,
    parity=serial.PARITY_NONE,  # serial.PARITY_ODD,
    stopbits=serial.STOPBITS_ONE,  # serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS  # serial.SEVENBITS
)



# Configuracion del Dobot
def dobot_cmd_send(cmd_str_10):
    global cmd_str_42
    cmd_str_42 = ['\x00' for i in range(42)]
    cmd_str_42[0] = '\xA5'
    cmd_str_42[41] = '\x5A'
    for i in range(10):
        str4 = struct.pack('<f', float(cmd_str_10[i]))
        cmd_str_42[4 * i + 1] = hex(str4[0])[2:].rjust(2, '0')
        cmd_str_42[4 * i + 2] = hex(str4[1])[2:].rjust(2, '0')
        cmd_str_42[4 * i + 3] = hex(str4[2])[2:].rjust(2, '0')
        cmd_str_42[4 * i + 4] = hex(str4[3])[2:].rjust(2, '0')
    cmd_str = str(cmd_str_42).replace("'", "").replace(",", "")[2:-2]
    cmd_str1 = bytes.fromhex(cmd_str)
    time.sleep(0.5)
    print(cmd_str1)
    msg = b'\xA5'
    msg1 = b'\x5A'
    time.sleep(0.5)
    ser.write(msg + cmd_str1 + msg1)


# Estado 3 para enviar coordenadas al dobot y especificar succion y tipo de movimiento
def dobot_cmd_send_3(x=265, y=0, z=-30, mov=1, suc=0):
    global cmd_str_10
    cmd_str_10 = [0 for i in range(10)]
    cmd_str_10[0] = 3
    cmd_str_10[2] = x
    cmd_str_10[3] = y
    cmd_str_10[4] = z
    cmd_str_10[6] = suc  # succion
    cmd_str_10[7] = mov  # JUMP 0, MOVL 1, MOVJ 2
    dobot_cmd_send(cmd_str_10)


# Configuracion de velocidades y aceleraciones
def dobot_cmd_send_9():
    global cmd_str_10
    cmd_str_10 = [0 for i in range(10)]
    cmd_str_10[0] = 9
    cmd_str_10[1] = 1
    cmd_str_10[2] = 200  # JointVel
    cmd_str_10[3] = 200  # JointAcc
    cmd_str_10[4] = 200  # ServoVel
    cmd_str_10[5] = 200  # ServoAcc
    cmd_str_10[6] = 800  # LinearVel
    cmd_str_10[7] = 1000  # LinearAcc
    dobot_cmd_send(cmd_str_10)


def dobot_cmd_send_10(VelRat=100, AccRat=100):
    global cmd_str_10
    cmd_str_10 = [0 for i in range(10)]
    cmd_str_10[0] = 10
    cmd_str_10[2] = VelRat
    cmd_str_10[3] = AccRat
    dobot_cmd_send(cmd_str_10)


# Funcion para conexion con puerto serial
def comunicacion_serial(port="COM4"):
    time.sleep(0.1)
    ser = serial.Serial(  # serial connection
        port=port,
        baudrate=9600,
        parity=serial.PARITY_NONE,  # serial.PARITY_ODD,
        stopbits=serial.STOPBITS_ONE,  # serial.STOPBITS_TWO,
        bytesize=serial.EIGHTBITS  # serial.SEVENBITS
    )
    ser.isOpen()

# Funcion para llamado de funciones de configuracion del dobot
def config_dobot():
    ser.write(bytes.fromhex('a5000010410000804000000000000000000000000000000000000000000000000000000000000000005a'))
    time.sleep(0.5)
    dobot_cmd_send_9()  # config
    time.sleep(0.1)
    dobot_cmd_send_10()  # config
    time.sleep(0.1)
    
# Posicion de Origen
def pos_origen():
    dobot_cmd_send_3(211, 0, -25, 1, 0)
    time.sleep(0.5)
    dobot_cmd_send_3(158.909, 0, -25)
    time.sleep(0.5)
    

# Posicion tapa 1********
def control_tapa1():
    # dobot_cmd_send_3(158.909, 0, -25)
    # time.sleep(0.5)
    dobot_cmd_send_3(209, 0, -99.989, 1, 1)
    time.sleep(0.5)
    dobot_cmd_send_3(209, 0, -52.8, 1, 1)
    time.sleep(0.5)
    dobot_cmd_send_3(209, 0, -52.8, 1, 1)
    time.sleep(0.5)

# #Empacado caja 1
def control_caja1():
    dobot_cmd_send_3(30, 200, 40, 1, 1)
    time.sleep(0.5)
    dobot_cmd_send_3(30, 200, -20, 1, 1)
    time.sleep(0.5)
    dobot_cmd_send_3(30, 200, -20, 1, 0)
    time.sleep(0.5)
    dobot_cmd_send_3(211, 0, -25, 1, 0)
    time.sleep(0.5)
    dobot_cmd_send_3(158.909, 0, -25)
    time.sleep(0.5)
    # ser.close()

# Posicion tapa 2 ******
def control_tapa2():
    dobot_cmd_send_3(158.909, 0, -25)
    time.sleep(0.5)
    dobot_cmd_send_3(163.8, 0, -94.9, 1, 1)
    time.sleep(0.5)
    dobot_cmd_send_3(163.8, 0, -52.8, 1, 1)
    time.sleep(0.5)
    dobot_cmd_send_3(163.8, 0, -52.8, 1, 1)
    time.sleep(0.5)

# Empacado caja 2
def control_caja2():
    dobot_cmd_send_3(0, 270, 40, 1, 1)
    time.sleep(0.5)
    dobot_cmd_send_3(0, 270, -20, 1, 1)
    time.sleep(0.5)
    dobot_cmd_send_3(0, 270, -20, 1, 0)
    time.sleep(0.5)
    dobot_cmd_send_3(211, 0, -25, 1, 0)
    time.sleep(0.5)
    dobot_cmd_send_3(158.909, 0, -25)
    time.sleep(0.5)
    # ser.close()

# Posicion tapa 3********
def control_tapa3():
    dobot_cmd_send_3(164, -76, -99.7, 1, 1)
    time.sleep(0.5)
    dobot_cmd_send_3(164, -76, -52.8, 1, 1)
    time.sleep(0.5)
    dobot_cmd_send_3(164, -76, -52.8, 1, 1)
    time.sleep(0.5)

# Empacado caja 3
def control_caja3():
    dobot_cmd_send_3(50, 270, 40, 1, 1)
    time.sleep(0.5)
    dobot_cmd_send_3(50, 270, -20, 1, 1)
    time.sleep(0.5)
    dobot_cmd_send_3(50, 270, -20, 1, 0)
    time.sleep(0.5)
    dobot_cmd_send_3(211, 0, -25, 1, 0)
    time.sleep(0.5)
    dobot_cmd_send_3(158.909, 0, -25)
    time.sleep(0.5)
    # ser.close()

# Posicion tapa 4********
def control_tapa4():
    dobot_cmd_send_3(211, -76, -99, 1, 1)
    time.sleep(0.5)
    dobot_cmd_send_3(211, -76, -52.8, 1, 1)
    time.sleep(0.5)
    dobot_cmd_send_3(211, -76, -52.8, 1, 1)
    time.sleep(0.5)

# Empacado caja 4
def control_caja4():
    dobot_cmd_send_3(100, 200, 40, 1, 1)
    time.sleep(0.5)
    dobot_cmd_send_3(100, 200, -20, 1, 1)
    time.sleep(0.5)
    dobot_cmd_send_3(100, 200, -20, 1, 0)
    time.sleep(0.5)
    dobot_cmd_send_3(211, 0, -25, 1, 0)
    time.sleep(0.5)
    dobot_cmd_send_3(158.909, 0, -25)
    time.sleep(0.5)
    # ser.close()


# Modo automatico
def modo_automatico():  
    time.sleep(2)
    config_dobot()
    print("hola")
    
    ser.close()
    ser.open()
    # comunicacion_serial()
    print("serial")
    control_tapa1()
    control_caja1()
    ser.close()
    
    comunicacion_serial()
    ser.open()
    config_dobot()
    control_tapa2()
    control_caja2()
    ser.close()
    
    comunicacion_serial()
    ser.open()
    config_dobot()
    control_tapa3()
    control_caja3()
    ser.close()
    
    comunicacion_serial()
    ser.open()
    config_dobot()
    control_tapa4()
    control_caja4()
    ser.close()
    ser.open()