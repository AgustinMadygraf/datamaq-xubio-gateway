// Path: static/js/use_cases/ListarClientes.js
export class ListarClientes {
  constructor({ repo }) { this.repo = repo; }
  async execute() { return this.repo.listar(); }
}
