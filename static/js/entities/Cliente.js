// Path: static/js/entities/Cliente.js
export class Cliente {
  constructor({
    id = "",
    nombre = "",
    razonSocial = "",
    email = "",
    telefono = "",
    cuit = "",
    provincia = "",
    direccion = "",
    actualizado = ""
  } = {}) {
    this.id = id;
    this.nombre = nombre;
    this.razonSocial = razonSocial;
    this.email = email;
    this.telefono = telefono;
    this.cuit = cuit;
    this.provincia = provincia;
    this.direccion = direccion;
    this.actualizado = actualizado;
  }

  static fromApi(json = {}) {
    return new Cliente({
      id: json.cliente_id ?? json.id ?? "",
      nombre: json.nombre ?? json.primer_nombre ?? "",
      razonSocial: json.razon_social ?? json.nombre_comercial ?? "",
      email: json.email ?? "",
      telefono: json.telefono ?? "",
      cuit: json.cuit ?? json.CUIT ?? "",
      provincia: json?.provincia?.nombre ?? "",
      direccion: json.direccion ?? "",
      actualizado: json.actualizado_en ?? ""
    });
  }
}
