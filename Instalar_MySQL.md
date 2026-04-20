# Instalar MySQL en Docker con SQLTools (sin Workbench)

Esta guia refleja los pasos reales aplicados en este repositorio.

## 1. Requisitos

- Linux Mint o Ubuntu
- Docker Engine
- Docker Compose plugin
- VS Code con extensiones:
	- SQLTools (`mtxr.sqltools`)
	- SQLTools MySQL Driver (`mtxr.sqltools-driver-mysql`)

Instalacion de Docker y Compose:

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin
sudo systemctl enable --now docker
```

Opcional (evitar sudo con Docker):

```bash
sudo usermod -aG docker $USER
newgrp docker
```

## 2. Crear archivos de configuracion del proyecto

Archivo `docker-compose.yml`:

```yaml
services:
	mysql:
		image: mysql:8.0
		container_name: mysql-gym
		restart: unless-stopped
		ports:
			- "3306:3306"
		environment:
			MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
			MYSQL_DATABASE: ${MYSQL_DATABASE}
		volumes:
			- mysql_data:/var/lib/mysql

volumes:
	mysql_data:
		external: true
		name: mysql_data
```

Archivo `.env`:

```env
MYSQL_ROOT_PASSWORD=RootPass123!
MYSQL_DATABASE=gimnasio
MYSQL_APP_USER=app_user
MYSQL_APP_PASSWORD=segura123
MYSQL_ADMIN_USER=admin
MYSQL_ADMIN_PASSWORD=adminpass
```

## 3. Levantar MySQL

```bash
docker compose up -d
docker compose ps
```

Validar que responde:

```bash
set -a
source .env
set +a
docker exec mysql-gym mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "SELECT 1 as ok;"
```

## 4. Inicializar usuarios y permisos

Entrar a MySQL como root:

```bash
docker exec -it mysql-gym mysql -u root -p
```

Ejecutar:

```sql
CREATE DATABASE IF NOT EXISTS gimnasio;

CREATE USER IF NOT EXISTS 'app_user'@'%' IDENTIFIED BY 'segura123';
GRANT SELECT, INSERT, UPDATE ON gimnasio.* TO 'app_user'@'%';

CREATE USER IF NOT EXISTS 'admin'@'%' IDENTIFIED BY 'adminpass';
GRANT ALL PRIVILEGES ON gimnasio.* TO 'admin'@'%';

FLUSH PRIVILEGES;
```

## 5. Configurar SQLTools en VS Code

El workspace usa `.vscode/settings.json` con dos conexiones:

- `MySQL Docker Local (app_user)` para desarrollo diario
- `MySQL Docker Local (root)` para tareas administrativas

La conexion por defecto para desarrollo se deja con:

```json
"sqltools.autoConnectTo": "MySQL Docker Local (app_user)"
```

Si no ves el panel:

1. Abrir paleta y ejecutar `View: Open View...`
2. Buscar `SQLTools`
3. Ejecutar `Developer: Reload Window`

## 6. Comandos diarios con Makefile

```bash
make help
make up
make down
make restart
make ps
make logs
make backup
```

## 7. Migracion desde docker run (si aplica)

Si inicialmente se creo con `docker run`, la migracion a Compose es:

```bash
docker stop mysql-gym
docker rm mysql-gym
docker compose up -d
```

No se pierden datos si se reutiliza el volumen `mysql_data`.

## 8. Backup y restauracion

Backup:

```bash
make backup
```

Restaurar (ejemplo):

```bash
set -a
source .env
set +a
cat backups/archivo.sql | docker exec -i mysql-gym mysql -u root -p"$MYSQL_ROOT_PASSWORD" "$MYSQL_DATABASE"
```

## 9. Solucion de problemas

- Puerto ocupado en 3306:

```bash
sudo lsof -i :3306
```

- Ver logs de MySQL:

```bash
docker compose logs -f mysql
```

- Verificar estado general:

```bash
docker compose ps
```
