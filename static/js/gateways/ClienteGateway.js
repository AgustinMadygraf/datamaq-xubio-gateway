// Path: static/js/gateways/ClienteGateway.js
/**
 * @interface
 * Define el contrato de acceso a datos de clientes.
 */
export class ClienteGateway {
  /** @returns {Promise<import('../entities/Cliente.js').Cliente[]>} */
  async listar() { throw new Error("Not implemented"); }
  /** @param {string} id @returns {Promise<import('../entities/Cliente.js').Cliente>} */
  async obtenerPorId(id) { throw new Error("Not implemented"); }
}
