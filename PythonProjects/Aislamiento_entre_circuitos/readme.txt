"Protocolo" de toma de pruebas para script "test_3.py"

se pueden cambiar los filtros pero ya que estan limitados por las etiquetas del instrumento de medida, se
considero el siguiente cirterio de etiquetas y orden de toma de medidas para el uso de filtros.

No es ideal, ya que es necesario trabajo humano. :/


Cuando el circuito corresponde a Barra ---> Level B vacio, Level C num del circuito de referencia

Es necesario indicar el numero de Diferenciales presentes en el tablero, y ademas la cantidad de circuitos por diferencial
para el correcto funcionamiento del script.

Etiquetas:

    "Level B" = Circuito_A
    "Level C" = Circuito_B


Orden --> rotulado:

1°    F-F = L-N
2°    F-N = L-N
3°    N-F = L-N
4°    N-N = L-N

5°    T-F = L-PE
6°    T-N = N-PE 
