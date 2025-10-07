/*
Path: static/main.js
*/

const tabs = document.querySelectorAll('.tab');
const contents = {
    clientes: document.getElementById('tab-clientes'),
    productos: document.getElementById('tab-productos'),
    token: document.getElementById('tab-token')
};

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        console.info(`[INFO] Tab seleccionado: ${tab.dataset.tab}`);
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        Object.values(contents).forEach(c => c.classList.remove('show', 'active'));
        contents[tab.dataset.tab].classList.add('show', 'active');

        // Si es el tab de clientes, carga la tabla
        if (tab.dataset.tab === 'clientes') {
            console.log('[LOG] Cargando clientes...');
            cargarClientes();
        }
    });
});

function cargarClientes() {
    const container = document.getElementById('clientes-table-container');
    container.innerHTML = '<div class="text-center my-3"><div class="spinner-border"></div> Cargando...</div>';
    console.info('[INFO] Realizando fetch a /api/xubio/clienteBean');
    fetch('/api/xubio/clienteBean')
        .then(response => {
            if (!response.ok) {
                console.warn(`[WARN] Respuesta HTTP no OK: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('[LOG] Datos recibidos:', data);
            if (!Array.isArray(data)) {
                console.warn('[WARN] La respuesta no es un array.');
                container.innerHTML = '<div class="alert alert-warning">No se encontraron clientes.</div>';
                return;
            }
            if (data.length === 0) {
                console.info('[INFO] No hay clientes para mostrar.');
                container.innerHTML = '<div class="alert alert-info">No hay clientes para mostrar.</div>';
                return;
            }
            // Construye la tabla con más campos relevantes
            let table = `<table class="table table-striped table-bordered table-sm">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nombre</th>
                        <th>Razón Social</th>
                        <th>Email</th>
                        <th>Teléfono</th>
                        <th>CUIT</th>
                        <th>Provincia</th>
                        <th>Dirección</th>
                        <th>Actualizado</th>
                    </tr>
                </thead>
                <tbody>`;
            data.forEach(cliente => {
                const id = cliente.cliente_id || cliente.id || '';
                table += `<tr>
                    <td class="cliente-id" style="cursor:pointer;" data-id="${id}">${id}</td>
                    <td>${cliente.nombre || cliente.primer_nombre || ''}</td>
                    <td>${cliente.razon_social || cliente.nombre_comercial || ''}</td>
                    <td>${cliente.email || ''}</td>
                    <td>${cliente.telefono || ''}</td>
                    <td>${cliente.cuit || cliente.CUIT || ''}</td>
                    <td>${(cliente.provincia && cliente.provincia.nombre) ? cliente.provincia.nombre : ''}</td>
                    <td>${cliente.direccion || ''}</td>
                    <td>${cliente.actualizado_en || ''}</td>
                </tr>`;
            });
            table += '</tbody></table>';
            container.innerHTML = table;
            console.info('[INFO] Tabla de clientes renderizada.');

            // Agrega el evento click a cada celda de ID
            document.querySelectorAll('.cliente-id').forEach(td => {
                td.addEventListener('click', function () {
                    const selectedId = this.getAttribute('data-id');
                    console.log(`[LOG] ID seleccionado: ${selectedId}`);
                    container.innerHTML = `<div class="alert alert-primary text-center">ID seleccionado: <strong>${selectedId}</strong></div>
                        <button class="btn btn-secondary mt-3" id="volver-clientes">Volver a la tabla</button>`;
                    document.getElementById('volver-clientes').addEventListener('click', cargarClientes);
                });
            });
        })
        .catch(err => {
            console.error('[ERROR] Error al cargar clientes:', err);
            container.innerHTML = `<div class="alert alert-danger">Error al cargar clientes: ${err}</div>`;
        });
}

// Carga inicial si el tab de clientes está activo
if (document.getElementById('clientes-tab').classList.contains('active')) {
    console.log('[LOG] Tab clientes activo al cargar la página.');
    cargarClientes();
}
