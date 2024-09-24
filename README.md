# SIR_estocastico
Proyecto final de la materia simulaciones computacionales en física

Para finalizar el curso de Simulaciones computacionales en física 2023 implementé el modelo SIR estocástico para estudiar desarrollo de epidemias.
Para el proyecto implementé en gillespie_cl.py por un lado los métodos necesarios como son:
- el SIR usando el algoritmo de Gillespie, sir_gillespie();
- los histogramas para los tamaños de brotes en el threshold epidémico, G();
- la distribución de probabilidad cumulativa relacionada a estos histogramas, U();
- un método para armar la ecdf a partir de los datos obtenidos de las simulaciones, ecdf();
- un último método para armar la relación del paper de referencia ( http://dx.doi.org/10.1140/epjb/e2012-30117-0 figura 4) y simplificar la obtención de gráficos a partir de las cantidades buscadas

Los diversos archivos en formato .pdf o .png son outputs de los 3 scripts presentes en este repo. Los números delante de cada nombre indican a que ejercicio responde ese plot.
Los scripts gillespie_{n}.py están armados para dar directamente outputs que sirvan para responder al ejercicio "n" del proyecto

chequeo.pdf no es mas que una superposición de la curva de infectados en función del tiempo según dan los modelos determinista y estocásticos. 
Esto sirve como parte de una demostración de que el modelo estocástico así construido puede reproducir los resultados ya estudiados en el curso para el modelo determinista.

El primer ejercicio se responde directamente con los gráficos que salen de gillespie_1.py. Ahí se ve que si bien la población total es idéntica, teniendo distintos valores de r_0 es drásticamente diferente la probabilidad de tener brotes mas grandes.

Para el segundo ejercicio se encaró esto con un método un tanto mas flexible que solo este caso empleado en gillespie_2.py .
Si estuvieramos estudiando un modelo que en su evolución temporal con un parámetro que ocurra una transición, se podría determinar haciendo algo así.
Conceptualmente la metodología implica acercarnos alrededor del valor crítico del parámetro y ver como evoluciona en promedio el sistema solo unos pocos pasos temporales.
Con unos pocos pasos se ve la diferencia en comportamiento y esto reafirma la existencia del valor crítico que en este caso sería R_0=1; de todas formas este modelo se puede estudiar analíticamente y el valor ya es conocido.

El intento de reproducir los gráficos de la publicación previamente mencionada se llevó a cabo en varios pasos. 
Todos ellos en el threshold epidémico (R_0= 1).
En primer lugar se construyó la G(n) sería la probabilidad de tener un brote de tamanño "n". A partir de esta se reprodujo la curva U_n(N) que es la probabilidad de tener un brote de tamaño mayor o igual que n (ver 3_u_n.pdf). Con esto se puede obtener la U_n(\inf) ya que converge correctamente.
Por otro lado a partir de las simulaciones se obtuvieron los histogramas "experimentales".
Para ver como varía la probabilidad de tener un brote mayor a n y también verificar que escala con N^2/3 graficó entonces U_n(N)/U_n(\inf) en el eje de las ordenadas y en el eje de las abscisas n/N^2/3.
Efectivamente se ve una dependencia similar a la que muestra en la figura 4 el paper de referencia en lo que 3_graphs_3000.pdf muestra en la 3er gráfica.
