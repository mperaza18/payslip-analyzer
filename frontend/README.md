# Frontend — Payslip Analyzer

React 19 · TypeScript · Vite · Tailwind CSS v4 · Recharts

---

## Prerequisitos

| Herramienta | Versión mínima |
|-------------|---------------|
| Node.js     | 20 LTS+       |
| npm         | 10+           |

---

## Setup inicial

```bash
# Desde la raíz del monorepo, generar el proyecto con Vite
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install

# Dependencias adicionales
npm install recharts
npm install tailwindcss @tailwindcss/vite
```

---

## Configuración

El frontend espera que el backend corra en `http://localhost:8000`.  
Si cambias el puerto del backend, actualiza la URL base en `src/api/client.ts` (o donde configures axios).

Para desarrollo, Vite ya incluye HMR — no se necesita configuración extra.

---

## Correr en desarrollo

```bash
npm run dev
```

Abre `http://localhost:5173` en el navegador.

---

## Otros comandos

```bash
# Type-check sin emitir archivos
npm run tsc --noEmit

# Build para producción
npm run build

# Preview del build
npm run preview
```

---

## Estructura de `src/`

```
src/
├── main.tsx          # Entrypoint React
├── App.tsx           # Root component (smoke test de /health)
├── index.css         # @import "tailwindcss"
├── components/       # Componentes reutilizables (gráficas, tablas)
├── pages/            # Vistas principales
└── api/              # Clientes axios por recurso
```

---

## Stack de UI

| Librería   | Uso                                      |
|------------|------------------------------------------|
| Tailwind   | Utilidades CSS (v4, sin config extra)    |
| Recharts   | Gráficas de percepciones/deducciones     |
| fetch      | HTTP client nativo del browser           |
