import sqlite3
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import src.db.queries as commerceDa
import src.utils.email_send as email_serv
import src.utils.file_serv as file_serv

# Función para solicitar y validar fechas
def get_valid_date(prompt):
    while True:
        date_str = input(f"{prompt} (formato YYYY-MM): ")
        try:
            date = datetime.strptime(date_str, "%Y-%m")
            return date_str
        except ValueError:
            print("⚠️ Formato incorrecto. Inténtalo de nuevo.")

# Pedir fechas al usuario
print("📅 Ingrese el rango de fechas para calcular las comisiones:")
start_date = get_valid_date("Fecha de inicio")
end_date = get_valid_date("Fecha de fin")

api_calls_per_month = commerceDa.get_all_api_calls(start_date, end_date)
grouped_data = {}
facturas_resumidas = []  # Lista para almacenar todas las facturas
IVA = 0.19

if not api_calls_per_month:
    print("⚠️ No se encontraron resultados en el rango de fechas indicado.")
else:
    print("\n📜 Valores a cobrar por empresa: \n")
    # Se agrupa la información por empresa
    for entry in api_calls_per_month:
        commerce_id = entry["commerce_id"]
        if commerce_id not in grouped_data:
            grouped_data[commerce_id] = []
        grouped_data[commerce_id].append(entry)

# Procesar la información individualmente por empresa y en el rango de fechas
for commerce_id, records in grouped_data.items():
    commerce_info = commerceDa.get_all_commerce(commerce_id)
    commerce_name = commerce_info["commerce_name"]
    commerce_nit = commerce_info["commerce_nit"]
    commerce_email = commerce_info["commerce_email"]

    total_comision = 0

    # Obtener descuentos
    discounts = commerceDa.get_commerce_discount(commerce_id)
    # Obtener planes
    planes = commerceDa.get_commerce_plans(commerce_id)

    # Recorre los reportes de cada una de las empresas
    for record in records:
        success_calls = record["calls_successful"]
        monthly_fee = 0  # Comisión o cuota

        # Determinar el tipo de plan y asignar el costo
        if commerce_info["commerce_plan_type"] == 'Fijo':
            for plan in planes:
                monthly_fee = plan["monthly_fee"]
        elif commerce_info["commerce_plan_type"] == 'Variable':
            for plan in planes:
                if plan["max_api_calls"] is None and plan["min_api_calls"] <= success_calls:
                    monthly_fee = plan["monthly_fee"]
                elif plan["min_api_calls"] <= success_calls <= plan["max_api_calls"]:
                    monthly_fee = plan["monthly_fee"]

        # Calcular comisión sin descuento
        comision_base = success_calls * monthly_fee

        # Aplicar descuento según el número de llamadas API exitosas
        descuento_aplicado = 0
        for discount in discounts:
            min_calls = discount["min_api_calls"]
            max_calls = discount["max_api_calls"]
            discount_percent = discount["monthly_discount_percent"]

            # Si max_api_calls es None, significa "sin límite superior"
            if max_calls is None and success_calls >= min_calls:
                descuento_aplicado = discount_percent
            elif min_calls <= success_calls <= max_calls:
                descuento_aplicado = discount_percent

        # Aplicar descuento a la comisión base
        total_comision += comision_base * (1 - descuento_aplicado / 100)

    # Calcular total con IVA
    total_con_iva = total_comision * (1 + IVA)

    # Crear la factura del comercio y almacenarla en la lista global
    factura_comercio = [
        f"{start_date} - {end_date}", commerce_name, commerce_nit,
        f"{total_comision:.2f}", f"{IVA:.2f}", f"{total_con_iva:.2f}", commerce_email
    ]
    facturas_resumidas.append(factura_comercio)
    
    print(f"🏢 Empresa: {commerce_name} | 💰 Total con IVA: {total_con_iva:.2f} COP | 🎯 Descuento aplicado: {descuento_aplicado}%")

# 📜 Resumen Final de Facturas
print("\n📜 Resumen de Facturas Generadas:\n")
print(f"{'Fecha':<25} {'Nombre':<25} {'NIT':<15} {'Comisión':<12} {'IVA':<12} {'Total':<12} {'Correo':<30}")
print("-" * 140)


for factura in facturas_resumidas:
    fecha, nombre, nit, comision, iva, total, correo = factura
    print(f"{fecha:<25} {nombre:<25} {nit:<15} {comision:<12} {iva:<12} {total:<12} {correo:<30}")

print("\n")
if facturas_resumidas: 
    file_serv.guardar_copia_seguridad(facturas_resumidas, start_date, end_date)

# 🔹 Enviar los correos después de mostrar el resumen
print("\n📧 Enviando facturas por correo...")
for factura in facturas_resumidas:
    fecha, nombre, nit, comision, iva, total, correo = factura
    email_serv.enviar_resumen_facturas([factura], correo)
    print(f"✅ Se ha enviado exitosamente el correo a {correo}")

print("\n🚀 Proceso finalizado.")
input("Presiona Enter para salir...")
