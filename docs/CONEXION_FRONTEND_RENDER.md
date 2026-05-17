# Conexión del Frontend con el Backend de Render

Este documento explica cómo conectar el frontend del proyecto `MYSGYM_FRONT` con el backend desplegado en Render.

## URL base del backend

La API publicada en Render responde en:

```text
https://backend-mysgym.onrender.com
```

Todas las peticiones desde el frontend deben apuntar a esa URL.

## Variables de entorno recomendadas

### En el backend de Render

```dotenv
FRONTEND_ORIGIN=https://mysgym-front.onrender.com
```

Si defines esta variable, el backend limitará CORS a ese origen.
Si el frontend ya no se despliega por separado, puedes omitirla y el backend seguirá aceptando orígenes de Render y de desarrollo local.

### Si usas Vite

En el archivo `.env` del frontend añade:

```dotenv
VITE_API_URL=https://backend-mysgym.onrender.com
```

### Si usas Create React App

En el archivo `.env` del frontend añade:

```dotenv
REACT_APP_API_URL=https://backend-mysgym.onrender.com
```

## Ejemplo con `fetch`

```js
const API_URL = import.meta.env.VITE_API_URL;

async function login(email, password) {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  return response.json();
}
```

## Ejemplo con `axios`

```js
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

export default api;
```

## Llamadas autenticadas con JWT

Las rutas protegidas deben enviar el token en el header `Authorization`:

```js
api.get('/usuarios', {
  headers: {
    Authorization: `Bearer ${token}`,
  },
});
```

## Rutas disponibles

- `POST /auth/register`
- `POST /auth/login`
- `GET /gym/actividades`
- `GET /gym/salas`
- `GET /gym/horarios`
- `GET /usuarios` (requiere JWT)
- `GET /empleados` (requiere JWT)
- `GET /reservas` (requiere JWT)
- `GET /pagos` (requiere JWT)
- `GET /mantenimiento/materiales`
- `GET /mantenimiento/incidencias`

## Pasos para conectar el frontend

1. Clona el repositorio del frontend `MYSGYM_FRONT`.
2. Crea o modifica el archivo `.env` del frontend.
3. Define la URL base según el framework que uses.
4. Sustituye las llamadas directas por `API_URL` o una instancia de `axios`.
5. Guarda el token JWT tras iniciar sesión.
6. Incluye el token en los endpoints protegidos.
7. Prueba primero `GET /` para verificar que el backend responde.
8. Después prueba `POST /auth/login` y una ruta protegida como `GET /usuarios`.

## Verificación rápida

Si la conexión funciona, al abrir la URL raíz deberías recibir una respuesta similar a:

```json
{
  "status": "success",
  "message": "Bienvenido a la API de MYSGYM"
}
```

## Notas importantes

- No uses `localhost` como backend en producción si el frontend está desplegado.
- En Render, el frontend debe apuntar siempre a la URL pública del backend.
- En Render, el backend puede restringir CORS a la URL pública del frontend con `FRONTEND_ORIGIN`.
- Si todavía no conoces la URL final del frontend, la configuración por defecto ya acepta dominios `*.onrender.com`.
- Si una ruta devuelve `401`, normalmente falta el token JWT o está caducado.
- Si el navegador bloquea la petición, revisa CORS y la URL base configurada.
