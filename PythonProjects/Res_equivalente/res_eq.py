import math

L_May = float(input("Lado mayor L [m]: "))
L_Men = float(input("Lado menor W [m]: "))
h = float(input("Profundidad enterramiento h [m]: "))

n = int(input("Numero de estratos n: "))

capas = []  
for i in range(1, n + 1):
    rho = float(input(f"rho_{i} [ohm*m]: "))
    if i < n:
        t = float(input(f"espesor_{i} [m]: "))
        capas.append({"rho": rho, "t": t})
    else:
        capas.append({"rho": rho, "t": None})  

A = L_May * L_Men
r = math.sqrt(A / math.pi)

def Fi(h_i):
    r0_sq = r*r - h*h
    q0_sq = 2.0 * r * (r + h)
    ui_sq = q0_sq + r0_sq + h_i*h_i
    disc = ui_sq*ui_sq - 4.0*q0_sq*r0_sq
    vi_sq = 0.5 * (ui_sq - math.sqrt(disc))
    return math.sqrt(1.0 - (vi_sq / r0_sq))

prof = []
acumulado = 0.0
for i in range(n - 1):
    acumulado += capas[i]["t"]
    prof.append(acumulado)

F = [0.0] + [Fi(d) for d in prof] + [1.0]

den = 0.0
for i in range(1, n + 1):
    w = F[i] - F[i - 1]
    den += w / capas[i - 1]["rho"]

rho_eq = 1.0 / den
print(f"rho_eq = {rho_eq}")
