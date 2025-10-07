// Path: static/main.js
import { HttpClienteGateway } from "./js/infrastructure/HttpClienteGateway.js";
import { ListarClientes } from "./js/use_cases/ListarClientes.js";
import { ObtenerClientePorId } from "./js/use_cases/ObtenerClientePorId.js";
import { ClientePresenter } from "./js/presenters/ClientePresenter.js";
import { ClientesView } from "./js/ui/ClientesView.js";
import { ClientesController } from "./js/controllers/ClientesController.js";
import { TabsController } from "./js/controllers/TabsController.js";
import { TokenView } from "./js/ui/TokenView.js";
import { TokenController } from "./js/controllers/TokenController.js";
import { ProductosVentaView } from "./js/ui/ProductosVentaView.js";
import { ProductosVentaController } from "./js/controllers/ProductosVentaController.js";

// 1) Infraestructura
const repo = new HttpClienteGateway({ baseUrl: "/api/xubio" });

// 2) Casos de uso
const listarClientes = new ListarClientes({ repo });
const obtenerClientePorId = new ObtenerClientePorId({ repo });

// 3) Presentador + Vista
const presenter = new ClientePresenter();
const view = new ClientesView({ tableContainerId: "clientes-table-container", clientesTabId: "clientes-tab" });
const tokenView = new TokenView({ containerId: "tab-token" });
const productosVentaView = new ProductosVentaView({ containerId: "tab-productos" });

// 4) Controlador
const clientesController = new ClientesController({
  listarClientes,
  obtenerClientePorId,
  presenter,
  view
});
const tokenController = new TokenController({ view: tokenView });
const productosVentaController = new ProductosVentaController({ view: productosVentaView });

// 5) Tabs
const tabs = new TabsController({
  onTabChange: (name) => {
    if (name === "clientes") {
      console.log("[LOG] Cargando clientes...");
      clientesController.cargarListado();
    }
    if (name === "token") {
      console.log("[LOG] Cargando token...");
      tokenController.cargarToken();
    }
    if (name === "productos") {
      console.log("[LOG] Cargando productos venta...");
      productosVentaController.cargarListado();
    }
    // No cargar nada en "inicio"
  }
});

tabs.init();

// Carga inicial solo si Clientes ya está activo
if (view.isClientesActive()) {
  console.log("[LOG] Tab clientes activo al cargar la página.");
  clientesController.cargarListado();
}
