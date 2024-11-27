from reportlab.pdfgen import canvas
from models import Proforma, OrdenServicio, Cliente, Vehiculo
import os

def generar_pdf_proforma(proforma_id):
    proforma = Proforma.query.get(proforma_id)
    if not proforma:
        raise Exception("Proforma no encontrada")
    
    cliente = Cliente.query.get(proforma.vehiculo.cliente_id)
    vehiculo = Vehiculo.query.get(proforma.vehiculo_id)

    file_path = f'static/proforma_{proforma_id}.pdf'
    c = canvas.Canvas(file_path)
    c.drawString(100, 800, f"Proforma ID: {proforma.id}")
    c.drawString(100, 780, f"Cliente: {cliente.nombre}")
    c.drawString(100, 760, f"Vehículo: {vehiculo.marca} {vehiculo.modelo}")
    c.drawString(100, 740, f"Total: S/{proforma.total}")
    c.save()

    return file_path

def generar_pdf_orden(orden_id):
    orden = OrdenServicio.query.get(orden_id)
    if not orden:
        raise Exception("Orden no encontrada")
    
    proforma = Proforma.query.get(orden.proforma_id)
    cliente = Cliente.query.get(proforma.vehiculo.cliente_id)
    vehiculo = Vehiculo.query.get(proforma.vehiculo_id)

    file_path = f'static/orden_{orden_id}.pdf'
    c = canvas.Canvas(file_path)
    c.drawString(100, 800, f"Orden ID: {orden.id}")
    c.drawString(100, 780, f"Estado: {orden.estado}")
    c.drawString(100, 760, f"Cliente: {cliente.nombre}")
    c.drawString(100, 740, f"Vehículo: {vehiculo.marca} {vehiculo.modelo}")
    c.drawString(100, 720, f"Proforma Total: S/{proforma.total}")
    c.save()

    return file_path
