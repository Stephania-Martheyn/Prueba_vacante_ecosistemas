from src.db.database import conectar_db

#Obtiene la cantidad de llamadas API exitosas y fallidas por comercio en un rango de fechas.
def get_all_api_calls(start_date, end_date):
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT commerce_id, 
               strftime('%Y-%m', date_api_call) AS year_month,
               SUM(CASE WHEN ask_status = 'Successful' THEN 1 ELSE 0 END) AS calls_successful, 
               SUM(CASE WHEN ask_status = 'Unsuccessful' THEN 1 ELSE 0 END) AS calls_unsuccessful
        FROM apicall
        WHERE date_api_call BETWEEN ? AND ?
        GROUP BY commerce_id, year_month
        ORDER BY commerce_id, year_month
    ''', (start_date, end_date))
    
    result = cursor.fetchall()  
    conn.close()

    result_list = []
    for row in result:
        resultado_dict = {
            "commerce_id": row[0],
            "year_month": row[1],
            "calls_successful": row[2],
            "calls_unsuccessful": row[3]
        }
        result_list.append(resultado_dict)

    return result_list

#Obtiene la información de un comercio por su ID.
def get_all_commerce(commerce_id):
    
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT commerce_name, commerce_nit, commerce_email, commerce_status,commerce_plan_type
        FROM commerce 
        WHERE commerce_id = ?
    ''', (commerce_id,)) 
    
    commerce = cursor.fetchone() 
    conn.close() 

    if commerce:
        return {
            "commerce_name": commerce[0],
            "commerce_nit": commerce[1],
            "commerce_email": commerce[2],
            "commerce_status": commerce[3],
            "commerce_plan_type": commerce[4]
        }
    return None  

def get_commerce_plans(commerce_id):
    conn = conectar_db()
    cursor = conn.cursor()
    
    query = "SELECT commerce_id, commerce_nit, min_api_calls, max_api_calls, monthly_fee FROM commerce_plans WHERE commerce_id = ?"
    cursor.execute(query, (commerce_id,))
    
    plans = cursor.fetchall()  
    
    conn.close()  
    
    # Convertir el resultado en una lista de diccionarios
    result_list = [
        {
            "commerce_id": row[0],
            "commerce_nit": row[1],
            "min_api_calls": row[2],
            "max_api_calls": row[3],
            "monthly_fee": row[4]
        }
        for row in plans
    ]
    
    return result_list  # Retornar lista de diccionarios

def get_commerce_discount(commerce_id):
    conn = conectar_db()
    cursor = conn.cursor()
    
    query = "SELECT commerce_id, commerce_nit, min_api_calls, max_api_calls, monthly_discount_percent FROM commerce_discounts WHERE commerce_id = ?"
    cursor.execute(query, (commerce_id,))
    
    plans = cursor.fetchall()  
    
    conn.close()  
    
    # Convertir el resultado en una lista de diccionarios
    result_list = [
        {
            "commerce_id": row[0],
            "commerce_nit": row[1],
            "min_api_calls": row[2],
            "max_api_calls": row[3],
            "monthly_discount_percent": row[4]
        }
        for row in plans
    ]
    
    return result_list  # Retornar lista de diccionarios
