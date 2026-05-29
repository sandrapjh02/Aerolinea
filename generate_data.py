import pandas as pd
import numpy as np
from faker import Faker
import random
import os

fake = Faker("es_CO")
random.seed(42)
np.random.seed(42)

# 📁 RUTA DE SALIDA (Ajustada a tu perfil)
OUTPUT_PATH = r"C:\Users\Sandra Jimenez\Documents\AD14_BeTek\Proyecto\Entrega"
os.makedirs(OUTPUT_PATH, exist_ok=True)

print(f"📁 Guardando en: {OUTPUT_PATH}")

# =========================================================
# ✈️ TABLAS BASE
# =========================================================

# AVION
avion = pd.DataFrame({
    "id_avion": range(1, 6),
    "modelo": ["B737", "A320", "B787", "A321", "B737MAX"],
    "matricula": [fake.bothify("HK-####") for _ in range(5)],
    "anio_fabricacion": np.random.randint(2005, 2023, 5),
    "estado_avion": ["activo"]*5,
    "capacidad_total": [180, 150, 280, 220, 170]
})

# CLASE
clase = pd.DataFrame({
    "id_clase": [1, 2, 3],
    "codigo_clase": ["ECO", "BUS", "FIR"],
    "nombre_clase": ["Económica", "Ejecutiva", "Primera"]
})

# AEROPUERTO (Nombres reales de Colombia para impacto ejecutivo)
ciudades_col = ["Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena", "Pereira", "Bucaramanga", "Santa Marta", "Cúcuta", "San Andrés"]
aeropuerto = pd.DataFrame({
    "id_aeropuerto": range(1, 11),
    "codigo_iata": ["BOG", "MDE", "CLO", "BAQ", "CTG", "PEI", "BGA", "SMR", "CUC", "ADZ"],
    "nombre": [f"Aeropuerto Internacional {c}" for c in ciudades_col],
    "ciudad": ciudades_col,
    "pais": ["Colombia"]*10
})

# RUTA
ruta = pd.DataFrame({
    "id_ruta": range(1, 11),
    "aeropuerto_origen": np.random.randint(1, 6, 10), 
    "aeropuerto_destino": np.random.randint(1, 11, 10)
})

# VUELO PROGRAMADO (Distribución horaria para simular operación real)
vuelo_programado = pd.DataFrame({
    "id_vuelo_programado": range(1, 11),
    "id_ruta": range(1, 11),
    "numero_vuelo": [fake.bothify("AV###") for _ in range(10)],
    "dias_operacion": ["Lun-Dom"]*10,
    "hora_salida_programada": ["06:00:00", "08:30:00", "11:00:00", "14:20:00", "16:00:00", "18:30:00", "20:00:00", "22:15:00", "07:00:00", "12:00:00"],
    "hora_llegada_programada": ["08:00:00", "10:30:00", "13:00:00", "16:20:00", "18:00:00", "20:30:00", "22:00:00", "00:15:00", "09:00:00", "14:00:00"],
    "temporada_operacion": ["Regular"]*10,
    "tipo_servicio": ["Regular"]*10,
    "tiempo_min_conexion": [60]*10
})

# =========================================================
# ✈️ VUELO INSTANCIA (Efecto Cascada y Retrasos Realistas)
# =========================================================
N = 50000

fechas = [fake.date_between(start_date="-1y", end_date="today") for _ in range(N)]
ids_vuelo_prog = np.random.randint(1, 11, N)

estados_vuelo = []
for i in range(N):
    idx = ids_vuelo_prog[i] - 1
    hora_str = vuelo_programado.iloc[idx]["hora_salida_programada"]
    hora_h = int(hora_str.split(':')[0])
    prob_retraso = 0.08 if hora_h < 12 else 0.42
    estados_vuelo.append(np.random.choice(["Aterrizado", "Demorado", "Cancelado"], p=[1-prob_retraso-0.03, prob_retraso, 0.03]))

from datetime import datetime, timedelta

horas_salida_real = []
horas_llegada_real = []
retrasos_minutos = []

for i in range(N):
    idx = ids_vuelo_prog[i] - 1
    hora_prog_str = vuelo_programado.iloc[idx]["hora_salida_programada"]
    hora_prog = datetime.strptime(hora_prog_str, "%H:%M:%S")
    estado = estados_vuelo[i]

    if estado == "Demorado":
        retraso = random.randint(20, 120)
    elif estado == "Aterrizado":
        retraso = random.randint(-5, 15)
    else:
        retraso = 0

    salida_real = hora_prog + timedelta(minutes=retraso)
    llegada_real = salida_real + timedelta(hours=2)

    horas_salida_real.append(salida_real.strftime("%H:%M:%S"))
    horas_llegada_real.append(llegada_real.strftime("%H:%M:%S"))
    retrasos_minutos.append(retraso if estado == "Demorado" else None)

vuelo_instancia = pd.DataFrame({
    "id_vuelo_instancia": range(1, N+1),
    "id_vuelo_programado": ids_vuelo_prog,
    "id_avion": np.random.randint(1, 6, N),
    "fecha_operacion": fechas,
    "hora_salida_real": horas_salida_real,      # ← LÍNEA NUEVA
    "hora_llegada_real": horas_llegada_real,    # ← LÍNEA NUEVA
    "Retraso_Minutos": retrasos_minutos,        # ← LÍNEA NUEVA
    "estado_vuelo": estados_vuelo,
    "puerta_embarque": [fake.bothify("A##") for _ in range(N)],
    "clima_afectado": np.random.choice([1, 0], N, p=[0.12, 0.88]),
    "motivo_cancelacion": np.random.choice(["Mantenimiento", "Clima", "Tripulación", "Tráfico Aéreo", "N/A"], N, p=[0.4, 0.2, 0.1, 0.1, 0.2])
})

# =========================================================
# 💰 TARIFA Y TARIFA_VUELO (Yield Management)
# =========================================================
# Definimos 'tarifa' explícitamente para evitar el error de image_78b38d.png
tarifa = pd.DataFrame({
    "id_tarifa": [1, 2, 3, 4, 5],
    "id_clase": [1, 1, 2, 2, 3],
    "codigo_tarifa": ["BAS", "FLEX", "BUS", "BUSF", "FIRST"],
    "precio_base": [250000, 450000, 950000, 1300000, 2800000],
    "moneda": ["COP"]*5,
    "anticipacion_minima": [0, 7, 0, 0, 0],
    "permite_cambio": [0, 1, 1, 1, 1],
    "permite_reembolso": [0, 0, 1, 1, 1],
    "restricciones": [""]*5,
    "reglas_penalizacion": [""]*5
})

# Ocupación realista (Campana de Gauss centrada en 82%)
factores_ocupacion = np.clip(np.random.normal(82, 10, N), 30, 100)

tarifa_vuelo = pd.DataFrame({
    "id_tarifa_vuelo": range(1, N+1),
    "id_vuelo_instancia": range(1, N+1),
    "id_tarifa": np.random.randint(1, 6, N),
    "cupo_asignado": np.random.randint(100, 250, N),
    "cupo_disponible": np.random.randint(0, 40, N),
    "nivel_demanda": np.random.choice(["Alta", "Media", "Baja"], N, p=[0.3, 0.5, 0.2]),
    "factor_ocupacion": factores_ocupacion,
    "sobreventa_permitida": np.random.randint(0, 5, N)
})

# =========================================================
# 👤 PASAJERO (Segmentación de Clientes)
# =========================================================
niveles_fidelidad = np.random.choice(["básico", "oro", "platino"], N, p=[0.75, 0.20, 0.05])

pasajero = pd.DataFrame({
    "id_pasajero": range(1, N+1),
    "nombre_completo": [fake.name() for _ in range(N)],
    "genero": np.random.choice(["M", "F"], N),
    "fecha_nacimiento": [fake.date_of_birth(minimum_age=18, maximum_age=70) for _ in range(N)],
    "email": [fake.email() for _ in range(N)],
    "telefono": [fake.phone_number() for _ in range(N)],
    "nacionalidad": ["Colombia"]*N,
    "tipo_documento": ["CC"]*N,
    "documento_pasajero": [fake.random_number(digits=10) for _ in range(N)],
    "nivel_fidelidad": niveles_fidelidad,
    "contacto_emergencia": [fake.name() for _ in range(N)]
})

# =========================================================
# 🎟️ PNR Y SEGMENTO (Precios Dinámicos por Anticipación)
# =========================================================
fechas_reserva = []
precios_finales = []

for i in range(N):
    fecha_op = vuelo_instancia.iloc[i]["fecha_operacion"]
    # Anticipación promedio 15 días (Exponencial)
    dias_anticipacion = int(np.clip(np.random.exponential(15), 1, 90))
    fecha_res = pd.to_datetime(fecha_op) - pd.Timedelta(days=dias_anticipacion)
    fechas_reserva.append(fecha_res)
    
    # Yield Management: Precio sube si compras tarde
    mult_urgencia = 1.0 if dias_anticipacion > 14 else 2.4
    precio_base_clase = tarifa.iloc[random.randint(0, 4)]["precio_base"]
    precios_finales.append(precio_base_clase * mult_urgencia)

pnr = pd.DataFrame({
    "id_pnr": range(1, N+1),
    "id_pasajero": range(1, N+1),
    "codigo_localizador": [fake.bothify("??###") for _ in range(N)],
    "fecha_reserva": fechas_reserva,
    "estado_reserva": np.random.choice(["Confirmada", "Cancelada"], N, p=[0.91, 0.09]),
    "forma_pago": np.random.choice(["Tarjeta", "PSE", "Efectivo"], N, p=[0.65, 0.25, 0.1]),
    "estado_pago": np.random.choice(["Pagado", "Pendiente"], N, p=[0.96, 0.04]),
    "monto_total": precios_finales,
    "canal_reserva": np.random.choice(["Web", "App", "Agencia"], N, p=[0.6, 0.3, 0.1]),
    "agencia_emisora": np.random.choice(["Directo", "Viajes Éxito", "Despegar"], N, p=[0.8, 0.1, 0.1])
})

segmento = pd.DataFrame({
    "id_segmento": range(1, N+1),
    "id_pnr": range(1, N+1),
    "id_pasajero": range(1, N+1),
    "id_vuelo_instancia": range(1, N+1),
    "id_tarifa_vuelo": range(1, N+1),
    "estado_segmento": pnr["estado_reserva"],
    "asiento_asignado": [fake.bothify("##A") for _ in range(N)],
    "precio_pagado": pnr["monto_total"],
    "impuestos": [p * 0.19 for p in precios_finales],
    "estado_checkin": np.random.choice(["Online", "Aeropuerto", "Pendiente"], N, p=[0.72, 0.20, 0.08]),
    "numero_ticket_electronico": [fake.bothify("AV########") for _ in range(N)]
})

# =========================================================
# 💾 EXPORTAR Y GENERAR MASTER (Solución a image_78b38d.png)
# =========================================================
tables = {
    "avion": avion,
    "clase": clase,
    "aeropuerto": aeropuerto,
    "ruta": ruta,
    "vuelo_programado": vuelo_programado,
    "vuelo_instancia": vuelo_instancia,
    "tarifa": tarifa,  # Variable ahora correctamente definida
    "tarifa_vuelo": tarifa_vuelo,
    "pasajero": pasajero,
    "pnr": pnr,
    "segmento_reserva": segmento
}

for name, df in tables.items():
    df.to_csv(f"{OUTPUT_PATH}/{name}.csv", index=False, encoding='utf-8-sig')
    print(f"✔ {name}.csv generado")

print("🔄 Generando MASTER para Power BI...")
df_master = segmento.copy()
df_master = df_master.merge(pnr, on=["id_pnr", "id_pasajero"], how="left")
df_master = df_master.merge(pasajero, on="id_pasajero", how="left")
df_master = df_master.merge(vuelo_instancia, on="id_vuelo_instancia", how="left")
df_master = df_master.merge(tarifa_vuelo, on="id_tarifa_vuelo", how="left")

df_master.to_csv(f"{OUTPUT_PATH}/MASTER.csv", index=False, encoding='utf-8-sig')
print("✅ Proceso completado exitosamente.")

# --- IMPORTACIONES (Van al puro inicio del archivo) ---
from sqlalchemy import create_engine, text
import pymysql

# --- BLOQUE DE CARGA A MYSQL (Al final de tu código actual) ---

# 1. Configura tus credenciales reales aquí
user = "root"          # Cambia por tu usuario (ej: root)
password = "" # Cambia por tu contraseña de MySQL
host = "localhost"
db = "aeropuerto_database"    # El nombre de tu base de datos en MySQL

# 2. Creamos la conexión
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{db}")

# 3. Ciclo de carga con protección de llaves foráneas
with engine.connect() as connection:
    print("🔓 Desactivando restricciones de llaves foráneas...")
    connection.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
    
    print("🚀 Cargando datos a MySQL...")
    for name, df in tables.items():
        # CAMBIO CLAVE: Usamos 'append' para no borrar la tabla.
        # Pero primero vaciamos la tabla manualmente para no duplicar datos.
        connection.execute(text(f"TRUNCATE TABLE {name};"))
        
        # Ahora insertamos los nuevos 50,000 registros
        df.to_sql(name, con=engine, if_exists='append', index=False)
        print(f"✔ Tabla {name} actualizada con éxito")
    
    connection.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
    connection.commit() # Aseguramos que los cambios se guarden

print("✅ ¡Proceso terminado exitosamente!")