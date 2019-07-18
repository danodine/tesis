# -*- coding: utf-8 -*-

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from subprocess import check_output
import collections

"""
Variables globales
"""
lista_nodos = dict()
path_base = os.getcwd()

def banner():
    print(u"\u001b[32m ")
    print("   ██████╗ ██████╗  █████╗ ███████╗██╗ ██████╗ █████╗ ███████╗")
    print("  ██╔════╝ ██╔══██╗██╔══██╗██╔════╝██║██╔════╝██╔══██╗██╔════╝")
    print("  ██║  ███╗██████╔╝███████║█████╗  ██║██║     ███████║███████╗")
    print("  ██║   ██║██╔══██╗██╔══██║██╔══╝  ██║██║     ██╔══██║╚════██║")
    print("  ╚██████╔╝██║  ██║██║  ██║██║     ██║╚██████╗██║  ██║███████║")
    print("   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝")
    print(u"\u001b[0m ")

def generate_data():
    for file in os.listdir(path_base):
        if file.endswith(".pcap"):
            jsonData = check_output(["tshark", "-r", path_base + "/" + file, "-T", "json"])
            jsonData = jsonData.decode("utf-8")

            # print (pathbase + file)
            # print (jsonData)
            lista_nodos[file] = json.loads(jsonData)


def generate_data_nodos():
    dir_nodos4 = "/ipv4"
    dir_nodos = "/ipv6"
    nodos_data4 = dict()
    nodos_data = dict()
    for num_nodos in os.listdir(path_base+dir_nodos):
        if not os.path.isfile(num_nodos):
            dir_pcap = path_base+dir_nodos + "/" + num_nodos
            for file in os.listdir(dir_pcap):
                if file.endswith(".pcap"):
                    abosolute_dir = dir_pcap + "/" + file
                    jsonData = check_output(["tshark", "-r", abosolute_dir, "-T", "json"])
                    jsonData = jsonData.decode("utf-8")
                    # print (pathbase + file)
                    # print (jsonData)
                    if num_nodos in nodos_data:
                        nodos_data[num_nodos].update({file: json.loads(jsonData)})
                    else:
                        nodos_data[num_nodos] = {file: json.loads(jsonData)}
    return nodos_data


def graph_rendimiento(lista_nodos):
    """
    Funcion para graficar tiempo de envio de paquetes.
    paquete->_source->layers->frame->frame.time_relative
    :return: grafica
    """
    package_for_seconds = dict()
    for nodo in lista_nodos.values():
        for paquete in nodo:
            tiempo_paquete = paquete["_source"]["layers"]["frame"]["frame.time_relative"]
            time = tiempo_paquete.split(".")
            if int(time[0]) in package_for_seconds:
                package_for_seconds[int(time[0])] += 1
            else:
                package_for_seconds[int(time[0])] = 1

    # rellenar datos
    for valor in range(max(package_for_seconds.keys())):
        if valor not in package_for_seconds:
            package_for_seconds[valor] = 0
    dictlistx = []
    dictlisty = []
    for key, value in package_for_seconds.items():
        dictlistx.append(int(key))
        dictlisty.append(int(value))

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
    # nodos_data -(dict) .pcap - (list) - _source - layers - aodv or icmpv6
    data_nodos_grap = {}
    nodos_data = generate_data_nodos()
    for key, num_nodos in nodos_data.items():
        num_pkg_aodv_nodo = 0
        num_total_pkg = 0
        for pcap in num_nodos.values():
            for packague in pcap:
                num_total_pkg += 1
                if "aodv" in packague["_source"]["layers"]:
                    num_pkg_aodv_nodo += 1
        data_nodos_grap[key] = {"aodv": num_pkg_aodv_nodo, "total": num_total_pkg}

    plt.rcdefaults()
    fig, ax = plt.subplots()

    # data
    value_nodos = []
    name_nodos = []
    for key, data in data_nodos_grap.items():
        name_nodos.append(key + " Nodos")
        value_nodos.append(float(data["aodv"])/float(data["total"]))
    y_pos = np.arange(len(value_nodos))
    error = np.random.rand(len(name_nodos))

    ax.barh(y_pos, value_nodos, xerr=error, align='center',
            color='green', ecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(name_nodos)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('%')
    ax.set_title('Tasa de envío de paquetes!')

    plt.show()

def graph_retardo():
    # Fixing random state for reproducibility
    np.random.seed(19680801)
    # nodos_data -(dict) .pcap - (list) - _source - layers - frame - frame.time_delta_displayed
    data_nodos_grap = {}
    nodos = generate_data_nodos()

    for key, num_nodos in nodos.items():
        suma = 0
        num_pkg_aodv_nodo = 0
        for pcap in num_nodos.values():
            for packague in pcap:
                suma += float(packague["_source"]["layers"]["frame"]["frame.time_delta_displayed"])
                if "aodv" in packague["_source"]["layers"]:
                    num_pkg_aodv_nodo += 1
        data_nodos_grap[key] = {"sum": suma, "total_aodv": num_pkg_aodv_nodo}
    plt.rcdefaults()
    fig, ax = plt.subplots()

    # Example data
    value_nodos = []
    name_nodos = []
    for key, data in data_nodos_grap.items():
        name_nodos.append(key + " Nodos")
        value_nodos.append(float(data["sum"]) / float(data["total_aodv"]))
    print(value_nodos)
    y_pos = np.arange(len(value_nodos))
    error = np.random.rand(len(name_nodos))

    ax.barh(y_pos, value_nodos, xerr=error, align='center',
            color='green', ecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(name_nodos)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('%')
    ax.set_title('Retardo!')

    plt.show()

def graph_package_lost():
    # nodos_data -(dict) .pcap - (list) - _source - layers - aodv or icmpv6
    data_nodos_grap = {}
    nodos = generate_data_nodos()
    for key, num_nodos in nodos.items():
        num_pkg_aodv_nodo = 0
        num_total_pkg = 0
        for pcap in num_nodos.values():
            for packague in pcap:
                num_total_pkg += 1
                if "aodv" in packague["_source"]["layers"]:
                    num_pkg_aodv_nodo += 1
        data_nodos_grap[key] = {"aodv": num_pkg_aodv_nodo, "total": num_total_pkg}

    plt.rcdefaults()
    fig, ax = plt.subplots()
    # Example data
    value_nodos = []
    name_nodos = []
    for key, data in data_nodos_grap.items():
        name_nodos.append(key + " Nodos")
        value_nodos.append(int(data["total"]) - int(data["aodv"]))
    print(value_nodos)
    y_pos = np.arange(len(value_nodos))
    error = np.random.rand(len(name_nodos))

    ax.barh(y_pos, value_nodos, xerr=error, align='center',
            color='green', ecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(name_nodos)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('%')
    ax.set_title('Retardo!')

    plt.show()


def main():  ## Your menu design here
    banner()
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
    choice = int(input("Enter your choice [1-5]: "))

    if choice == 1:
        print("Menu 1 has been selected")
        graph_rendimiento(lista_nodos)
    elif choice == 2:
        print("Menu 3 has been selected")
        graph_send_package()
    elif choice == 3:
        print("Menu 4 has been selected")
        graph_retardo()
    elif choice == 4:
        print("Menu 5 has been selected")
        graph_package_lost()
    elif choice == 5:
        print("Menu 6 has been selected")

        loop = False  # This will make the while loop to end as not value of loop is set to False
    else:
        # Any integer inputs other than values 1-5 we print an error message
        input("Wrong option selection. Enter any key to try again..")


if __name__ == "__main__":
    main()
