1. Actualizar el sistema

```bash
sudo apt update
sudo apt upgrade -y
```

✅ 2. Instalar MySQL Server

Linux Mint 22.2 usa repositorios compatibles con MySQL 8.x.

Ejecuta:

```bash
sudo apt install mysql-server -y
```

Esto instala:

- mysqld (servidor)
- mysql (cliente)
- scripts de inicialización

✅ 3. Verificar que MySQL está corriendo

```bash
sudo systemctl status mysql
```

Debes ver:

Código

```text
active (running)
```

Si no está activo:

```bash
sudo systemctl start mysql
```

4. Asegurar la instalación

MySQL incluye un script para endurecer la seguridad:

```bash
sudo mysql_secure_installation
```

Responde así (recomendado):

| Pregunta | Respuesta |
| --- | --- |
| VALIDATE PASSWORD PLUGIN | n |
| New password for root | (elige una contraseña segura) |
| Remove anonymous users? | y |
| Disallow root login remotely? | y |
| Remove test database? | y |
| Reload privilege tables? | y |

5. Entrar a MySQL como root

```bash
sudo mysql
```

Si quieres usar contraseña en vez de autenticación por socket:

```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'TuPasswordSegura';
FLUSH PRIVILEGES;
```

Salir:

```sql
exit;
```

6. Crear la base de datos del proyecto

```bash
sudo mysql -u root -p
```

Dentro del prompt:

```sql
CREATE DATABASE gimnasio;
```

7. Crear usuarios para el proyecto (requisito del bootcamp)

Usuario de la aplicación:

```sql
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'segura123';
GRANT SELECT, INSERT, UPDATE ON gimnasio.* TO 'app_user'@'localhost';
```

Usuario administrador:

```sql
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'adminpass';
GRANT ALL PRIVILEGES ON gimnasio.* TO 'admin'@'localhost';
```

Aplicar cambios:

```sql
FLUSH PRIVILEGES;
```

8. Probar conexión

Como root:

```bash
mysql -u root -p
```

Como app_user:

```bash
mysql -u app_user -p gimnasio
```

9. Exportar la base de datos (dump)

Requisito del bootcamp:

```bash
mysqldump -u root -p gimnasio > gimnasio_backup.sql
```

10. Comandos útiles

Reiniciar MySQL:

```bash
sudo systemctl restart mysql
```

Ver versión:

```bash
mysql --version
```
