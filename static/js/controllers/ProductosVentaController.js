export class ProductosVentaController {
  constructor({ view }) {
    this.view = view;
  }

  async cargarListado() {
    try {
      this.view.showLoading();
      const res = await fetch("/api/xubio/productos-venta");
      const data = await res.json();
      this.view.renderTable(data);
      this.view.onClickProductoId(id => this.mostrarDetalle(id));
    } catch (err) {
      this.view.showError(err);
    }
  }

  async mostrarDetalle(id) {
    try {
      this.view.showLoading("Cargando detalle...");
      const res = await fetch(`/api/xubio/productos-venta/${id}`);
      const data = await res.json();
      // Si el endpoint devuelve una lista, toma el primero
      const producto = Array.isArray(data) ? data[0] : data;
      this.view.renderDetail(producto);
      this.view.onClickVolver(() => this.cargarListado());
    } catch (err) {
      this.view.showError(err);
    }
  }
}