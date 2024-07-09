# SIR_estocastico
Proyecto final de la materia simulaciones computacionales en física

Para finalizar el curso de Simulaciones computacionales en física 2023 implementé el modelo SIR estocástico para estudiar desarrollo de epidemias.
Para desarrollar el proyecto implementé en gillespie_cl.py por un lado los métodos necesarios como son:
- el SIR usando el algoritmo de Gillespie, sir_gillespie();
- los histogramas para los tamaños de brotes en el threshold epidémico, G();
- la distribución de probabilidad cumulativa relacionada a estos histogramas, U();
- un método para armar la ecdf a partir de los datos obtenidos de las simulaciones, ecdf();
- un último método para armar la relación del paper de referencia ( http://dx.doi.org/10.1140/epjb/e2012-30117-0 figura 4) y simplificar la obtención de gráficos a partir de las cantidades buscadas
