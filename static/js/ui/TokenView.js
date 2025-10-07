export class TokenView {
  constructor({ containerId = "tab-token" } = {}) {
    this.$container = document.getElementById(containerId);
  }

  showLoading() {
    this.$container.innerHTML = `<div class="text-center my-3"><div class="spinner-border"></div> Obteniendo token...</div>`;
  }

  showToken(data) {
    this.$container.innerHTML = `
      <div class="card mt-3">
        <div class="card-header">Token de Xubio</div>
        <div class="card-body">
          <p><strong>Tipo:</strong> ${data.token_type}</p>
          <p><strong>Expira en:</strong> ${data.expires_in} segundos</p>
          <p><strong>Obtenido:</strong> ${data.obtained_at_utc}</p>
          <p><strong>Preview:</strong> <code>${data.access_token_preview}</code></p>
        </div>
      </div>
    `;
  }

  showError(err) {
    this.$container.innerHTML = `<div class="alert alert-danger">Error: ${err?.message ?? err}</div>`;
  }
}