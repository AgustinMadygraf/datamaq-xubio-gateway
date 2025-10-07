export class ProductosVentaView {
  constructor({ containerId = "tab-productos" } = {}) {
    this.$container = document.getElementById(containerId);
  }

  showLoading(text = "Cargando productos...") {
    this.$container.innerHTML =
      `<div class="text-center my-3"><div class="spinner-border"></div> ${text}</div>`;
  }

  showError(err) {
    this.$container.innerHTML =
      `<div class="alert alert-danger">Error: ${err?.message ?? err}</div>`;
  }

  showInfo(msg) {
    this.$container.innerHTML = `<div class="alert alert-info">${msg}</div>`;
  }

  renderTable(rows) {
    if (!rows?.length) return this.showInfo("No hay productos para mostrar.");
    const head = `
      <thead><tr>
        <th>ID</th>
        <th>Nombre</th>
      </tr></thead>`;
    const body = rows.map(r => `
      <tr>
        <td>
          <a href="#" class="producto-id-link text-primary text-decoration-underline" data-id="${r.productoid}">${r.productoid}</a>
        </td>
        <td>${r.nombre ?? ""}</td>
      </tr>
    `).join("");
    this.$container.innerHTML =
      `<table class="table table-striped table-bordered table-sm">${head}<tbody>${body}</tbody></table>`;
  }

  renderDetail(producto) {
    if (!producto) return this.showError("Producto no encontrado.");
    const keys = Object.keys(producto);
    const rows = keys.map(k => `
      <tr>
        <th class="text-end">${k}</th>
        <td>${typeof producto[k] === "object" ? JSON.stringify(producto[k]) : (producto[k] ?? "")}</td>
      </tr>
    `).join("");
    this.$container.innerHTML = `
      <table class="table table-bordered w-auto mx-auto mt-4"><tbody>${rows}</tbody></table>
      <div class="text-center">
        <button class="btn btn-secondary mt-3" id="volver-productos">Volver a la tabla</button>
      </div>`;
  }

  onClickProductoId(handler) {
    this.$container.querySelectorAll(".producto-id-link").forEach(a => {
      a.addEventListener("click", (e) => {
        e.preventDefault();
        handler(a.getAttribute("data-id"));
      });
    });
  }

  onClickVolver(handler) {
    const btn = document.getElementById("volver-productos");
    if (btn) btn.addEventListener("click", handler);
  }
}