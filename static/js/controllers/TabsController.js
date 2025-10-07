// Path: static/js/controllers/TabsController.js
export class TabsController {
  constructor({ onTabChange }) {
    this.onTabChange = onTabChange;
    this.$tabs = document.querySelectorAll(".tab");
    this.$contents = {
      inicio: document.getElementById("tab-inicio"),
      clientes: document.getElementById("tab-clientes"),
      productos: document.getElementById("tab-productos"),
      token: document.getElementById("tab-token"),
    };
  }

  init() {
    this.$tabs.forEach(tab => {
      tab.addEventListener("click", () => {
        const name = tab.dataset.tab;
        console.info(`[INFO] Tab seleccionado: ${name}`);
        // activar tab
        this.$tabs.forEach(t => t.classList.remove("active"));
        tab.classList.add("active");
        // mostrar contenido
        Object.values(this.$contents).forEach(c => c?.classList.remove("show", "active"));
        this.$contents[name]?.classList.add("show", "active");
        // callback
        this.onTabChange?.(name);
      });
    });
  }
}
