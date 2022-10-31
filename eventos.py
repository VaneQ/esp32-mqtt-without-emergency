from machine import Pin, UART, reset
import time as time
import network
import socket
import usocket
#import paho.mqtt.client as mqtt
from umqttsimple import MQTTClient
import json
#import uping 

#norte
#cable_1 = 2 #verde
cable_1 = 2 #verde
#cable_2 = 23 #amarillo
#cable_2 = 23 #amarillo
cable_2 = 25 #amarillo
#cable_3 = 5 #rojo
#cable_3 = 5 #rojo
cable_3 = 26 #rojo

#oeste
#cable_4 = 13 #verde
cable_4 = 13 #verde
#cable_5 = 14 #amarillo
cable_5 = 14 #amarillo
#cable_6 = 15 #rojo
cable_6 = 15 #rojo

#sur
#cable_7 = 16 #verde
cable_7 = 16 #verde
#cable_8 = 17 #amarillo
cable_8 = 17 #amarillo
#cable_9 = 18 #rojo
#cable_9 = 18 #rojo
cable_9 = 27 #rojo

#este
#cable_10 = 19 #verde
#cable_10 = 19 #verde
cable_10 = 12 #verde
#cable_11 = 21 #amarillo
cable_11 = 21 #amarillo
#cable_12 = 22 #rojo
cable_12 = 22 #rojo

intervalo_1 = 8;
intervalo_2 = 3;
intervalo_3 = 8;
intervalo_4 = 3;
intervalo_5 = 8;
intervalo_6 = 3;
intervalo_7 = 8;
intervalo_8 = 3;

ON = 1
OFF = 0

estado_cableado_a = ON;
estado_cableado_b = OFF;
estado_cableado_c = OFF;
estado_cableado_d = OFF;
estado_cableado_e = OFF;
estado_cableado_f = OFF;
estado_cableado_g = OFF;
estado_cableado_h = OFF;
estado_cableado_s = OFF;

estado_cableado_rojos = OFF;
estado_cableado_amarillos = OFF;
estado_cableado_verdes = OFF;
estado_cableado_oeste = OFF;
estado_cableado_este = OFF;
estado_cableado_norte = OFF;
estado_cableado_sur = OFF;

semaforo_a = 1;  # 0 - Apagado, 1 - Encendido
global modo_a;      # 1 - Normal, 2 - Solo Verde, 3 - Solo Rojo
modo_a = 1
modo_cont = 1;   # 0 - Apagado, 1 - Ambos, 2 - Solo Contador, 3 - Solo Mensaje

segundos = 0;
cuenta = intervalo_2;
intervaloSig = 0;

tiempo = 0;
tiempo_a = 0;
tiempo_b = 0;
contador = 0;

i = 0;

mensaje = "#GranMisionTransporteVenezuela";
enviar = 1;
xy = 0;

ultimo_cambio_seg = 0;
ultimo_cambio_seg1 = 0;

#ssid = 'VICT3'
#password = '*masc4f3*'

ssid = 'Soporte Informatico'
password = 'produccion*2019*'

#ssid = 'MikroTik-TIC'
#password = '12345678'

#ssid = 'MikroTik-CALIDAD'
#password = 'c4l1d4d*22'

#ssid = 'Domino'
#password = 'Pandorito1!'
wlan = network.WLAN(network.STA_IF)

wlan.active(True)

def conectar_red():
    try:
       wlan.connect(ssid, password)
       print("conectado a red")
       return True
   
    except OSError as err:
        time.sleep(2)
        print("reconectando a red")
        conectar_red()
        return False
    return True


conectar_red()

#wlan.connect(ssid, password)

while wlan.isconnected() == False:
    pass


print('Conexion con el WiFi %s establecida' % ssid)
print(wlan.ifconfig())

device_network_data = wlan.ifconfig()

global client_id, mqtt_server, topic_sub, topic_pub

client_id = device_network_data[0]
#topic_sub = b'Semaforo/notificacion'
topic_sub = b'Semaforo/45/Emergencia'
topic_pub = b'Semaforo/45/Status'

last_message = 0
message_interval = 10
counter = 1
temporizador = False

#mqtt_server = "192.168.200.241"
mqtt_server = "192.168.200.132"
#mqtt_server = "test.mosquitto.org"

def setup():
    Pin(cable_1,Pin.OUT)
    Pin(cable_2,Pin.OUT)
    Pin(cable_3,Pin.OUT)
    Pin(cable_4,Pin.OUT)
    Pin(cable_5,Pin.OUT)
    Pin(cable_6,Pin.OUT)
    Pin(cable_7,Pin.OUT)
    Pin(cable_8,Pin.OUT)
    Pin(cable_9,Pin.OUT)
    Pin(cable_10,Pin.OUT)
    Pin(cable_11,Pin.OUT)
    Pin(cable_12,Pin.OUT)

setup()

def pause_mode():
    
    if Pin(cable_1).value() == 1:
        
        Pin(cable_1).value(OFF);
        Pin(cable_2).value(ON);
        Pin(cable_3).value(OFF);
    
    else:
        Pin(cable_1).value(OFF)
        Pin(cable_2).value(OFF)
        Pin(cable_3).value(ON);
    
    if Pin(cable_4).value() == 1:
        
        Pin(cable_4).value(OFF);
        Pin(cable_5).value(ON);
        Pin(cable_6).value(OFF);
    
    else:
        Pin(cable_4).value(OFF);
        Pin(cable_5).value(OFF);
        Pin(cable_6).value(ON);
        
    if Pin(cable_7).value() == 1:
        
        Pin(cable_7).value(OFF);
        Pin(cable_8).value(ON);
        Pin(cable_9).value(OFF);
    
    else:
        Pin(cable_7).value(OFF);
        Pin(cable_8).value(OFF);
        Pin(cable_9).value(ON);
    
    if Pin(cable_10).value() == 1:
        
        Pin(cable_10).value(OFF);
        Pin(cable_11).value(ON);
        Pin(cable_12).value(OFF);
    
    else:
        Pin(cable_10).value(OFF);
        Pin(cable_11).value(OFF);
        Pin(cable_12).value(ON);
    
    #Pin(cable_1).value(OFF)
    #Pin(cable_2).value(ON)
    #Pin(cable_3).value(OFF)
                
    #Pin(cable_4).value(OFF)
    #Pin(cable_5).value(ON)
    #Pin(cable_6).value(OFF)
                
    #Pin(cable_7).value(OFF)
    #Pin(cable_8).value(ON)
    #Pin(cable_9).value(OFF)
                
    #Pin(cable_10).value(OFF)
    #Pin(cable_11).value(ON)
    #Pin(cable_12).value(OFF)
    
    time.sleep(3)

def reset_mode(modo = 1, cifra = 0):
    
    print("reseteando")
    
    pause_mode()
    
    global estado_cableado_a, estado_cableado_b, estado_cableado_c, estado_cableado_d, estado_cableado_e
    global estado_cableado_f, estado_cableado_g, estado_cableado_h, estado_cableado_s
    global contador, modo_a, cuenta, intervaloSig, segundos, tiempo, ultimo_cambio_seg
    global estado_cableado_rojos, estado_cableado_amarillos, estado_cableado_verdes, estado_cableado_oeste, estado_cableado_este, estado_cableado_norte, estado_cableado_sur
    global temporizador
    
    estado_cableado_a = OFF
    estado_cableado_b = OFF
    estado_cableado_c = OFF
    estado_cableado_d = OFF
    estado_cableado_e = OFF
    estado_cableado_f = OFF
    estado_cableado_g = OFF
    estado_cableado_h = OFF
    estado_cableado_s = OFF
    
    
    estado_cableado_rojos = OFF;
    estado_cableado_amarillos = OFF;
    estado_cableado_verdes = OFF;
    estado_cableado_oeste = OFF;
    estado_cableado_este = OFF;
    estado_cableado_norte = OFF;
    estado_cableado_sur = OFF;
       
    
    if cifra > 0:
        contador = cifra
        temporizador = True
    else:
        temporizador = False
        contador = 0
        
    segundos = 0;
    cuenta = 0;
    modo_a = modo;
        
    if modo_a == 1:
        contador = 0  
        estado_cableado_a = ON
        cuenta = intervalo_2;
        intervaloSig = intervalo_2;
        tiempo = 1;
        
    else:
        if modo_a == 2:
            estado_cableado_este = ON
        
        elif modo_a == 3:
            estado_cableado_oeste = ON
        
        elif modo_a == 4:
            estado_cableado_norte = ON
        
        elif modo_a == 5:
            estado_cableado_sur = ON
        
        elif modo_a == 6:
            estado_cableado_rojos = ON
        
        else:
            estado_cableado_amarillos = ON
            
        cuenta = 0;
        intervaloSig = intervalo_2;
        tiempo = 0;
        
    ultimo_cambio_seg = 0;
    
def semaforos_a():
    
    hora = time.ticks_ms()
    hora_1 = time.ticks_ms()
    
    global ultimo_cambio_seg
    global cuenta
    global segundos
    global estado_cableado_a
    global estado_cableado_b
    global estado_cableado_c
    global estado_cableado_d
    global estado_cableado_e
    global estado_cableado_f
    global estado_cableado_g
    global estado_cableado_h
    global estado_cableado_s
    global contador
    global modo_a
    global semaforo_a
    global i
    global estado_cableado_rojos, estado_cableado_amarillos, estado_cableado_verdes, estado_cableado_oeste, estado_cableado_este, estado_cableado_norte, estado_cableado_sur
    global temporizador

    
    if( time.ticks_diff(hora, ultimo_cambio_seg) >= 1000 ):
        
        print("segundos ")
        print(segundos)
        print("contador ")
        print(contador)
        
        #print("milisegundos mayor a 1 segun")
        
        if( semaforo_a == 1 and modo_a == 1 ):
            cuenta = cuenta - 1
        elif( semaforo_a == 1 and modo_a != 1 ):
            cuenta = cuenta - 1
        else:
            cuenta = 0
            intervaloSig = 0
            tiempo = 0
        
        segundos = segundos + 1
        
        if(segundos > 255):
            segundos = 0
        
        ultimo_cambio_seg = hora
    
    #fin hora
        
    if ( semaforo_a == 1 ):
        
        #print("semaforo_a igual a 1")
        
        if( modo_a == 1 ):
            
            if( segundos >= intervalo_2 and estado_cableado_a == 1 and modo_a == 1  ):
                
                print("primer intervalo")
                
                cuenta = intervalo_1
                intervaloSig =intervalo_1
                tiempo = 1
                tiempo_a = 1
                tiempo_b = 3
                estado_cableado_a = OFF
                estado_cableado_b = ON
                estado_cableado_c = OFF
                estado_cableado_d = OFF
                estado_cableado_e = OFF
                estado_cableado_f = OFF
                estado_cableado_g = OFF
                estado_cableado_h = OFF
                estado_cableado_s = OFF
                segundos = 0
                ultimo_cambio_seg = hora
                
                Pin(cable_1).value(ON)
                Pin(cable_2).value(OFF)
                Pin(cable_3).value(OFF)
                
                Pin(cable_4).value(OFF)
                Pin(cable_5).value(OFF)
                Pin(cable_6).value(ON)
                
                Pin(cable_7).value(OFF)
                Pin(cable_8).value(OFF)
                Pin(cable_9).value(ON)
                
                Pin(cable_10).value(OFF)
                Pin(cable_11).value(OFF)
                Pin(cable_12).value(ON)
                
            
            #fin estado cableado a
                
            if( segundos >= intervalo_1 and estado_cableado_b == ON and modo_a == 1 ):
                
                print("amarillo 1")
                
                cuenta = intervalo_2
                intervaloSig = intervalo_2
                tiempo = 2
                tiempo_a = 2
                tiempo_b = 3
                estado_cableado_a = OFF
                estado_cableado_b = OFF
                estado_cableado_c = ON
                estado_cableado_d = OFF
                estado_cableado_e = OFF
                estado_cableado_f = OFF
                estado_cableado_g = OFF
                estado_cableado_h = OFF
                estado_cableado_s = OFF
                segundos = 0
                ultimo_cambio_seg = hora
                
                Pin(cable_1).value(OFF)
                Pin(cable_2).value(ON)
                Pin(cable_3).value(OFF)
                
                Pin(cable_4).value(OFF)
                Pin(cable_5).value(OFF)
                Pin(cable_6).value(ON)
                
                Pin(cable_7).value(OFF)
                Pin(cable_8).value(OFF)
                Pin(cable_9).value(ON)
                
                Pin(cable_10).value(OFF)
                Pin(cable_11).value(OFF)
                Pin(cable_12).value(ON)
                
             
            #fin estado cableado b
                
            if( segundos >= intervalo_2 and estado_cableado_c == ON and modo_a == 1 ):
                #intervalo2
                print("segundo intervalo")
                
                cuenta = intervalo_3
                intervaloSig = intervalo_3
                tiempo = 3
                tiempo_a = 3
                tiempo_b = 1
                estado_cableado_a = OFF
                estado_cableado_b = OFF
                estado_cableado_c = OFF
                estado_cableado_d = ON
                estado_cableado_e = OFF
                estado_cableado_f = OFF
                estado_cableado_g = OFF
                estado_cableado_h = OFF
                estado_cableado_s = OFF
                segundos = 0
                ultimo_cambio_seg = hora
                
                Pin(cable_1).value(OFF)
                Pin(cable_2).value(OFF)
                Pin(cable_3).value(ON)
                
                Pin(cable_4).value(ON)
                Pin(cable_5).value(OFF)
                Pin(cable_6).value(OFF)
                
                Pin(cable_7).value(OFF)
                Pin(cable_8).value(OFF)
                Pin(cable_9).value(ON)
                
                Pin(cable_10).value(OFF)
                Pin(cable_11).value(OFF)
                Pin(cable_12).value(ON)
            
            #fin cableado c
                
            if( segundos >= intervalo_3 and estado_cableado_d == ON and modo_a == 1 ):
                #AMARILLO 2
                print("amarillo 2")
                
                cuenta = intervalo_4
                intervaloSig = intervalo_4
                tiempo = 4
                tiempo_a = 3
                tiempo_b = 2
                estado_cableado_a = OFF
                estado_cableado_b = OFF
                estado_cableado_c = OFF
                estado_cableado_d = OFF
                estado_cableado_e = ON
                estado_cableado_f = OFF
                estado_cableado_g = OFF
                estado_cableado_h = OFF
                estado_cableado_s = OFF
                segundos = 0
                ultimo_cambio_seg = hora
                
                Pin(cable_1).value(OFF)
                Pin(cable_2).value(OFF)
                Pin(cable_3).value(ON)
                
                Pin(cable_4).value(OFF)
                Pin(cable_5).value(ON)
                Pin(cable_6).value(OFF)
                
                Pin(cable_7).value(OFF)
                Pin(cable_8).value(OFF)
                Pin(cable_9).value(ON)
                
                Pin(cable_10).value(OFF)
                Pin(cable_11).value(OFF)
                Pin(cable_12).value(ON)
                
            
            #fin cableado d
            if( segundos >= intervalo_4 and estado_cableado_e == ON and modo_a == 1 ):
                #intervalo 3
                #secuencia v
                print("tercer intervalo")
                
                cuenta = intervalo_5
                intervaloSig = intervalo_5
                tiempo = 5
                tiempo_a = 1
                tiempo_b = 3
                estado_cableado_a = OFF
                estado_cableado_b = OFF
                estado_cableado_c = OFF
                estado_cableado_d = OFF
                estado_cableado_e = OFF
                estado_cableado_f = ON
                estado_cableado_g = OFF
                estado_cableado_h = OFF
                estado_cableado_s = OFF
                segundos = 0
                ultimo_cambio_seg = hora
                
                Pin(cable_1).value(OFF)
                Pin(cable_2).value(OFF)
                Pin(cable_3).value(ON)
                
                Pin(cable_4).value(OFF)
                Pin(cable_5).value(OFF)
                Pin(cable_6).value(ON)
                
                Pin(cable_7).value(ON)
                Pin(cable_8).value(OFF)
                Pin(cable_9).value(OFF)
                
                Pin(cable_10).value(OFF)
                Pin(cable_11).value(OFF)
                Pin(cable_12).value(ON)
                
            #fin cableado_e
                
            if( segundos >= intervalo_5 and estado_cableado_f == ON and modo_a == 1 ):
                #amarillo 3
                #secuencia VI
                print("amarillo 3")
                
                cuenta = intervalo_5
                intervaloSig = intervalo_5
                tiempo = 6
                tiempo_a = 1
                tiempo_b = 3
                estado_cableado_a = OFF
                estado_cableado_b = OFF
                estado_cableado_c = OFF
                estado_cableado_d = OFF
                estado_cableado_e = OFF
                estado_cableado_f = OFF
                estado_cableado_g = ON
                estado_cableado_h = OFF
                estado_cableado_s = OFF
                segundos = 0
                ultimo_cambio_seg = hora
                
                Pin(cable_1).value(OFF)
                Pin(cable_2).value(OFF)
                Pin(cable_3).value(ON)
                
                Pin(cable_4).value(OFF)
                Pin(cable_5).value(OFF)
                Pin(cable_6).value(ON)
                
                Pin(cable_7).value(OFF)
                Pin(cable_8).value(ON)
                Pin(cable_9).value(OFF)
                
                Pin(cable_10).value(OFF)
                Pin(cable_11).value(OFF)
                Pin(cable_12).value(ON)
                
             #fin cableado_f
                
            if( segundos >= intervalo_6 and estado_cableado_g == ON and modo_a == 1 ):
                #amarillo 3
                #secuencia VI
                print("intervalo 4")
                
                cuenta = intervalo_6
                intervaloSig = intervalo_6
                tiempo = 7
                tiempo_a = 1
                tiempo_b = 3
                estado_cableado_a = OFF
                estado_cableado_b = OFF
                estado_cableado_c = OFF
                estado_cableado_d = OFF
                estado_cableado_e = OFF
                estado_cableado_f = OFF
                estado_cableado_g = OFF
                estado_cableado_h = ON
                estado_cableado_s = OFF
                segundos = 0
                ultimo_cambio_seg = hora
                
                Pin(cable_1).value(OFF)
                Pin(cable_2).value(OFF)
                Pin(cable_3).value(ON)
                
                Pin(cable_4).value(OFF)
                Pin(cable_5).value(OFF)
                Pin(cable_6).value(ON)
                
                Pin(cable_7).value(OFF)
                Pin(cable_8).value(OFF)
                Pin(cable_9).value(ON)
                
                Pin(cable_10).value(ON)
                Pin(cable_11).value(OFF)
                Pin(cable_12).value(OFF)
                
             #fin cableado_g
                
            if( segundos >= intervalo_7 and estado_cableado_h == ON and modo_a == 1 ):
                #amarillo 4
                #secuencia VI
                print("amarillo 4")
                
                cuenta = intervalo_7
                intervaloSig = intervalo_7
                tiempo = 1
                tiempo_a = 1
                tiempo_b = 3
                estado_cableado_a = ON
                estado_cableado_b = OFF
                estado_cableado_c = OFF
                estado_cableado_d = OFF
                estado_cableado_e = OFF
                estado_cableado_f = OFF
                estado_cableado_g = OFF
                estado_cableado_h = OFF
                estado_cableado_s = OFF
                segundos = 0
                ultimo_cambio_seg = hora
                
                Pin(cable_1).value(OFF)
                Pin(cable_2).value(OFF)
                Pin(cable_3).value(ON)
                
                Pin(cable_4).value(OFF)
                Pin(cable_5).value(OFF)
                Pin(cable_6).value(ON)
                
                Pin(cable_7).value(OFF)
                Pin(cable_8).value(OFF)
                Pin(cable_9).value(ON)
                
                Pin(cable_10).value(OFF)
                Pin(cable_11).value(ON)
                Pin(cable_12).value(OFF)
                
             #fin cableado_g
        #fin modo_a = 1
 
        if( modo_a == 2 and estado_cableado_este == ON ):
            
            print("mostrando patron este")
            
            estado_cableado_a = OFF
            estado_cableado_b = OFF
            estado_cableado_c = OFF
            estado_cableado_d = OFF
            estado_cableado_e = OFF
            estado_cableado_f = OFF
            estado_cableado_g = OFF
            estado_cableado_h = OFF
            estado_cableado_s = OFF
            
            estado_cableado_rojos = OFF;
            estado_cableado_amarillos = OFF;
            estado_cableado_verdes = OFF;
            estado_cableado_oeste = OFF;
            estado_cableado_este = OFF;
            estado_cableado_norte = OFF;
            estado_cableado_sur = OFF;
            
            #segundos = 0
            ultimo_cambio_seg = hora
                
            #Pin(cable_1).value(ON)
            #Pin(cable_2).value(OFF)
            #Pin(cable_3).value(OFF)
                
            #Pin(cable_4).value(OFF)
            #Pin(cable_5).value(OFF)
            #Pin(cable_6).value(ON)
                
            #Pin(cable_7).value(OFF)
            #Pin(cable_8).value(OFF)
            #Pin(cable_9).value(ON)
            
            #Pin(cable_10).value(OFF)
            #Pin(cable_11).value(OFF)
            #Pin(cable_12).value(ON)
            
            Pin(cable_1).value(OFF)
            Pin(cable_2).value(OFF)
            Pin(cable_3).value(ON)
                
            Pin(cable_4).value(OFF)
            Pin(cable_5).value(OFF)
            Pin(cable_6).value(ON)
                
            Pin(cable_7).value(OFF)
            Pin(cable_8).value(OFF)
            Pin(cable_9).value(ON)
            
            Pin(cable_10).value(ON)
            Pin(cable_11).value(OFF)
            Pin(cable_12).value(OFF)

        #fin modo a = 2
            
        if(modo_a == 3 and estado_cableado_oeste == ON ):
            
            print("mostrando patron oeste")
            
            estado_cableado_a = OFF
            estado_cableado_b = OFF
            estado_cableado_c = OFF
            estado_cableado_d = OFF
            estado_cableado_e = OFF
            estado_cableado_f = OFF
            estado_cableado_g = OFF
            estado_cableado_h = OFF
            estado_cableado_s = OFF
            
            estado_cableado_rojos = OFF;
            estado_cableado_amarillos = OFF;
            estado_cableado_verdes = OFF;
            estado_cableado_oeste = OFF;
            estado_cableado_este = OFF;
            estado_cableado_norte = OFF;
            estado_cableado_sur = OFF;

            ultimo_cambio_seg = hora
                
            #Pin(cable_1).value(OFF)
            #Pin(cable_2).value(OFF)
            #Pin(cable_3).value(ON)
                
            #Pin(cable_4).value(ON)
            #Pin(cable_5).value(OFF)
            #Pin(cable_6).value(OFF)
                
            #Pin(cable_7).value(OFF)
            #Pin(cable_8).value(OFF)
            #Pin(cable_9).value(ON)
            
            #Pin(cable_10).value(OFF)
            #Pin(cable_11).value(OFF)
            #Pin(cable_12).value(ON)
            
            Pin(cable_1).value(OFF)
            Pin(cable_2).value(OFF)
            Pin(cable_3).value(ON)
                
            Pin(cable_4).value(ON)
            Pin(cable_5).value(OFF)
            Pin(cable_6).value(OFF)
                
            Pin(cable_7).value(OFF)
            Pin(cable_8).value(OFF)
            Pin(cable_9).value(ON)
            
            Pin(cable_10).value(OFF)
            Pin(cable_11).value(OFF)
            Pin(cable_12).value(ON)

            
        #fin modo a = 3
            
        if(modo_a == 4 and estado_cableado_norte == ON ):
            
            print("mostrando patron norte")
            
            estado_cableado_a = OFF
            estado_cableado_b = OFF
            estado_cableado_c = OFF
            estado_cableado_d = OFF
            estado_cableado_e = OFF
            estado_cableado_f = OFF
            estado_cableado_g = OFF
            estado_cableado_h = OFF
            estado_cableado_s = OFF
            
            estado_cableado_rojos = OFF;
            estado_cableado_amarillos = OFF;
            estado_cableado_verdes = OFF;
            estado_cableado_oeste = OFF;
            estado_cableado_este = OFF;
            estado_cableado_norte = OFF;
            estado_cableado_sur = OFF;
            
            ultimo_cambio_seg = hora
                
#             Pin(cable_1).value(OFF)
#             Pin(cable_2).value(OFF)
#             Pin(cable_3).value(ON)
#                 
#             Pin(cable_4).value(OFF)
#             Pin(cable_5).value(OFF)
#             Pin(cable_6).value(ON)
#                 
#             Pin(cable_7).value(ON)
#             Pin(cable_8).value(OFF)
#             Pin(cable_9).value(OFF)
#             
#             Pin(cable_10).value(OFF)
#             Pin(cable_11).value(OFF)
#             Pin(cable_12).value(ON)

            Pin(cable_1).value(ON)
            Pin(cable_2).value(OFF)
            Pin(cable_3).value(OFF)
                
            Pin(cable_4).value(OFF)
            Pin(cable_5).value(OFF)
            Pin(cable_6).value(ON)
                
            Pin(cable_7).value(OFF)
            Pin(cable_8).value(OFF)
            Pin(cable_9).value(ON)
            
            Pin(cable_10).value(OFF)
            Pin(cable_11).value(OFF)
            Pin(cable_12).value(ON)

            cuenta = intervalo_2;
            intervaloSig = 0;
            segundos = 0;
            ultimo_cambio_seg = hora;

            tiempo = 0;
            tiempo_a = 0;
            tiempo_b = 0;
            
        #fin modo a = 4
        
        if(modo_a == 5 and estado_cableado_sur == ON):
            
            print("mostrando patron sur")
            
            estado_cableado_a = OFF
            estado_cableado_b = OFF
            estado_cableado_c = OFF
            estado_cableado_d = OFF
            estado_cableado_e = OFF
            estado_cableado_f = OFF
            estado_cableado_g = OFF
            estado_cableado_h = OFF
            estado_cableado_s = OFF
            
            estado_cableado_rojos = OFF;
            estado_cableado_amarillos = OFF;
            estado_cableado_verdes = OFF;
            estado_cableado_oeste = OFF;
            estado_cableado_este = OFF;
            estado_cableado_norte = OFF;
            estado_cableado_sur = OFF;
            
            ultimo_cambio_seg = hora
                
            #Pin(cable_1).value(OFF)
            #Pin(cable_2).value(OFF)
            #Pin(cable_3).value(ON)
#        
            #Pin(cable_4).value(OFF)
            #Pin(cable_5).value(OFF)
            #Pin(cable_6).value(ON)
#                 
            #Pin(cable_7).value(ON)
            #Pin(cable_8).value(OFF)
            #Pin(cable_9).value(OFF)
#             
            #Pin(cable_10).value(ON)
            #Pin(cable_11).value(OFF)
            #Pin(cable_12).value(OFF)

            Pin(cable_1).value(OFF)
            Pin(cable_2).value(OFF)
            Pin(cable_3).value(ON)
                
            Pin(cable_4).value(OFF)
            Pin(cable_5).value(OFF)
            Pin(cable_6).value(ON)
                
            Pin(cable_7).value(ON)
            Pin(cable_8).value(OFF)
            Pin(cable_9).value(OFF)
            
            Pin(cable_10).value(OFF)
            Pin(cable_11).value(OFF)
            Pin(cable_12).value(ON)

            
        #fin modo a = 5
        #print(segundos)
        
        if(modo_a == 6 and estado_cableado_rojos == ON):
            
            print("mostrando patron rojo")

            estado_cableado_a = OFF
            estado_cableado_b = OFF
            estado_cableado_c = OFF
            estado_cableado_d = OFF
            estado_cableado_e = OFF
            estado_cableado_f = OFF
            estado_cableado_g = OFF
            estado_cableado_h = OFF
            estado_cableado_s = OFF
            
            estado_cableado_rojos = OFF;
            estado_cableado_amarillos = OFF;
            estado_cableado_verdes = OFF;
            estado_cableado_oeste = OFF;
            estado_cableado_este = OFF;
            estado_cableado_norte = OFF;
            estado_cableado_sur = OFF;
            
            ultimo_cambio_seg = hora
                
            Pin(cable_1).value(OFF)
            Pin(cable_2).value(OFF)
            Pin(cable_3).value(ON)
                
            Pin(cable_4).value(OFF)
            Pin(cable_5).value(OFF)
            Pin(cable_6).value(ON)
                
            Pin(cable_7).value(OFF)
            Pin(cable_8).value(OFF)
            Pin(cable_9).value(ON)
            
            Pin(cable_10).value(OFF)
            Pin(cable_11).value(OFF)
            Pin(cable_12).value(ON)
            
            
            
        #fin modo a = 6
            
        if(modo_a == 7 and estado_cableado_amarillos == ON):
            
            print("mostrando patron amarillos")
            
            estado_cableado_a = OFF
            estado_cableado_b = OFF
            estado_cableado_c = OFF
            estado_cableado_d = OFF
            estado_cableado_e = OFF
            estado_cableado_f = OFF
            estado_cableado_g = OFF
            estado_cableado_h = OFF
            estado_cableado_s = OFF
            
            estado_cableado_rojos = OFF;
            estado_cableado_amarillos = OFF;
            estado_cableado_verdes = OFF;
            estado_cableado_oeste = OFF;
            estado_cableado_este = OFF;
            estado_cableado_norte = OFF;
            estado_cableado_sur = OFF;
            
            segundos = 0
            ultimo_cambio_seg = hora
                
            Pin(cable_1).value(OFF)
            Pin(cable_2).value(ON)
            Pin(cable_3).value(OFF)
                
            Pin(cable_4).value(OFF)
            Pin(cable_5).value(ON)
            Pin(cable_6).value(OFF)
                
            Pin(cable_7).value(OFF)
            Pin(cable_8).value(ON)
            Pin(cable_9).value(OFF)
            
            Pin(cable_10).value(OFF)
            Pin(cable_11).value(ON)
            Pin(cable_12).value(OFF) 

            cuenta = intervalo_2;
            intervaloSig = 0;
            segundos = 0;
            ultimo_cambio_seg = hora;

            tiempo = 0;
            tiempo_a = 0;
            tiempo_b = 0;
            
            
            
         #fin modo a = 7
        if contador > 0 and modo_a != 1 and segundos == contador and temporizador == True :
            print("RESET")
            reset_mode(1,0)
        
        
      
    
    #fin semaforos_a

def validateJSON(jsonData):
    try:
        if isinstance(jsonData,str):
            if jsonData.find(":") > -1: 
                return True;
            else:
                return False
        else:
            return True
        json.loads(jsonData)
    except ValueError as err:
        return False
    return False
    
def process_msg(topic, msg):
    
    global modo_a, contador, segundos, cuenta
    global intervalo_1, intervalo_3, intervalo_5, intervalo_7
    
    codigo = ""
    
    print(msg)
    
    #data_out=json.dumps(mensajito)
    
    #print(data_out)
    
    #print(type(msg))
    
    isValid = False
    
    isValid = validateJSON(msg)
    
    #print(isValid)
    
    if isValid == False :
        
        codigo = msg
        contador = 0
    
    else:
        
        m_in=json.loads(msg)
        
        for key, value in m_in.items():
            print(key, value)
            #codigo = i
            #contador = int(m_in[i])
            codigo = key
            contador = int(value)
            #print(i, m_in[i])
    
    
    #print("el codigo es: ")
    #print(codigo)
    #print(contador)
    
    if codigo == '"NORMAL"':
        segundos = 0
        print("entro en verde")
        #modo_a = 1
        reset_mode(1, contador)
    
    elif codigo == '"NORTE"' or codigo == "NORTE":
        print("entro en norte")
        #modo_a = 4
        if contador > 0:
            #intervalo_1 = contador
            reset_mode(4, contador)
        else:
            segundos = 0
            reset_mode(4, contador)
    
    elif codigo == '"OESTE"' or codigo == "OESTE":
        print("entro en oeste")
        #modo_a = 3
        if contador > 0:
            #intervalo_3 = contador
            reset_mode(3, contador)
        else:
            segundos = 0
            reset_mode(3, contador)
    
    elif codigo == '"SUR"' or codigo == "SUR":
        print("entro en sur")
        #modo_a = 5
        if contador > 0:
            #intervalo_5 = contador
            reset_mode(5, contador)
        else:
            segundos = 0
            reset_mode(5, contador)
       
    elif codigo == '"ESTE"' or codigo == "ESTE":
        print("entro en este")
        #modo_a = 2
        if contador > 0:
            #intervalo_7 = contador
            reset_mode(2, contador)
        else:
            segundos = 0
            reset_mode(2, contador)
    
    
       
    elif codigo == '"ROJOS"' or codigo == "ROJOS":
        print("entro en rojito")
        #modo_a = 6
        segundos = 0
        reset_mode(6, contador)
    
    elif codigo == '"AMARILLOS"' or codigo == "AMARILLOS":
        print("entro en amarillito")
        #modo_a = 7
        segundos = 0
        reset_mode(7, contador)
    
    elif codigo == '"ALTO"' or codigo == "ALTO":
        print("entro en detener")
        #modo_a = 7
        segundos = 0
        reset_mode(1, 0)
    
        
    print(modo_a)
    #process_mode()
    

     
def sub_cb(topic, msg):
  print((topic, msg))
  if topic == topic_sub:
    print('ESP received message')
    decode_msg = msg.decode('UTF-8')
    print((msg, decode_msg))
    process_msg(topic, decode_msg)

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  client.publish(topic_pub,"Activo")
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  reset()

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()
  

while True:
  try:
    client.check_msg()
    semaforos_a()
    if (time.time() - last_message) > message_interval:
      #msg = b'Activo #%d' % counter
      msg = b'Activo cliente ' + client_id
      client.publish(topic_pub, msg)
      last_message = time.time()
      counter += 1
   
        
  except OSError as e:
    restart_and_reconnect()

# a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# a.bind(('', 80))
# a.listen(3)



    

#fin setup
    
# def web_page():
# 
#   html =  """
#     <h1><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Control Leds</h1></b><br>
#     <body>
# 
#         <b>&nbsp;Modos&nbsp;&nbsp;</b>
#         <a href="/?modo1=on"><button id="modo1" style='width:100px; height:35px; background-color: #00ff00'>Modo semaforo</button></a>&nbsp;&nbsp;
# 
# 
#         <a href="/?modo2=on"><button id="modo2" style='width:100px; height:35px; background-color: #00ff00'>Modo verde un sentido</button></a>&nbsp;&nbsp;
# 
# 
#         <a href="/?modo3=on"><button id="modo3" style='width:100px; height:35px; background-color: #00ff00'>Modo verde un sentido 2</button></a>&nbsp;&nbsp;
# 
# 
#         <a href="/?modo4=on"><button id="modo4" style='width:100px; height:35px; background-color: #00ff00'>Modo verde un sentido 3</button></a>&nbsp;&nbsp;
#         
# 
#         <a href="/?modo5=on"><button id="modo5" style='width:100px; height:35px; background-color: #ff5252'>Modo luces en rojo</button></a>&nbsp;&nbsp;
#         
# 
#         <a href="/?modo6=on"><button id="modo6" style='width:100px; height:35px; background-color: #FFFF00'>Modo luces en amarillo</button></a>&nbsp;&nbsp;
#     
#     <script language = "JavaScript">
#         function isMode1(){
#          
#             let url = window.location.href
#             let busqueda = url.search("modo");
#             
#             if(busqueda != -1){
#             
#                 let busqueda2 = url.search("modo1");
#             
#                 if( busqueda2 != -1){
#                     document.getElementById("modo1").click()
#                 }
#             }else{
#                 document.getElementById("modo1").click()
#             }
#             
#         }
#         
#         isMode1()
#     </script>
#     </body>
#     """
#   return html
# #fin web
# 
# def levantar_web():
#     global a
#     global modo_a
#     global segundos
#     
#     conn,addr = a.accept()
#     print('Nueva conexion desde:  %s' % str(addr))
#     request = conn.recv(1024)
#     print('Solicitud = %s' % str(request))
#     request = str(request)
#     
#     if (request.find('/?modo1=on') == 6):
#         print('Estado: Modo semaforo Encendido')
#         modo_a = 1
#         
#     else:
#         
#         if (request.find('/?modo2=on') == 6):
#             print('Estado Modo luz verde un sentido')
#             modo_a = 2
#         
#         elif (request.find('/?modo3=on') == 6):
#             print('Estado Modo luz verde un sentido 2')
#             modo_a = 3
#         
#         elif (request.find('/?modo4=on') == 6):
#             print('Estado Modo luz verde un sentido 3')
#             modo_a = 4
#         
#         elif (request.find('/?modo5=on') == 6):
#             print('Estado Modo rojo encendido')
#             modo_a = 5
#     
#         elif (request.find('/?modo6=on') == 6):
#             print('Estado Modo amarillo encendido')
#             modo_a = 6
#             
#         else:
#             modo_a = 1
#       
#       
#     response = web_page()
#     conn.send('HTTP/1.1 200 OK\n')
#     conn.send('Content-Type: text/html\n')
#     conn.send('Connection: close\n\n')
#     conn.sendall(response)
#     conn.close()
#         
#     
#         
#     

#setup()



#while 1:
    #levantar_web()
    #semaforos_a()