# VIFER ERP – Generador de Precios desde Facturas CFDI

## Estructura del proyecto

```
erp_project/
├── server.py          ← Backend Flask (Python)
├── App.vue            ← Frontend Vue 3 + TypeScript
└── README.md
```

---

## 1. Backend Python (Flask)

### Instalar dependencias
```bash
pip install flask flask-cors pdfplumber openpyxl
```

### Correr el servidor
```bash
python server.py
# → http://localhost:5000
```

### Endpoint disponible
```
POST /generar-erp
  Body (multipart/form-data):
    pdf           → archivo PDF de la factura CFDI
    mult_publico  → multiplicador precio público  (default: 2.3)
    mult_mayoreo  → multiplicador precio mayoreo  (default: 1.35)

  Response:
    → archivo .xlsx para descargar directamente
```

---

## 2. Frontend Vue 3 + TypeScript

### Crear proyecto (si no lo tienes)
```bash
npm create vue@latest erp-front
# Selecciona: TypeScript ✓, sin Router, sin Pinia
cd erp-front
npm install
```

### Instalar fuentes (en index.html)
```html
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet"/>
```

### Usar el componente
Copia `App.vue` al `src/` de tu proyecto y corre:
```bash
npm run dev
```

---

## 3. Flujo completo

```
Usuario arrastra PDF
        ↓
App.vue (Vue 3 + TS)
  ├─ Lee mult_publico y mult_mayoreo del topbar
  ├─ Manda FormData al backend: POST /generar-erp
  │
  └─ server.py (Flask)
        ├─ parse_cfdi()  → extrae partidas del PDF dinámicamente
        ├─ build_excel() → genera .xlsx con 4 hojas:
        │     🗂️ Catálogo Productos  (con col. Precio Público y Precio Mayoreo)
        │     📄 Encabezado Factura
        │     📦 Detalle Partidas
        │     📊 Resumen ERP
        └─ Devuelve el .xlsx como descarga

Usuario descarga el Excel ⬇
```

---

## 4. Columnas en la hoja Catálogo

| Columna | Contenido | Editable |
|---------|-----------|----------|
| A | No. Identif. | No |
| B | Descripción | No |
| C | U.M. | No |
| D | Clave SAT | No |
| **E** | **Precio Costo (MXN)** | ✅ Amarillo |
| **F** | **Precio Público** = E × mult_publico | Fórmula verde |
| **G** | **Precio Mayoreo** = E × mult_mayoreo | Fórmula azul |
| H–M | Stock, Ubicación, Activo, Notas… | ✅ Amarillo |

Las columnas F y G usan fórmulas Excel (`=E2*2.3`), así que
si el usuario edita el costo en E, los precios se recalculan solos.

---

## 5. Cambiar los multiplicadores

En el topbar de la app Vue hay dos pills editables:

```
● Público  ×  [2.3]     ● Mayoreo  ×  [1.35]
```

El usuario escribe cualquier valor → sube el PDF → descarga el Excel
con los nuevos multiplicadores ya aplicados como fórmulas.
