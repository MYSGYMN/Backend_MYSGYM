# Instalar MySQL en Docker + MySQL Workbench (Linux Mint)

## 1. Actualizar el sistema

```bash
sudo apt update
sudo apt upgrade -y
```

## 2. Instalar Docker Engine y Docker Compose plugin

```bash
sudo apt install -y docker.io docker-compose-plugin
sudo systemctl enable --now docker
```

Opcional (para usar Docker sin sudo):

```bash
sudo usermod -aG docker $USER
newgrp docker
```

## 3. Evitar conflicto de puerto 3306 (si tienes MySQL local)

Si ya tenias MySQL instalado en el host, detenlo para liberar el puerto 3306:

```bash
sudo systemctl stop mysql
sudo systemctl disable mysql
```

## 4. Levantar MySQL en contenedor Docker

```bash
docker volume create mysql_data

docker run -d \
	--name mysql-gym \
	-e MYSQL_ROOT_PASSWORD=RootPass123! \
	-e MYSQL_DATABASE=gimnasio \
	-p 3306:3306 \
	-v mysql_data:/var/lib/mysql \
	--restart unless-stopped \
	mysql:8.0
```

Verifica que este corriendo:

```bash
docker ps
docker logs -n 50 mysql-gym
```

Debes ver mensajes similares a "ready for connections".

## 5. Entrar a MySQL dentro del contenedor

```bash
docker exec -it mysql-gym mysql -u root -p
```

Cuando pida password, usa la que definiste en MYSQL_ROOT_PASSWORD.

## 6. Crear usuarios para el proyecto

Dentro del prompt de MySQL:

```sql
CREATE DATABASE IF NOT EXISTS gimnasio;

CREATE USER IF NOT EXISTS 'app_user'@'%' IDENTIFIED BY 'segura123';
GRANT SELECT, INSERT, UPDATE ON gimnasio.* TO 'app_user'@'%';

CREATE USER IF NOT EXISTS 'admin'@'%' IDENTIFIED BY 'adminpass';
GRANT ALL PRIVILEGES ON gimnasio.* TO 'admin'@'%';

FLUSH PRIVILEGES;
```

## 7. Probar conexion desde host

Instala cliente MySQL en el host (si no lo tienes):

```bash
sudo apt install -y mysql-client
```

Prueba como root:

```bash
mysql -h 127.0.0.1 -P 3306 -u root -p
```

Prueba como app_user:

```bash
mysql -h 127.0.0.1 -P 3306 -u app_user -p gimnasio
```

## 8. Instalar MySQL Workbench

```bash
sudo apt install -y mysql-workbench
```

Abrir Workbench:

```bash
mysql-workbench
```

Configura una conexion nueva con estos datos:

- Connection Name: MySQL Docker Local
- Connection Method: Standard (TCP/IP)
- Hostname: 127.0.0.1
- Port: 3306
- Username: root (o app_user)
- Password: la que configuraste

## 9. Exportar base de datos (dump)

Desde el host, usando el puerto publicado por el contenedor:

```bash
mysqldump -h 127.0.0.1 -P 3306 -u root -p gimnasio > gimnasio_backup.sql
```

Alternativa ejecutando dentro del contenedor:

```bash
docker exec mysql-gym sh -c 'mysqldump -u root -p"$MYSQL_ROOT_PASSWORD" gimnasio' > gimnasio_backup.sql
```

## 10. Comandos utiles

Detener/Iniciar el contenedor:

```bash
docker stop mysql-gym
docker start mysql-gym
```

Reiniciar el contenedor:

```bash
docker restart mysql-gym
```

Ver version de MySQL del contenedor:

```bash
docker exec mysql-gym mysql --version
```

Ver estado del contenedor:

```bash
docker ps -a --filter name=mysql-gym
```
