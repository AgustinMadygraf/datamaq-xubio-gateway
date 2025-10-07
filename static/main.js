// Path: static/main.js
import { HttpClienteGateway } from "./js/infrastructure/HttpClienteGateway.js";
import { ListarClientes } from "./js/use_cases/ListarClientes.js";
import { ObtenerClientePorId } from "./js/use_cases/ObtenerClientePorId.js";
import { ClientePresenter } from "./js/presenters/ClientePresenter.js";
import { ClientesView } from "./js/ui/ClientesView.js";
import { ClientesController } from "./js/controllers/ClientesController.js";
import { TabsController } from "./js/controllers/TabsController.js";

// 1) Infraestructura
const repo = new HttpClienteGateway({ baseUrl: "/api/xubio" });

// 2) Casos de uso
const listarClientes = new ListarClientes({ repo });
const obtenerClientePorId = new ObtenerClientePorId({ repo });

// 3) Presentador + Vista
const presenter = new ClientePresenter();
const view = new ClientesView({ tableContainerId: "clientes-table-container", clientesTabId: "clientes-tab" });

// 4) Controlador
const clientesController = new ClientesController({
  listarClientes,
  obtenerClientePorId,
  presenter,
  view
});

// 5) Tabs
const tabs = new TabsController({
  onTabChange: (name) => {
    if (name === "clientes") {
      console.log("[LOG] Cargando clientes...");
      clientesController.cargarListado();
    }
  }
});

tabs.init();

// Carga inicial si Clientes ya está activo
if (view.isClientesActive()) {
  console.log("[LOG] Tab clientes activo al cargar la página.");
  clientesController.cargarListado();
}
