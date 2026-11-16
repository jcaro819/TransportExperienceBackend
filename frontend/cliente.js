// Pantallas del cliente: compra con carrito (HU-04). Se carga después de app.js y de
// paneles.js y reutiliza su cliente: api(), escapeHtml(), formatCOP(), humanDateTime(),
// showToast(), handleExpiredSession(), state, y de paneles.js fetchAllPages(), postJson(),
// downloadFile(), openPanelDialog(), handleDialogError(), runWithButton() y showPanelError().

const CART_KEY = "transport_cart";
const MAX_VEHICLES_PER_MODEL = 10; // límites de POST /ventas
const MAX_UNITS_PER_PRODUCT = 100;

const shop = {
  products: [],
  sales: [],
  cart: readCart(),
};

function injectClientStyles() {
  if (document.getElementById("tx-client-styles")) return;

  const style = document.createElement("style");
  style.id = "tx-client-styles";
  style.textContent = `
    .tx-cart-button{white-space:nowrap;gap:6px}
    .nav a{white-space:nowrap}
    @media(max-width:1500px){.nav{gap:20px}.header-actions .btn-primary{display:none}}
    .tx-cart-button[hidden]{display:none}
    .tx-cart-count{display:inline-grid;place-items:center;min-width:20px;height:20px;padding:0 6px;border-radius:999px;background:#fff;color:var(--brand-dark);font-size:10px;font-weight:800}
    .tx-product-desc{color:var(--muted);font-size:12px;line-height:1.5;margin:10px 0 0}
    .tx-product-icon{font-size:76px}
    .tx-buy-block{display:grid;gap:10px;margin-top:18px;padding-top:18px;border-top:1px solid var(--line)}
    .tx-buy-block small{color:var(--muted);font-size:11px;line-height:1.5}
    .tx-qty{display:inline-flex;align-items:center;gap:8px}
    .tx-qty button{width:30px;height:30px;border:1px solid var(--line);background:#fff;border-radius:9px;font-weight:800;color:var(--ink)}
    .tx-qty strong{min-width:22px;text-align:center}
    .tx-cart-summary{display:flex;justify-content:space-between;align-items:center;gap:18px;flex-wrap:wrap;margin-top:16px;background:#fff;border:1px solid var(--line);border-radius:18px;padding:20px}
    .tx-cart-summary small{display:block;color:var(--muted);font-size:12px;margin-top:4px}
    .tx-cart-summary strong{font-size:26px}
    .tx-account-block{padding-top:10px}
    .tx-receipt-table{margin:14px 0 6px}
    .tx-receipt-table th,.tx-receipt-table td{padding:8px 6px}
    .tx-receipt-table td:last-child,.tx-receipt-table th:last-child{text-align:right;white-space:nowrap}
    .tx-receipt-table small{display:block;color:var(--muted);font-size:10px}
    .tx-totals{display:grid;gap:5px;font-size:13px;margin:10px 0}
    .tx-totals div{display:flex;justify-content:space-between;gap:12px}
    .tx-totals .tx-total-line{font-size:16px;font-weight:800;border-top:1px solid var(--line);padding-top:8px}
    .tx-receipt-note{font-size:11px;color:var(--muted);line-height:1.5}
    @media(max-width:760px){
      .tx-cart-text{display:none}
      .tx-cart-summary{display:grid}
    }
  `;
  document.head.appendChild(style);
}

injectClientStyles();

// ---------------------------------------------------------
// Utilidades
// ---------------------------------------------------------

// Mensaje y acción del backend, por separado y ya escapados (estructura uniforme de errores).
function clientErrorHtml(error) {
  const detail = error?.payload?.error;
  if (detail?.mensaje) {
    return `<strong>${escapeHtml(detail.mensaje)}</strong>${detail.accion ? ` ${escapeHtml(detail.accion)}` : ""}`;
  }
  return escapeHtml(panelErrorMessage(error));
}

function showClientError(element, error) {
  if (!element) return;
  element.innerHTML = clientErrorHtml(error);
  element.hidden = false;
}

function isClient() {
  return state.user?.rol === "cliente";
}

function plural(count, one, many) {
  return `${count} ${count === 1 ? one : many}`;
}

// ---------------------------------------------------------
// Carrito (se guarda en el navegador hasta que se convierte en una compra)
// ---------------------------------------------------------

// Lo guardado puede venir de otra versión o estar dañado: solo se aceptan líneas bien formadas.
function readCart() {
  const empty = { vehiculos: [], productos: [] };
  try {
    const saved = JSON.parse(localStorage.getItem(CART_KEY) || "null");
    if (!saved) return empty;
    const clean = (lines, max) => (Array.isArray(lines) ? lines : [])
      .map(line => ({
        id: Number(line.id),
        nombre: String(line.nombre ?? ""),
        codigo: String(line.codigo ?? ""),
        precio: Math.trunc(Number(line.precio)),
        cantidad: Math.min(max, Math.max(1, Math.trunc(Number(line.cantidad)))),
        stock: line.stock == null ? null : Math.trunc(Number(line.stock)),
      }))
      .filter(line => Number.isInteger(line.id) && line.id > 0 && Number.isFinite(line.precio) && Number.isFinite(line.cantidad));
    return {
      vehiculos: clean(saved.vehiculos, MAX_VEHICLES_PER_MODEL),
      productos: clean(saved.productos, MAX_UNITS_PER_PRODUCT),
    };
  } catch {
    return empty;
  }
}

function saveCart() {
  try {
    localStorage.setItem(CART_KEY, JSON.stringify(shop.cart));
  } catch (error) {
    console.warn("No se pudo guardar el carrito.", error);
  }
  syncCartBadge();
}

function cartLines() {
  return [
    ...shop.cart.vehiculos.map(line => ({ ...line, kind: "vehiculos" })),
    ...shop.cart.productos.map(line => ({ ...line, kind: "productos" })),
  ];
}

function cartCount() {
  return cartLines().reduce((sum, line) => sum + line.cantidad, 0);
}

function cartTotal() {
  return cartLines().reduce((sum, line) => sum + line.precio * line.cantidad, 0);
}

function cartLimit(kind, line) {
  if (kind === "vehiculos") return MAX_VEHICLES_PER_MODEL;
  return Math.min(MAX_UNITS_PER_PRODUCT, line.stock ?? MAX_UNITS_PER_PRODUCT);
}

function syncCartBadge() {
  const button = document.getElementById("txCartButton");
  const badge = document.getElementById("txCartCount");
  if (!button || !badge) return;
  badge.textContent = String(cartCount());
  // El carrito es del cliente (o de quien aún no inicia sesión); el personal no compra.
  button.hidden = Boolean(state.user) && !isClient();
}

// app.js lo llama en cada cambio de sesión.
function syncClientUi() {
  syncCartBadge();
  if (!isClient()) {
    shop.sales = [];
    const list = document.getElementById("txSalesList");
    if (list) list.innerHTML = "";
  }
}

function addToCart(kind, item) {
  const lines = shop.cart[kind];
  const existing = lines.find(line => line.id === item.id);
  const limit = cartLimit(kind, existing || item);

  if ((existing?.cantidad || 0) >= limit) {
    showToast(kind === "productos"
      ? `Solo hay ${limit} en existencias de ${item.nombre}.`
      : `Máximo ${limit} unidades de un mismo modelo por compra.`);
    return false;
  }

  if (existing) {
    existing.cantidad += 1;
    existing.precio = item.precio;
    existing.stock = item.stock ?? null;
  } else {
    lines.push({ ...item, cantidad: 1 });
  }
  saveCart();
  showToast(`${item.nombre} se agregó al carrito.`);
  return true;
}

function changeCartQuantity(kind, id, delta) {
  const lines = shop.cart[kind];
  const line = lines.find(l => l.id === id);
  if (!line) return;

  const next = line.cantidad + delta;
  if (next < 1) {
    shop.cart[kind] = lines.filter(l => l.id !== id);
  } else if (next > cartLimit(kind, line)) {
    showToast(kind === "productos"
      ? `Solo hay ${cartLimit(kind, line)} en existencias de ${line.nombre}.`
      : `Máximo ${MAX_VEHICLES_PER_MODEL} unidades de un mismo modelo por compra.`);
    return;
  } else {
    line.cantidad = next;
  }
  saveCart();
  renderCart();
}

function removeFromCart(kind, id) {
  shop.cart[kind] = shop.cart[kind].filter(l => l.id !== id);
  saveCart();
  renderCart();
}

function cartLineHtml(line) {
  const isVehicle = line.kind === "vehiculos";
  return `
    <article class="tx-rental-card" data-cart-line="${line.kind}-${Number(line.id)}">
      <div class="tx-rental-main">
        <div class="tx-rental-icon">${isVehicle ? iconForType(line.nombre) : "🎒"}</div>
        <div>
          <small>${isVehicle ? "Vehículo en venta" : `Accesorio o repuesto · ${escapeHtml(line.codigo)}`}</small>
          <h3>${escapeHtml(line.nombre)}</h3>
          <span class="tx-qty">
            <button type="button" data-cart-kind="${line.kind}" data-cart-id="${Number(line.id)}" data-cart-delta="-1" aria-label="Quitar una unidad">−</button>
            <strong>${Number(line.cantidad)}</strong>
            <button type="button" data-cart-kind="${line.kind}" data-cart-id="${Number(line.id)}" data-cart-delta="1" aria-label="Agregar una unidad">+</button>
          </span>
        </div>
      </div>
      <div class="tx-rental-dates">
        <strong>${formatCOP(line.precio * line.cantidad)}</strong>
        <span>${Number(line.cantidad)} × ${formatCOP(line.precio)}</span>
      </div>
      <div class="tx-rental-actions">
        <button class="outline-danger" data-cart-kind="${line.kind}" data-cart-remove="${Number(line.id)}">Quitar</button>
      </div>
    </article>
  `;
}

// app.js lo llama al abrir la vista "carrito".
function renderCart() {
  const list = document.getElementById("txCartList");
  const summary = document.getElementById("txCartSummary");
  if (!list || !summary) return;

  const lines = cartLines();
  if (!lines.length) {
    summary.hidden = true;
    list.innerHTML = `
      <div class="empty-state">
        <div>🛒</div>
        <h3>Tu carrito está vacío</h3>
        <p>Agrega vehículos en venta desde el catálogo o accesorios y repuestos.</p>
        <button class="btn btn-primary" data-cart-go="accesorios">Ver accesorios</button>
      </div>`;
    list.querySelector("[data-cart-go]").addEventListener("click", () => showView("accesorios"));
    return;
  }

  list.innerHTML = lines.map(cartLineHtml).join("");
  list.querySelectorAll("[data-cart-delta]").forEach(btn => {
    btn.addEventListener("click", () => changeCartQuantity(btn.dataset.cartKind, Number(btn.dataset.cartId), Number(btn.dataset.cartDelta)));
  });
  list.querySelectorAll("[data-cart-remove]").forEach(btn => {
    btn.addEventListener("click", () => removeFromCart(btn.dataset.cartKind, Number(btn.dataset.cartRemove)));
  });

  summary.hidden = false;
  summary.innerHTML = `
    <div>
      <span>${plural(cartCount(), "artículo", "artículos")}</span><br>
      <strong>${formatCOP(cartTotal())}</strong>
      <small>El precio y las existencias se confirman al comprar. El domicilio, si lo quieres, se agrega antes de pagar.</small>
    </div>
    <div class="tx-row-actions">
      <button class="btn btn-ghost" id="txCartClear">Vaciar</button>
      <button class="btn btn-primary" id="txCheckout">Comprar por ${formatCOP(cartTotal())}</button>
    </div>
  `;
  document.getElementById("txCartClear").addEventListener("click", () => {
    shop.cart = { vehiculos: [], productos: [] };
    saveCart();
    renderCart();
  });
  document.getElementById("txCheckout").addEventListener("click", e => checkout(e.currentTarget));
}

// POST /ventas: una sola compra con vehículos (por modelo) y productos (por cantidad).
async function checkout(button) {
  const errorBox = document.getElementById("txCartError");
  hidePanelError(errorBox);

  if (!state.user) {
    showView("login");
    showToast("Inicia sesión como cliente para comprar. Tu carrito queda guardado.");
    return;
  }
  if (!isClient()) {
    showToast("Las compras se hacen con una cuenta de cliente.");
    return;
  }

  await runWithButton(button, "Creando compra...", async () => {
    try {
      const sale = await postJson("/ventas", {
        vehiculos: shop.cart.vehiculos.map(l => ({ modelo_id: l.id, cantidad: l.cantidad })),
        productos: shop.cart.productos.map(l => ({ producto_id: l.id, cantidad: l.cantidad })),
      });

      shop.cart = { vehiculos: [], productos: [] };
      saveCart();
      showToast(`Compra #${sale.id} creada. Tienes 15 minutos para pagar.`);
      showView("cuenta");
      await loadAccountExtras();
      focusSale(sale.id);
      refreshCatalog();
    } catch (error) {
      if (error.status === 401) handleExpiredSession();
      else showClientError(errorBox, error);
    }
  });
}

// ---------------------------------------------------------
// Accesorios y repuestos: GET /catalogo/productos
// ---------------------------------------------------------

function productCategoryLabel(category) {
  return ({ accesorio: "Accesorio", repuesto: "Repuesto" })[category] || category;
}

function productCard(product) {
  const stock = Number(product.stock || 0);
  return `
    <article class="catalog-card">
      <div class="catalog-card-media">
        <span class="availability ${stock > 0 ? "ok" : "no"}">${stock > 0 ? `● ${stock} en existencias` : "● Agotado"}</span>
        ${product.imagen_url
          ? `<img src="${escapeHtml(product.imagen_url)}" alt="${escapeHtml(product.nombre)}" style="max-width:82%;max-height:150px;object-fit:contain">`
          : `<span class="tx-product-icon">${product.categoria === "repuesto" ? "🧰" : "🎒"}</span>`}
      </div>
      <div class="catalog-card-body">
        <small>${escapeHtml(productCategoryLabel(product.categoria))}</small>
        <h3>${escapeHtml(product.nombre)}</h3>
        <div class="catalog-card-meta"><span>${escapeHtml(product.codigo)}</span></div>
        ${product.descripcion ? `<p class="tx-product-desc">${escapeHtml(product.descripcion)}</p>` : ""}
        <div class="catalog-card-footer">
          <div><div class="price">${formatCOP(product.precio_venta)}</div></div>
          <button data-add-product="${Number(product.id)}" ${stock > 0 ? "" : "disabled"}>${stock > 0 ? "Agregar" : "Agotado"}</button>
        </div>
      </div>
    </article>
  `;
}

// app.js lo llama al abrir la vista "accesorios".
async function loadShop() {
  const grid = document.getElementById("txShopGrid");
  const errorBox = document.getElementById("txShopError");
  if (!grid) return;

  const params = new URLSearchParams();
  const category = document.getElementById("txShopCategory").value;
  if (category) params.set("categoria", category);
  if (document.getElementById("txShopAvailable").checked) params.set("solo_disponibles", "true");

  if (!grid.children.length) {
    grid.innerHTML = `<div class="empty-state"><div>⏳</div><h3>Cargando productos</h3></div>`;
  }

  try {
    shop.products = await fetchPublicPages("/catalogo/productos", params);
    hidePanelError(errorBox);
  } catch (error) {
    grid.innerHTML = "";
    document.getElementById("txShopCount").textContent = "0";
    showClientError(errorBox, error);
    return;
  }

  document.getElementById("txShopCount").textContent = String(shop.products.length);
  if (!shop.products.length) {
    grid.innerHTML = `<div class="empty-state"><div>🔎</div><h3>No hay productos con esos filtros</h3><p>Prueba con otra categoría.</p></div>`;
    return;
  }

  grid.innerHTML = shop.products.map(productCard).join("");
  grid.querySelectorAll("[data-add-product]").forEach(btn => {
    btn.addEventListener("click", () => {
      const product = shop.products.find(p => p.id === Number(btn.dataset.addProduct));
      if (!product) return;
      addToCart("productos", {
        id: product.id,
        nombre: product.nombre,
        codigo: product.codigo,
        precio: product.precio_venta,
        stock: product.stock,
      });
    });
  });
}

// Igual que fetchAllPages() de paneles.js, pero sin sesión: el listado es público.
async function fetchPublicPages(path, params = new URLSearchParams(), maxPages = 20) {
  const items = [];
  let page = 1;
  let pages = 1;

  do {
    const query = new URLSearchParams(params);
    query.set("tamano", "100");
    query.set("pagina", String(page));
    const data = await api(`${path}?${query}`);
    items.push(...(data.elementos || []));
    pages = data.paginas || 1;
    page += 1;
  } while (page <= pages && page <= maxPages);

  return items;
}

["txShopCategory", "txShopAvailable"].forEach(id => {
  document.getElementById(id)?.addEventListener("input", loadShop);
});

// app.js lo llama al abrir la ficha de un modelo: si se vende, se puede llevar al carrito.
function decorateVehicleDialog(model, raw) {
  if (!raw?.se_vende || !raw.precio_venta) return;
  const body = document.querySelector("#dialogContent .dialog-body");
  if (!body) return;

  body.insertAdjacentHTML("beforeend", `
    <div class="tx-buy-block">
      <strong>Comprar este modelo</strong>
      <small>Precio de venta: ${formatCOP(raw.precio_venta)}. Al comprar, el sistema te asigna una unidad disponible.</small>
      <button class="btn btn-soft" id="txAddVehicle">Agregar al carrito · ${formatCOP(raw.precio_venta)}</button>
    </div>
  `);
  document.getElementById("txAddVehicle").addEventListener("click", () => {
    const added = addToCart("vehiculos", { id: raw.id, nombre: raw.nombre, codigo: "", precio: raw.precio_venta, stock: null });
    // El toast queda detrás del modal: se cierra la ficha para que se vea.
    if (added) dialog.close();
  });
}

// ---------------------------------------------------------
// Mis compras: GET /ventas/mias, pago, cancelación y comprobante preliminar
// ---------------------------------------------------------

function saleStatusLabel(status = "") {
  return ({
    pendiente_pago: "Pendiente de pago",
    pagada: "Pagada",
    cancelada: "Cancelada",
    expirada: "Expirada",
  })[status] || status.replaceAll("_", " ");
}

function saleStatusClass(status = "") {
  if (status === "pagada") return "tx-status-ok";
  if (["cancelada", "expirada"].includes(status)) return "tx-status-off";
  return "tx-status-pending";
}

function saleItemsSummary(sale) {
  return (sale.items || [])
    .map(item => `${item.descripcion}${item.cantidad > 1 ? ` ×${item.cantidad}` : ""}`)
    .join(", ");
}

function saleCard(sale) {
  const pending = sale.estado === "pendiente_pago";
  const units = (sale.items || []).reduce((sum, item) => sum + item.cantidad, 0);

  return `
    <article class="tx-rental-card" data-sale-id="${Number(sale.id)}" data-sale-status="${escapeHtml(sale.estado)}">
      <div class="tx-rental-main">
        <div class="tx-rental-icon">🛍️</div>
        <div>
          <small>Compra #${Number(sale.id)} · ${escapeHtml(humanDateTime(sale.creado_en))}</small>
          <h3>${escapeHtml(saleItemsSummary(sale) || "Compra")}</h3>
          <span class="tx-status ${saleStatusClass(sale.estado)}">${escapeHtml(saleStatusLabel(sale.estado))}</span>
        </div>
      </div>
      <div class="tx-rental-dates">
        <strong>${formatCOP(sale.total)}</strong>
        <span>${plural(units, "artículo", "artículos")}${sale.valor_envio ? ` · incluye envío de ${formatCOP(sale.valor_envio)}` : ""}</span>
        ${sale.expira_en && pending ? `<small>Apartado hasta ${escapeHtml(humanDateTime(sale.expira_en))}</small>` : ""}
        ${sale.motivo_cancelacion ? `<small>Motivo: ${escapeHtml(sale.motivo_cancelacion)}</small>` : ""}
      </div>
      <div class="tx-rental-actions">
        ${pending ? `<button class="btn btn-primary small-btn" data-pay-sale="${Number(sale.id)}">Pagar</button>` : ""}
        <button class="btn btn-ghost small-btn" data-receipt-sale="${Number(sale.id)}">Comprobante</button>
        ${pending ? `<button class="outline-danger" data-cancel-sale="${Number(sale.id)}">Cancelar</button>` : ""}
      </div>
    </article>
  `;
}

function ensureAccountSections() {
  const account = document.getElementById("view-cuenta");
  if (!account || document.getElementById("txSalesList")) return;

  account.insertAdjacentHTML("beforeend", `
    <section class="section tx-rentals-section tx-account-block" id="txSalesSection">
      <div class="section-heading"><div><span class="eyebrow">COMPRAS · HU-04</span><h2>Tus compras</h2></div><p>Paga lo que tienes apartado y consulta el comprobante de cada compra.</p></div>
      <div id="txSalesError" class="tx-availability no tx-panel-error" hidden></div>
      <div id="txSalesList" class="tx-rentals-list"></div>
    </section>
  `);
  document.getElementById("txRefreshRentals")?.addEventListener("click", loadAccountExtras);
}

function renderSales() {
  const list = document.getElementById("txSalesList");
  if (!list) return;

  if (!shop.sales.length) {
    list.innerHTML = `
      <div class="empty-state">
        <div>🛍️</div>
        <h3>Aún no tienes compras</h3>
        <p>Los vehículos en venta están en el catálogo; los accesorios y repuestos, en su propia sección.</p>
        <button class="btn btn-primary" data-sales-go>Ver accesorios</button>
      </div>`;
    list.querySelector("[data-sales-go]").addEventListener("click", () => showView("accesorios"));
    return;
  }

  list.innerHTML = shop.sales.map(saleCard).join("");
  list.querySelectorAll("[data-pay-sale]").forEach(btn => {
    btn.addEventListener("click", () => paySale(Number(btn.dataset.paySale)));
  });
  list.querySelectorAll("[data-cancel-sale]").forEach(btn => {
    btn.addEventListener("click", () => cancelSale(Number(btn.dataset.cancelSale)));
  });
  list.querySelectorAll("[data-receipt-sale]").forEach(btn => {
    btn.addEventListener("click", () => openReceipt(Number(btn.dataset.receiptSale), btn));
  });
}

// app.js lo llama al abrir "Mi cuenta", junto con loadMyRentals().
async function loadAccountExtras() {
  ensureAccountSections();
  const list = document.getElementById("txSalesList");
  const errorBox = document.getElementById("txSalesError");
  if (!list) return;

  if (!isClient()) {
    list.innerHTML = "";
    return;
  }

  if (list.dataset.owner !== String(state.user.id)) {
    list.dataset.owner = String(state.user.id);
    list.innerHTML = `<div class="empty-state"><div>⏳</div><h3>Cargando tus compras</h3></div>`;
  }

  try {
    const sales = await fetchAllPages("/ventas/mias");
    shop.sales = sales.sort((a, b) => {
      const aPending = a.estado === "pendiente_pago" ? 0 : 1;
      const bPending = b.estado === "pendiente_pago" ? 0 : 1;
      if (aPending !== bPending) return aPending - bPending;
      return new Date(b.creado_en) - new Date(a.creado_en);
    });
    hidePanelError(errorBox);
    renderSales();
  } catch (error) {
    if (error.status === 401) handleExpiredSession();
    else showClientError(errorBox, error);
  }
}

function focusSale(id) {
  const card = document.querySelector(`[data-sale-id="${Number(id)}"]`);
  if (!card) return;
  card.classList.add("tx-pending-focus");
  card.scrollIntoView({ behavior: "smooth", block: "center" });
  setTimeout(() => card.classList.remove("tx-pending-focus"), 1800);
}

// Igual que payRental() de app.js: con la pasarela falsa el cobro se resuelve al instante.
async function paySale(id) {
  const sale = shop.sales.find(s => s.id === id);
  if (!sale) return;

  const confirmed = window.confirm(`Vas a pagar ${formatCOP(sale.total)} por la compra #${id}. ¿Continuar?`);
  if (!confirmed) return;

  try {
    const config = await api("/pagos/configuracion");
    if (!config.metodos?.length) {
      showToast("No hay métodos de pago habilitados.");
      return;
    }

    if (config.proveedor !== "falso") {
      showToast("La UI de tokenización Wompi todavía no está implementada. Para pruebas locales usa PAGOS_PROVEEDOR=falso.");
      return;
    }

    const result = await postJson(`/ventas/${id}/pago`, { metodo_pago: config.metodos[0] });
    const status = result.pago?.estado || "desconocido";

    if (result.devolucion) {
      showToast(`El pago se aprobó, pero la compra #${id} no se pudo completar. Registramos la devolución de ${formatCOP(result.devolucion.monto)}.`);
    } else if (status === "aprobado") {
      showToast(`Pago aprobado. La compra #${id} quedó pagada.`);
    } else {
      showToast(`Pago registrado con estado: ${status}.`);
    }

    await loadAccountExtras();
    refreshCatalog();
    if (status === "aprobado" && !result.devolucion) openReceipt(id);
  } catch (error) {
    if (error.status === 401) handleExpiredSession();
    else showToast(error.message);
    await loadAccountExtras();
  }
}

async function cancelSale(id) {
  const reason = window.prompt("Motivo de cancelación (opcional):", "Cambio de planes");
  if (reason === null) return;

  try {
    await postJson(`/ventas/${id}/cancelacion`, { motivo: reason.trim() || null });
    showToast(`Compra #${id} cancelada. Lo apartado quedó libre.`);
    await loadAccountExtras();
    refreshCatalog();
  } catch (error) {
    if (error.status === 401) handleExpiredSession();
    else showToast(error.message);
  }
}

function paymentStatusLabel(status = "") {
  return ({
    pendiente: "Pendiente",
    aprobado: "Aprobado",
    rechazado: "Rechazado",
    expirado: "Expirado",
    error: "Con error",
  })[status] || status;
}

// GET /ventas/{id}/comprobante: comprobante preliminar (JSON). El PDF es el del pago aprobado.
async function openReceipt(id, button) {
  let receipt;
  try {
    const load = () => api(`/ventas/${id}/comprobante`, { auth: true });
    receipt = button ? await runWithButton(button, "Abriendo...", load) : await load();
  } catch (error) {
    if (error.status === 401) handleExpiredSession();
    else showToast(error.message);
    return;
  }

  const payment = receipt.pago;
  const rows = (receipt.items || []).map(item => `
    <tr>
      <td>${escapeHtml(item.descripcion)}<small>${escapeHtml(item.codigo)}</small></td>
      <td>${Number(item.cantidad)} × ${formatCOP(item.precio_unitario)}</td>
      <td>${formatCOP(item.subtotal)}</td>
    </tr>
  `).join("");

  const content = openPanelDialog(`
    <span class="eyebrow">${receipt.es_preliminar ? "COMPROBANTE PRELIMINAR" : "COMPROBANTE"}</span>
    <h2 id="txReceiptNumber">${escapeHtml(receipt.numero)}</h2>
    <p class="tx-receipt-note">${escapeHtml(receipt.leyenda)}</p>
    <div class="dialog-specs">
      <div><small>ESTADO</small><strong>${escapeHtml(saleStatusLabel(receipt.estado))}</strong></div>
      <div><small>FECHA</small><strong>${escapeHtml(humanDateTime(receipt.fecha_compra))}</strong></div>
      <div><small>TOTAL</small><strong>${formatCOP(receipt.total)}</strong></div>
    </div>
    <p class="tx-receipt-note">Cliente: ${escapeHtml(receipt.cliente?.nombre_completo)} · ${escapeHtml(receipt.cliente?.correo)}</p>
    <div class="tx-dialog-scroll">
      <table class="tx-receipt-table">
        <thead><tr><th>Artículo</th><th>Cantidad</th><th>Subtotal</th></tr></thead>
        <tbody>${rows}</tbody>
      </table>
    </div>
    <div class="tx-totals">
      <div><span>Subtotal</span><span>${formatCOP(receipt.subtotal)}</span></div>
      <div><span>Envío</span><span>${receipt.valor_envio ? formatCOP(receipt.valor_envio) : "Sin domicilio"}</span></div>
      <div class="tx-total-line"><span>Total</span><span>${formatCOP(receipt.total)}</span></div>
    </div>
    <p class="tx-receipt-note" id="txReceiptPayment">${payment
      ? `Pago ${escapeHtml(payment.referencia)} · ${escapeHtml(payment.metodo)} · ${escapeHtml(paymentStatusLabel(payment.estado))}${payment.aprobado_en ? ` el ${escapeHtml(humanDateTime(payment.aprobado_en))}` : ""}`
      : "Aún no hay un pago registrado para esta compra."}</p>
    <div class="tx-form-actions">
      ${payment?.estado === "aprobado" ? `<button type="button" class="btn btn-ghost" data-receipt-pdf>Descargar PDF del pago</button>` : ""}
      <button type="button" class="btn btn-primary" data-dialog-cancel>Cerrar</button>
    </div>
  `);

  content.querySelector("[data-receipt-pdf]")?.addEventListener("click", async e => {
    await runWithButton(e.currentTarget, "Descargando...", async () => {
      try {
        await downloadFile(`/pagos/${encodeURIComponent(payment.referencia)}/comprobante`, `comprobante-${payment.referencia}.pdf`);
      } catch (error) {
        handleDialogError(content, error);
      }
    });
  });
}

// Si este archivo carga después del arranque de app.js, la interfaz se pone al día.
ensureAccountSections();
syncClientUi();
if (document.getElementById("view-cuenta")?.classList.contains("active")) loadAccountExtras();
if (document.getElementById("view-accesorios")?.classList.contains("active")) loadShop();
if (document.getElementById("view-carrito")?.classList.contains("active")) renderCart();
