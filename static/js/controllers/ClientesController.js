// Path: static/js/controllers/ClientesController.js
export class ClientesController {
  constructor({ listarClientes, obtenerClientePorId, presenter, view }) {
    this.listarClientes = listarClientes;
    this.obtenerClientePorId = obtenerClientePorId;
    this.presenter = presenter;
    this.view = view;
  }

  async cargarListado() {
    try {
      this.view.showLoading("Cargando clientes...");
      const clientes = await this.listarClientes.execute();
      const vm = this.presenter.toTableViewModel(clientes);
      this.view.renderTable(vm);
      this.view.onClickClienteId((id) => this.mostrarDetalle(id));
      console.info("[INFO] Tabla de clientes renderizada.");
    } catch (err) {
      console.error("[ERROR] Al listar clientes:", err);
      this.view.showError(err);
    }
  }

  async mostrarDetalle(id) {
    try {
      this.view.showLoading("Cargando cliente...");
      const cliente = await this.obtenerClientePorId.execute(id);
      if (!cliente) return this.view.showWarning("No se encontró el cliente.");
      const vm = this.presenter.toDetailViewModel(cliente);
      this.view.renderDetail(vm);
      this.view.onClickVolver(() => this.cargarListado());
      console.info("[INFO] Cliente mostrado en formato vertical.");
    } catch (err) {
      console.error("[ERROR] Al obtener cliente:", err);
      this.view.showError(err);
    }
  }
}
