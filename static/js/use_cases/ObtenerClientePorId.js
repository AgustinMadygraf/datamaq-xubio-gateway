// Path: static/js/use_cases/ObtenerClientePorId.js
export class ObtenerClientePorId {
  constructor({ repo }) { this.repo = repo; }
  async execute(id) { return this.repo.obtenerPorId(id); }
}
