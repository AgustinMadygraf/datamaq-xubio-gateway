// Path: static/js/infrastructure/HttpClienteGateway.js
import { ClienteGateway } from "../gateways/ClienteGateway.js";
import { Cliente } from "../entities/Cliente.js";

export class HttpClienteGateway extends ClienteGateway {
  constructor({ baseUrl }) {
    super();
    this.baseUrl = baseUrl.replace(/\/$/, "");
  }

  async listar() {
    const url = `${this.baseUrl}/clienteBean`;
    console.info(`[INFO] GET ${url}`);
    const res = await fetch(url);
    if (!res.ok) console.warn(`[WARN] HTTP ${res.status} al listar clientes`);
    const data = await res.json();
    if (!Array.isArray(data)) return [];
    return data.map(Cliente.fromApi);
  }

  async obtenerPorId(id) {
    const url = `${this.baseUrl}/clienteBean/${encodeURIComponent(id)}`;
    console.info(`[INFO] GET ${url}`);
    const res = await fetch(url);
    if (!res.ok) console.warn(`[WARN] HTTP ${res.status} al obtener cliente ${id}`);
    const json = await res.json();
    if (!json || typeof json !== "object") return null;
    return Cliente.fromApi(json);
  }
}
