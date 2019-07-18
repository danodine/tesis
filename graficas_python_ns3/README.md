# Graficas
## Rendimiento
     
      Formula:
      R = Pr / Ts
      
      historia:
      R = Rendimiento
      Pr = Paquetes recibidos
      Ts = Tiempo de simulación
      
![img](https://github.com/jrsarango/graficas_python_ns3/blob/master/recurso_imagenes/rendimiento.png)
      
## Tasa de envío de paquetes
      Formula:
      TEP = (Pr / Pe) * 100 %
      
      historia:
      TEP = Tasa de envío de paquetes
      PR = Paquetes recibidos (solo paquetes con protocolo aodv)
      Pe = Paquetes enviados (todos los paquetes)
      x= numero de nodos
      y= % del numero de paquetes de AODV
      
![img](https://github.com/jrsarango/graficas_python_ns3/blob/master/recurso_imagenes/tasa_envio_paquetes.png)
      
## Retardo 
      Formula:
      Rp = Sr / Pr
      
      historia:
      Rp = Retardo promedio
      Sr = Suma del retardo (suma de "Time delta from previous captured frame:")
      Pr = Paquetes recibidos (solo aodv)
      
      suma de retardo es la diferencia del tiempo en que se envio hasta que se entrego
      x= numero nodos
      y= tiempo

![img](https://github.com/jrsarango/graficas_python_ns3/blob/master/recurso_imagenes/retardo_promedio.png)
      
## Perdida de paquetes
      Formula:
      Pp = Pt - Pr
      
      historia:
      Pp = Paquetes perdidos
      Pt = Paquetes transmitidos (todos los paquetes)
      Pr = Paquetes recibidos (solo aodv)
      
      
  ![img](https://github.com/jrsarango/graficas_python_ns3/blob/master/recurso_imagenes/perdida_paquetes.png)
