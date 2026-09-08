# 📊 Auditoría Operativa y Logística - E-commerce Textil (End-to-End Data Pipeline)

Este proyecto es una simulación de un entorno real de datos para un e-commerce textil. El objetivo principal fue resolver un conflicto operativo crítico utilizando datos: el área de manufactura culpaba a logística por las demoras en las entregas, mientras que logística afirmaba que los paquetes no estaban listos a tiempo.

Mediante la construcción de un pipeline ETL completo y un dashboard interactivo, se pasó de evidencia anecdótica a la toma de decisiones fundamentada en datos, identificando los verdaderos cuellos de botella de la línea de producción.

## 🛠️ Tecnologías Utilizadas

- **Lenguaje principal:** Python 3.12
- **Procesamiento y Limpieza (ETL):** Pandas
- **Base de Datos:** SQL Server (Modelado relacional)
- **Conexión BD:** SQLAlchemy, pyodbc
- **Visualización y Análisis:** Power BI, DAX avanzado

## ⚙️ Arquitectura del Proyecto

El flujo de trabajo se dividió en tres fases principales:

1. **Extracción y Transformación (Python / Pandas):**
   - Procesamiento de archivos sucios simulados.
   - Estandarización robusta de fechas ambiguas para evitar la distorsión de meses y días.
   - Manejo de valores atípicos y nulos generados en la carga inicial de los sistemas.
   - Modularización del código (`src/extract`, `src/transform`, `src/load`).

2. **Carga y Almacenamiento (SQL Server):**
   - Diseño de un esquema de Data Warehouse con tablas de hechos (`fact_ventas`) y dimensiones (`logistica`, `productos`, `fechas`, etc.).
   - Inserción de datos limpios y tipados para un consumo ágil.

3. **Análisis y Visualización (Power BI / DAX):**
   - Modelado de datos en Power BI.

## 💡 Hallazgos Clave del Negocio

El análisis de los datos arrojó conclusiones que cambiaron el paradigma operativo de la empresa:

* 🟢 **El Mito de la Logística:** Se demostró irrefutablemente que el proveedor logístico retira los paquetes en un tiempo óptimo (promedio de 12 horas). Logística no era el responsable de las demoras.
* 🔴 **El Verdadero Cuello de Botella:** El problema residía en la línea de producción interna. Específicamente, la confección del producto **"Buzo Canguro"** demoraba hasta 5 veces más (120 horas) que el resto del catálogo debido a su complejidad de ensamblaje, estancando el circuito de despacho.
* 📈 **Control de Calidad:** Se observó una tendencia positiva en la curva de aprendizaje, evidenciada por la reducción mes a mes de la tasa de artículos defectuosos.
