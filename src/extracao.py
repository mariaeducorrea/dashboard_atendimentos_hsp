from conexao import connection
import csv

def export_data():
    conn = connection()
    cur = conn.cursor()

    query = """
    
    """
    
    cur.execute(query)

    rows = cur.fetchall()
    
    csv_file = "C:/Users/Administrador/Desktop/projetos/dashboard_atendimentos_hsp/dados/dados.csv"


    with open(csv_file, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["paciente", "convenio", "unidade","setor", "tipo_atendimento", "idade_paciente", "data_atendimento", "hora_inicio", "data_alta", "hora_fim"])
        writer.writerows(rows)

    print("Consulta finalizada.")


    cur.close()
    conn.close()


export_data()
