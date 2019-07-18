# -*- coding: utf-8 -*-

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from subprocess import check_output
import sys

"""
Variables globales
"""
lista_nodos = dict()
path_base = os.getcwd()

def generate_data():
    for file in os.listdir(path_base):
        if file.endswith(".pcap"):
            jsonData = check_output(["tshark", "-r", path_base + "/" + file, "-T", "json"])
            jsonData = jsonData.decode("utf-8")

            print (pathbase + file)
            print (jsonData)
            lista_nodos[file] = json.loads(jsonData)


def generate_data_nodos():
    # nodos_data = dict()
    nodos_data2 = dict()
    dir_nodos = ["/ipv4"]
    for ip in dir_nodos:
        for num_nodos in os.listdir(path_base+ip):
            if not os.path.isfile(num_nodos):
                dir_pcap = path_base+ip + "/" + num_nodos
                for file in os.listdir(dir_pcap):
                    if file.endswith(".pcap"):
                        abosolute_dir = dir_pcap + "/" + file
                        jsonData = check_output(["tshark", "-r", "-k" ,abosolute_dir, "-T", "json"])
                        jsonData = jsonData.decode("utf-8")
                        # print (pathbase + file)
                        # print (jsonData)
                        if ip in nodos_data2:
                            if num_nodos not in nodos_data2[ip]:
                                nodos_data2[ip][num_nodos] = {}
                            nodos_data2[ip][num_nodos].update({file: json.loads(jsonData)})
                            # nodos_data2[ip].update({num_nodos: files})
                            # nodos_data[num_nodos].update({file: json.loads(jsonData)})
                        else:
                            nodos_data2[ip] = {num_nodos: {file: json.loads(jsonData)}}
                            # nodos_data[num_nodos] = {file: json.loads(jsonData)}

    return nodos_data2


def graph_rendimiento(lista_nodos):
    """
    Funcion para graficar tiempo de envio de paquetes.
    paquete->_source->layers->frame->frame.time_relative
    :return: grafica
    """
    package_for_seconds = dict()
    ip_data = generate_data_nodos()
    keys = list(ip_data.keys())
    for key_ip, ip in ip_data.items():
        for pcaps in ip.values():
            for nodo in pcaps.values():
                for paquete in nodo:
                    tiempo_paquete = paquete["_source"]["layers"]["frame"]["frame.time_relative"]
                    time = tiempo_paquete.split(".")
                    if int(time[0]) in package_for_seconds:
                        if key_ip not in package_for_seconds[int(time[0])]:
                            package_for_seconds[int(time[0])].update({key_ip: 1})
                        else:
                            package_for_seconds[int(time[0])][key_ip] += 1
                    else:
                        if key_ip == keys[0]:
                            package_for_seconds[int(time[0])] = {key_ip: 1, keys[1]: 0}


    # rellenar datos
    tamanio = len(package_for_seconds)
    for valor in range(max(package_for_seconds.keys())):
        if valor not in package_for_seconds:
            package_for_seconds[valor] = {keys[0]: 0}
    dictlistx = []
    dictlisty = []
    order = sorted(package_for_seconds.items())
    for value in order:
        dictlistx.append(int(value[0]))
        dictlisty.append((int(value[1]["/ipv4"])))

    plt.ion()
    plt.plot(dictlistx, dictlisty)  # Los dibujamos

#def graph_rendimiento():
    #url: https://matplotlib.org/gallery/lines_bars_and_markers/cohere.html#sphx-glr-gallery-lines-bars-and-markers-cohere-py

    # Fixing random state for reproducibility
    #graph_time(lista_nodos)
    #fig, axs = plt.subplots()
    #axs.xticks(x, t)
    #axs.plot(x, s1, "g")
    #axs.set_xlim(0, 2)
    #axs.set_xlabel('time')
    #axs.set_ylabel('s1 and s2')
    #axs.grid(True)

    #plt.show()
    #pass


def graph_send_package():
    #nodos_data -(dict) .pcap - (list) - _source - layers - aodv or icmpv6
    nodos_data = generate_data_nodos()
    datos_ip = {}
    for key_ip, ip in nodos_data.items():
        data_nodos_grap = {}
        for key, num_nodos in ip.items():
            num_pkg_aodv_nodo = 0
            num_total_pkg = 0
            for pcap in num_nodos.values():
                for packague in pcap:
                    num_total_pkg += 1
                    if "aodv" in packague["_source"]["layers"]:
                        num_pkg_aodv_nodo += 1
            data_nodos_grap[key] = {"aodv": num_pkg_aodv_nodo, "total": num_total_pkg}
        datos_ip[key_ip] = data_nodos_grap

    plt.rcdefaults()
    fig, ax = plt.subplots(2)


    gra = {}
    for key_ip, ip in datos_ip.items():
        # data
        value_nodos = []
        name_nodos = []
        for key, data in ip.items():
            name_nodos.append(key + "Nodos")
            value_nodos.append(float(data["aodv"])/float(data["total"]))
        gra[key_ip] = {"name": name_nodos, "value": value_nodos,
                       "info_name": "\nTasa de envío de paquetes " + key_ip + "."}
    y_pos = np.arange(len(value_nodos))
    error = np.random.rand(len(name_nodos))
    count = 0
    for key, g in gra.items():
        ax[count].barh(g["name"], g["value"], xerr=error, align='center', color='orange', ecolor='black')
        ax[count].set_yticks(y_pos)
        ax[count].set_yticklabels(name_nodos)
        ax[count].invert_yaxis()  # labels read top-to-bottom
        ax[count].set_xlabel('%')
        ax[count].set_title(g["info_name"], pad=5.5)
        count += 1

    plt.show()


def graph_retardo():
    nodos = generate_data_nodos()

    datos_ip = {}
    for key_ip, ip in nodos.items():
        data_nodos_grap = {}
        for key, num_nodos in nodos.items():
            suma = 0
            num_pkg_aodv_nodo = 0
            for key_pcap, pcaps in num_nodos.items():
                for packague in pcaps.values():
                    for pkg in packague:
                        print(pkg["_source"]["layers"]["frame"]["frame.time_delta_displayed"])
                        suma += float(pkg["_source"]["layers"]["frame"]["frame.time_delta_displayed"])
                        if "aodv" in pkg["_source"]["layers"]:
                            num_pkg_aodv_nodo += 1
                if key_pcap not in data_nodos_grap:
                    data_nodos_grap[key_pcap] = {}
                data_nodos_grap[key_pcap].update({"sum": suma, "total_aodv": num_pkg_aodv_nodo})
        if key_ip not in datos_ip:
            datos_ip[key_ip] = {}
        datos_ip[key_ip].update(data_nodos_grap)
    plt.rcdefaults()
    fig, ax = plt.subplots(2)

    gra = {}
    for key_ip, ip in datos_ip.items():
        # data
        value_nodos = []
        name_nodos = []
        for key, data in data_nodos_grap.items():
            name_nodos.append(key + " Nodos")
            value_nodos.append(float(data["sum"])/float(data["total_aodv"]))
        gra[key_ip] = {"name": name_nodos, "value": value_nodos,
                       "info_name": "\nRetardo " + key_ip + "."}
    # print(value_nodos)
    y_pos = np.arange(len(value_nodos))   
    error = np.random.rand(len(name_nodos))
   
    

    count = 0
    for key, g in gra.items():
        ax[count].barh(g["name"], g["value"], xerr=error, align='center', color='green', ecolor='black')
        ax[count].set_yticks(y_pos)
        ax[count].set_yticklabels(name_nodos)
        ax[count].invert_yaxis()  # labels read top-to-bottom
        ax[count].set_xlabel('%')
        ax[count].set_title(g["info_name"], pad=5.5)
        # ax.barh(y_pos, value_nodos, xerr=error, align='center',
        #         color='green', ecolor='black')
        # ax.set_yticks(y_pos)
        # ax.set_yticklabels(name_nodos)
        # ax.invert_yaxis()  # labels read top-to-bottom
        # ax.set_xlabel('%')
        # ax.set_title('Retardo!')
        count += 1

    plt.show()


def graph_package_lost():
    # nodos_data -(dict) .pcap - (list) - _source - layers - aodv or icmpv6
    datos_ip = {}
    nodos = generate_data_nodos()
    for key_ip, ip in nodos.items():
        data_nodos_grap = {}
        for key, num_nodos in ip.items():
            num_pkg_aodv_nodo = 0
            num_total_pkg = 0
            for pcap in num_nodos.values():
                for packague in pcap:
                    num_total_pkg += 1
                    if "aodv" in packague["_source"]["layers"]:
                        num_pkg_aodv_nodo += 1
            data_nodos_grap[key] = {"aodv": num_pkg_aodv_nodo, "total": num_total_pkg}
        datos_ip[key_ip] = data_nodos_grap

    plt.rcdefaults()
    fig, ax = plt.subplots(2)

    gra = {}
    for key_ip, ip in datos_ip.items():
        # data
        value_nodos = []
        name_nodos = []
        for key, data in data_nodos_grap.items():
            name_nodos.append(key + " Nodos")
            value_nodos.append(int(data["total"])-int(data["aodv"]))
        gra[key_ip] = {"name": name_nodos, "value": value_nodos,
                       "info_name": "\nTasa de paqutes perdidos " + key_ip + "."}
    y_pos = np.arange(len(value_nodos))
    error = np.random.rand(len(name_nodos))

    count = 0
    for key, g in gra.items():
        ax[count].barh(g["name"], g["value"], xerr=error, align='center', color='green', ecolor='black')
        ax[count].set_yticks(y_pos)
        ax[count].set_yticklabels(name_nodos)
        ax[count].invert_yaxis()  # labels read top-to-bottom
        ax[count].set_xlabel('%')
        ax[count].set_title(g["info_name"], pad=5.5)
        # ax.barh(y_pos, value_nodos, xerr=error, align='center',
        #         color='green', ecolor='black')
        # ax.set_yticks(y_pos)
        # ax.set_yticklabels(name_nodos)
        # ax.invert_yaxis()  # labels read top-to-bottom
        # ax.set_xlabel('%')
        # ax.set_title('Retardo!')
        count += 1

    plt.show()


def main():  ## Your menu design here
    generate_data()
    print(30 * "-", "MENU", 30 * "-")
    print("Select the chart\n")
    print("Press to 1. Rendimiento")
    print("Press to 2. Tasa de envío de paquetes")
    print("Press to 3. Retardo")
    print("Press to 4. Perdida de paquetes")
    print("Press to 5. Salir")
    print(67 * "-")


loop = True

while loop:  ## While loop which will keep going until loop = False
    main()  ## Displays menu
    if len(sys.argv) > 1:
        choice = int(sys.argv[1])
    else:
        choice = int(input("Enter your choice [1-5]: "))

    if choice == 1:
        print("Generando gráfica de rendimiento...")
        graph_rendimiento(lista_nodos)
    elif choice == 2:
        print("Generando gráfica de tasa de envío de paquetes...")
        graph_send_package()
    elif choice == 3:
        print("Generando gráfica de retardo...")
        graph_retardo()
    elif choice == 4:
        print("Generando gráfica...")
        graph_package_lost()
    elif choice == 5:
        print("Exit!")

        loop = False  # This will make the while loop to end as not value of loop is set to False
    else:
        # Any integer inputs other than values 1-5 we print an error message
        input("Wrong option selection. Enter any key to try again..")


if __name__ == "__main__":
    main()
