import os
from dotenv import load_dotenv
from google import genai

# 1. Cargar el archivo .env
load_dotenv(override=True)
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print(" ERROR: No se encontró la clave en el archivo .env")
else:
    client = genai.Client(api_key=api_key.strip())
    
    print("---  SISTEMA DE REGISTRO ACADÉMICO (Escala 1-10) ---")
    
    # 2. Captura de datos manual
    nombre = input("Nombre del estudiante: ")
    materia = input("Materia: ")
    asistencia = input("Porcentaje de asistencia (ej. 60%): ")
    
    print(" Nota: Ingresa calificaciones del 1 al 10 (Mínimo para aprobar: 7)")
    notas_input = input("Introduce las calificaciones separadas por comas (ej: 5.0, 7.5, 6.2): ")
    notas = [n.strip() for n in notas_input.split(",")]
    
    comentario = input("Duda o comentario del alumno: ")

    estudiante = {
        "id": nombre,
        "materia": materia,
        "asistencia": asistencia,
        "notas": notas,
        "comentario": comentario
    }

    print(f"\n Analizando riesgo de deserción para {nombre}...")

    try:
        # 3. Prompt con las nuevas reglas de calificación
        prompt = f"""
        Actúa como analista académico. 
        Analiza a este estudiante con los siguientes criterios:
        - Escala de calificación: 1 a 10.
        - Nota mínima aprobatoria: 7.0 (Cualquier nota menor a 7 es reprobatoria).
        
        Datos del estudiante: {estudiante}
        
        Genera un reporte que incluya:
        1. Estado académico (¿Está aprobado o reprobado según su promedio?).
        2. Análisis de riesgo: Si el promedio es menor a 7 Y la asistencia es baja, el riesgo es CRÍTICO.
        3. Análisis de sentimiento: ¿Cómo influye su comentario en su posible abandono?
        4. Acción recomendada: Sugerencia específica para que el alumno alcance el 7 mínimo.
        """

        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt
        )
        
        print("\n" + "="*50)
        print(f"           DIAGNÓSTICO ACADÉMICO: {nombre}")
        print("="*50)
        print(response.text)
        print("="*50)

    except Exception as e:
        print(f"\n Error: {e}")