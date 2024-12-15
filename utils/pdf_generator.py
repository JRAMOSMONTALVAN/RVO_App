from extensions import db  # Importamos db desde extensions.py
from flask import Flask, render_template

# Ejemplo de funciones para generar PDFs
def generar_pdf_proforma(id_proforma):
    try:
        # Lógica para generar PDF de una proforma (ejemplo)
        # Este ejemplo asume que tienes datos en tu base de datos relacionados con `id_proforma`
        proforma = db.session.query(Proforma).filter_by(id=id_proforma).first()
        if not proforma:
            raise ValueError("Proforma no encontrada")
        
        # Aquí iría la lógica para renderizar y crear el PDF
        
        return "PDF generado con éxito"
    except Exception as e:
        return f"Error al generar PDF: {str(e)}"

def generar_pdf_orden(id_orden):
    try:
        # Lógica para generar PDF de una orden (ejemplo)
        orden = db.session.query(Orden).filter_by(id=id_orden).first()
        if not orden:
            raise ValueError("Orden no encontrada")
        
        # Aquí iría la lógica para renderizar y crear el PDF
        
        return "PDF generado con éxito"
    except Exception as e:
        return f"Error al generar PDF: {str(e)}"
