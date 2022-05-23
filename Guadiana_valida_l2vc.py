#### LEYENDA ####
#! Cosas a corregir
#? Cosas a aclarar
#TODO PENDIENTE DE HACER

#https://python-para-impacientes.blogspot.com/2016/09/dar-color-las-salidas-en-la-consola.html
#ubicado en C:\Users\Marc\Documents\ADAMO\VENV_PYTHON


#* En esta version anyadimos la parte de Excel

import telnetlib
import getpass
import time
from colorama.ansi import Style
import pandas as pd
from colorama import Fore, Back


def introduce_credenciales():

    user = input ('Introduce el usuario: ')
    password = getpass.getpass()



    return user, password




def telnet(IP,user, password):

    error_auth = 'Error: Authentication fail'
    IP = str(IP)

    print (" ")
    print ("Realizando acceso telnet a: "+IP)
    print (" ")
    tn = telnetlib.Telnet(IP)
    a = tn.read_until(b'Username:')
    #print (a)
    tn.write(user.encode('ascii') + b"\n")
    #! De momento usar esta contrasena x0axV6gE6gNu
    b = tn.read_until(b'Password:')
    tn.write(password.encode('ascii') + b"\n")
    c = tn.read_until(b'-cs-20>', 2)
    #? Convertimos a String para validar si se autentica correctamente
    d = str(c)
    if error_auth in d:
        print ("Error de auth")
        print (" ")
        print ("El script no puede continuar ya que hay error de autenticacion")
        tn = 'error_salir'
        return tn
    
    elif error_auth not in d:
        print ("ESTOY DENTRO DEL EQUIPO CON IP: " +IP)
        time.sleep(2)
        #print (d)
        print ("")
        print ("Eliminando limitación por buffer de la salida...")
        a = tn.write(b'screen-length 0 temporary'+ b"\n")
        #print (a)
        

    return tn


def display_interface_description_i_Eth_Trunk100(tn):

    print ("Buscando la interfaz Eth-Trunk100 ...")
    a = tn.read_until(b'>',2)
    print (a)
    tn.write(b'dis int des | i Eth-Trunk100'+b' \n')
    a = tn.read_until(b'>',2)
    print (a)
    return a

def parse_display_interface_description_i_Eth_Trunk100(a):


    a=str(a)
    a=a.replace('\\r','')
    lineas=a.split('\\n')


    for elemento in lineas: 
        #? He tenido que anyadir el service para el equipo mad-itx-service-01
        #TODO Deberia encontrar un metodo para todos los hostname
        if '-cs-2' in elemento:
            print ("esto deberia ser el hostname: "+elemento)
            
            hostname = elemento
            break
        
        
            

    lista_hostname.append(hostname)

    print ("La lista se deberia ir incrementando")
    print (lista_hostname)

    Eth_Trunk = 'KO'

    for elemento in lineas:
        if 'Eth-Trunk100' in elemento:
            Eth_Trunk = 'OK'
            if 'up      up' in elemento:
                print (elemento)
                
                lista_eth_trunk_100.append("UP")



            elif 'down    down' in elemento:
                print ('esta down!!')
                
                lista_eth_trunk_100.append("DOWN")


            else: 

                Eth_Trunk = 'KO'

    if Eth_Trunk == 'KO':

        lista_eth_trunk_100.append("KO")

    print(lista_eth_trunk_100)


    #TODO Pasar a EXCEL 
    return lista_hostname,lista_eth_trunk_100


def dis_int_des_i_402851(tn):
    print ("Buscando interfaces fisicas de Telefonica ...")
    a = tn.read_until(b'>',2)
    #print (a)
    tn.write(b'dis int des | i {402851-'+b' \n')
    a = tn.read_until(b'>',2)
    #print (a)
    return a


def parse_dis_int_des_i_402851(a, interfaz_up, interfaz_down, interfaz_admin_down, interfaces_total):

    a=str(a)
    a=a.replace('\\r','')
    lineas=a.split('\\n')



    for elemento in lineas: 
        if 'XGE0/0/' in elemento:
            if 'up      up' in elemento: 
                #print (elemento)
                #print ("deberia estar UP")
                interfaz_up = interfaz_up+1
            elif 'down    down' in elemento: 
                #print (elemento)
                #print ("deberia estar DOWN")
                interfaz_down = interfaz_down+1

            elif '*down   down' in elemento: 
                #print (elemento)
                #print ("debeira estar administrativamente DOWN")
                interfaz_admin_down = interfaz_admin_down+1

    interfaces_total.append(str(interfaz_up)+'-'+str(interfaz_down)+'-'+str(interfaz_admin_down))

    print (interfaces_total)
    
    #TODO Pasar a EXCEL 
    return interfaces_total

def dis_int_des_i_ID166(tn):

    print ("Buscando Vlanif de Telefonica")
    a = tn.read_until(b'>',2)
    print (a)
    tn.write(b'dis int des | i ID:166'+b' \n')
    a = tn.read_until(b'>',2)
    print (a)
    return a

def parse_dis_int_des_i_ID166(a):

    #TODO Aisla las Vlanif

    cont = 0
    Vlan_if_total = []
    a=str(a)
    a=a.replace('\\r','')
    lineas=a.split('\\n')


    for elemento in lineas:
        if 'Vlanif' in elemento: 
            cont = cont +1
            #Vlan_if_total.append(elemento)
            print (elemento)
            a = elemento.split(' ')
            Vlan_if_total.append(a[0]) 
            
    cantidad_vlanif.append(cont)

    if cont == 0:
        time.sleep(3)
        print ("NO hay vlan para este caso")
        cantidad_vlanif.append("N/A")

    print (Vlan_if_total)


    return Vlan_if_total

    

def dis_mpls_l2vc_interface(tn,a):

    cont_l2vc_down = 0
    cont_l2vc_up = 0
    
    mpls_l2vc = 'OK'
    print ("Viendo las interfaces mpls l2vc con las VLAN obtenidas anteriormente")
    b = tn.read_until(b'>',2)
    for elemento in a:
        #print ("Este es el eleento que hay dentro de mpls l2vc")
        #print (elemento)
        tn.write(b'dis mpls l2vc interface '+str(elemento).encode('ascii') + b'  | i VC state  \n')
        c = tn.read_until(b'-cs-2', 2)
        if 'down' in str(c):
            mpls_l2vc = 'KO'
            print ("al menos un mpls l2vc KO")
            cont_l2vc_down = cont_l2vc_down + 1
            
    

        elif 'up' in str(c):
            print (c)
            cont_l2vc_up = cont_l2vc_up + 1

            #print ("TODO CORRECTO")

    print ("Total mpls l2vc up: "+str(cont_l2vc_up))
    print ("Total mpls l2vc down: "+str(cont_l2vc_down))
    lista_cont_l2vc_down.append(cont_l2vc_down)
    lista_cont_l2vc_up.append(cont_l2vc_up)

    if mpls_l2vc == 'KO':
        mpls_l2vc_status.append('KO')
        print (mpls_l2vc_status)

        return mpls_l2vc_status,lista_cont_l2vc_up,lista_cont_l2vc_down

    elif mpls_l2vc == 'OK':
        mpls_l2vc_status.append('OK')
        print (mpls_l2vc_status)

        #TODO Pasar a EXCEL 
        return mpls_l2vc_status,lista_cont_l2vc_up,lista_cont_l2vc_down



def dis_curr_interface_Eth_Trunk_100(tn):

    print ("Extrayendo la configuración del Eth-Trunk100")
    b = tn.read_until(b'>', 2)
    tn.write(b'dis curr interface Eth-Trunk 100'+ b' \n')
    b = tn.read_until(b'>', 2)
    c = str(b)
    c = c.replace('\\r', '')
    c=c.split('\\n')


    return c


def deteccion_mode_lacp_Eth_Trunk_100(a):




    print ('AQUI AQUI')
    print (a)
    for elemento in a: 
        print (Back.RED+Fore.WHITE+elemento+Style.RESET_ALL)
        if 'mode lacp' in elemento: 
            mode_lacp_detectado.append('OK')


            return mode_lacp_detectado

    mode_lacp_detectado.append('KO')

    print (mode_lacp_detectado)

    return mode_lacp_detectado



def display_hostname_y_quit(tn):
    print ("Extrayendo el Hostname del equipo ...")
    b = tn.read_until(b'>', 2)
    tn.write(b'display version'+ b' \n') 
    b = tn.read_until(b'>', 2)

    c=str(b)
    c=c.replace('\\r', '')
    lineas=c.split('\\n')

    for linea in lineas:
        if '>' in linea:
            hostname=linea.replace('<','')
            hostname=hostname.replace('>\'','')
    tn.write(b'quit'+ b' \n') 
    print("Cerrando sesión del equipo: ", hostname)
    print('\n.\n.\n\.')


   
    return hostname

def creacion_df_equipo(output_hostname, IP, output_display_interface_description, output_interfaz_vlan_up,output_interfaz_vlan_down,output_parse_dis_mpls_l2vc_state_up_i_Vlanif,output_parse_dis_mpls_l2vc_state_down_i_Vlanif):

    info_equipo = []
    info_equipo.append(IP)
    info_equipo.append(" ")
    for linea in output_display_interface_description:
        info_equipo.append(linea)
    info_equipo.append(" ")
    
    info_equipo.append("Vlanif UP")
    for linea in output_interfaz_vlan_up:
        info_equipo.append(linea)
    info_equipo.append(" ")
    
    info_equipo.append("Vlanif DOWN")
    for linea in output_interfaz_vlan_down:
        info_equipo.append(linea)
    info_equipo.append(" ")

    info_equipo.append("l2vc UP")
    for linea in output_parse_dis_mpls_l2vc_state_up_i_Vlanif:
        info_equipo.append(linea)
    info_equipo.append(" ")

    info_equipo.append("l2vc DOWN")
    for linea in output_parse_dis_mpls_l2vc_state_down_i_Vlanif:
        info_equipo.append(linea)
    info_equipo.append(" ")

    col_names=[output_hostname]
    df = pd.DataFrame(list(info_equipo), columns = col_names)
    print (df)
    return df


def apertura_fichero_excel(a,b,c,d,e,f,g): #Parametros de entrada del excel

    fecha=time.strftime("%Y-%m-%d_%H-%M")
    writer = pd.ExcelWriter ('Comprobaciones_Guadiana.xlsx')
        
    col_names=['Hostname', 'Eth-Trunk100', 'Interfaces up-down-admin_down', 'l2vc Status','l2vc up', 'l2vc down','MODE LACP']
    df_resumen = pd.DataFrame(list(zip(a, b, c, d, e, f,g)), columns = col_names)
    df_resumen.to_excel(writer, sheet_name="Resumen", index=False)
    writer.save()

    return writer


def guardado_excel(writer, df_info_equipo, output_hostname):

    try:
        df_info_equipo.to_excel(writer, sheet_name=output_hostname, index=False)
        writer.save()
        print("Información de :", output_hostname, " guardada")

    except:
        print ("ERROR: No se pudo guardar la info de: ", output_hostname)

    return

def cierre_fichero_excel(writer):
    #print("Guardando fichero excel")
    #writer.save()
    writer.close()
    print("Fichero excel cerrado y guardado")
    
    return

## MAIN 

print ("Ejecutando script TELEFONICA")

user, password = introduce_credenciales()
lista_eth_trunk_100_up = []
lista_eth_trunk_100_down = []
lista_eth_trunk_100 = []
lista_hostname = []
interfaz_up = 0
interfaz_down = 0
interfaz_admin_down = 0
interfaces_total = []
Vlanif_KO = []
cantidad_vlanif = []
Vlan_if_total = []
mpls_l2vc_status = []
lista_cont_l2vc_down = []
lista_cont_l2vc_up = []
mode_lacp_detectado = []

with open ('IP_ITX.txt') as file:
    IPs = file.read().splitlines()



for IP in IPs: 
    tn = telnet(IP,user,password)
    output_display_interface_description_i_Eth_Trunk100 = display_interface_description_i_Eth_Trunk100(tn)
    
    lista_hostname,lista_eth_trunk_100 = parse_display_interface_description_i_Eth_Trunk100(output_display_interface_description_i_Eth_Trunk100)
    output_dis_int_des_i_402851 = dis_int_des_i_402851(tn)
    output_total_interfaces = parse_dis_int_des_i_402851(output_dis_int_des_i_402851, interfaz_up, interfaz_down, interfaz_admin_down, interfaces_total)
    output_dis_int_des_i_ID166 = dis_int_des_i_ID166(tn)
    output_Vlan_if_total = parse_dis_int_des_i_ID166(output_dis_int_des_i_ID166)
    output_mpls_l2vc_status,output_lista_cont_l2vc_up, output_lista_cont_l2vc_down = dis_mpls_l2vc_interface(tn, output_Vlan_if_total)
    output_dis_curr_interface_Eth_Trunk_100 = dis_curr_interface_Eth_Trunk_100(tn)
    output_deteccion_mode_lacp_Eth_Trunk_100 = deteccion_mode_lacp_Eth_Trunk_100(output_dis_curr_interface_Eth_Trunk_100)

    

writer_excel = apertura_fichero_excel(lista_hostname,lista_eth_trunk_100,output_total_interfaces,mpls_l2vc_status,output_lista_cont_l2vc_up, output_lista_cont_l2vc_down, output_deteccion_mode_lacp_Eth_Trunk_100)
cierre_fichero_excel(writer_excel)




