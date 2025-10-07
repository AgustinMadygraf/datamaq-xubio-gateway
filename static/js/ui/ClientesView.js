// Path: static/js/ui/ClientesView.js
export class ClientesView {
  constructor({
    tableContainerId = "clientes-table-container",
    clientesTabId = "clientes-tab"
  } = {}) {
    this.$container = document.getElementById(tableContainerId);
    this.$clientesTab = document.getElementById(clientesTabId);
  }

  isClientesActive() {
    return this.$clientesTab?.classList.contains("active");
  }

  showLoading(text = "Cargando...") {
    this.$container.innerHTML =
      `<div class="text-center my-3"><div class="spinner-border"></div> ${text}</div>`;
  }

  showInfo(msg) {
    this.$container.innerHTML = `<div class="alert alert-info">${msg}</div>`;
  }

  showWarning(msg) {
    this.$container.innerHTML = `<div class="alert alert-warning">${msg}</div>`;
  }

  showError(err) {
    this.$container.innerHTML =
      `<div class="alert alert-danger">Error: ${err?.message ?? err}</div>`;
  }

  renderTable(rows) {
    if (!rows?.length) return this.showInfo("No hay clientes para mostrar.");
    const head = `
      <thead><tr>
        <th>ID</th><th>Nombre</th>
      </tr></thead>`;
    const body = rows.map(r => `
      <tr>
        <td><a href="#" class="cliente-id-link text-primary text-decoration-underline" data-id="${r.id}">${r.id}</a></td>
        <td>${r.nombre}</td>
      </tr>
    `).join("");

    this.$container.innerHTML =
      `<table class="table table-striped table-bordered table-sm">${head}<tbody>${body}</tbody></table>`;
  }

  renderDetail(pairs) {
    const rows = pairs.map(([k, v]) =>
      `<tr><th class="text-end">${k}</th><td>${v}</td></tr>`).join("");
    this.$container.innerHTML = `
      <table class="table table-bordered w-auto mx-auto mt-4"><tbody>${rows}</tbody></table>
      <div class="text-center">
        <button class="btn btn-secondary mt-3" id="volver-clientes">Volver a la tabla</button>
      </div>`;
  }

  onClickClienteId(handler) {
    this.$container.querySelectorAll(".cliente-id-link").forEach(a => {
      a.addEventListener("click", (e) => {
        e.preventDefault();
        handler(a.getAttribute("data-id"));
      });
    });
  }

  onClickVolver(handler) {
    const btn = document.getElementById("volver-clientes");
    if (btn) btn.addEventListener("click", handler);
  }
}
