"""
Path: src/interface_adapter/presenters/cliente_presenter.py
"""

from src.entities.cliente import Cliente

class ClientePresenter:
    "Presentador para la entidad Cliente"
    @staticmethod
    def to_dict(cliente: Cliente) -> dict:
        "Convierte un objeto Cliente a un diccionario con los campos principales del modelo extendido"
        return {
            "cliente_id": cliente.cliente_id,
            "nombre": cliente.nombre,
            "primer_apellido": cliente.primer_apellido,
            "segundo_apellido": cliente.segundo_apellido,
            "primer_nombre": cliente.primer_nombre,
            "otros_nombres": cliente.otros_nombres,
            "razon_social": cliente.razon_social,
            "nombre_comercial": cliente.nombre_comercial,
            "identificacion_tributaria": cliente.identificacion_tributaria,
            "digito_verificacion": cliente.digito_verificacion,
            "categoria_fiscal": cliente.categoria_fiscal,
            "provincia": cliente.provincia,
            "direccion": cliente.direccion,
            "email": cliente.email,
            "telefono": cliente.telefono,
            "codigo_postal": cliente.codigo_postal,
            "cuenta_venta_id": cliente.cuenta_venta_id,
            "cuenta_compra_id": cliente.cuenta_compra_id,
            "pais": cliente.pais,
            "localidad": cliente.localidad,
            "usr_code": cliente.usr_code,
            "lista_precio_venta": cliente.lista_precio_venta,
            "descripcion": cliente.descripcion,
            "es_cliente_extranjero": cliente.es_cliente_extranjero,
            "es_proveedor": cliente.es_proveedor,
            "cuit": cliente.cuit,
            "tipo_de_organizacion": cliente.tipo_de_organizacion,
            "responsabilidad_organizacion_item": cliente.responsabilidad_organizacion_item,
            "CUIT": cliente.CUIT,
            "actualizado_en": cliente.actualizado_en,
        }

    @staticmethod
    def list_to_dict(clientes: list[Cliente]) -> list[dict]:
        "Convierte una lista de objetos Cliente a una lista de diccionarios"
        return [ClientePresenter.to_dict(c) for c in clientes]
