// Path: static/js/presenters/ClientePresenter.js
export class ClientePresenter {
  // De entidades -> filas para tabla
  toTableViewModel(clientes) {
    return clientes.map(c => ({
      id: c.id,
      nombre: c.nombre,
      razonSocial: c.razonSocial,
      email: c.email,
      telefono: c.telefono,
      cuit: c.cuit,
      provincia: c.provincia,
      direccion: c.direccion,
      actualizado: c.actualizado
    }));
  }

  // De entidad -> detalle
  toDetailViewModel(c) {
    return [
      ["ID", c.id],
      ["Nombre", c.nombre],
      ["Razón Social", c.razonSocial],
      ["Email", c.email],
      ["Teléfono", c.telefono],
      ["CUIT", c.cuit],
      ["Provincia", c.provincia],
      ["Dirección", c.direccion],
      ["Actualizado", c.actualizado],
    ];
  }
}
