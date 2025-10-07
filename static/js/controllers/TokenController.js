export class TokenController {
  constructor({ view }) {
    this.view = view;
  }

  async cargarToken() {
    try {
      this.view.showLoading();
      const res = await fetch("/api/xubio/token/test");
      const data = await res.json();
      if (!data.ok) throw new Error("No se pudo obtener el token.");
      this.view.showToken(data);
    } catch (err) {
      this.view.showError(err);
    }
  }
}