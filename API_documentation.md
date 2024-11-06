
# Documentación de la API

---

## Autenticación

### Iniciar sesión y obtener un token de acceso

- **Método**: `POST`
- **Endpoint**: `/login`
- **Encabezado de la solicitud**: 
  - `Authorization: Basic <base64(username:password)>`
- **Descripción**: Este endpoint permite a los usuarios iniciar sesión con sus credenciales (nombre de usuario y contraseña) en el encabezado de autorización. Si la autenticación es exitosa, se devuelve un token de acceso.

#### Ejemplo de respuesta

```json
{
    "Token": "Bearer tu_token_de_acceso"
}
```
#### Ejemplo de respuesta en caso de fallo

```json
{
    "Mensaje": "El usuario y la contraseña al parecer no coinciden"
}
```
---

## Usuarios

### Obtener la lista de usuarios

- **Método**: `GET`
- **Endpoint**: `/users`
- **Encabezado de la solicitud**: 
  - `Authorization: Bearer <tu_token_de_acceso>`
- **Descripción**: Este endpoint permite obtener una lista de todos los usuarios. Solo un administrador puede ver detalles completos de cada usuario, mientras que otros roles reciben información limitada.

#### Ejemplo de respuesta para administradores

```json
[
    {
        "id": 1,
        "is_admin": true,
        "password_hash": "scrypt:xxxxxxxxxxxxxxxxxxxxx",
        "username": "nombre_usuario"
    },
    // Otros usuarios
]
```

#### Ejemplo de respuesta para otros usuarios

```json
[
    {
        "username": "nombre_usuario"
    },
    // Otros usuarios
]
```

### Crear un nuevo usuario

- **Método**: `POST`
- **Endpoint**: `/users`
- **Encabezado de la solicitud**: 
  - `Authorization: Bearer <tu_token_de_acceso>`
- **Cuerpo de la solicitud**

    ```json
    {
        "usuario": "nuevo_usuario",
        "contrasenia": "contraseña",
        "tipo": "admin" // Valores posibles: "admin", "visor", "editor"
    }
    ```

- **Descripción**: Este endpoint permite al administrador crear un nuevo usuario especificando el nombre de usuario, la contraseña y el tipo de usuario (admin, visor o editor). Solo los administradores pueden acceder a este endpoint.

#### Ejemplo de respuesta exitosa

```json
{
    "Mensaje": "Usuario creado correctamente"
}
```

#### Ejemplo de respuesta en caso de fallo

```json
{
    "Mensaje": "Fallo la creación del nuevo usuario"
}
```


## Endpoints de Marca

### Obtener todas las marcas

- **Método**: `GET`
- **Endpoint**: `/marca`
- **Encabezado de la solicitud**: 
  - `Authorization: Bearer <tu_token_de_acceso>`
- **Descripción**: Este endpoint permite obtener una lista de todas las marcas activas. Solo los usuarios con rol de administrador o visor pueden acceder a este endpoint.

#### Ejemplo de respuesta

```json
[
    {
        "id": 1,
        "nombre": "Marca Ejemplo"
    },
    // Otros objetos de marca
]
```

### Crear una nueva marca

- **Método**: `POST`
- **Endpoint**: `/marca`
- **Encabezado de la solicitud**: 
  - `Authorization: Bearer <tu_token_de_acceso>`
- **Cuerpo de la solicitud**

    ```json
    {
        "nombre": "Nueva Marca"
    }
    ```

- **Descripción**: Este endpoint permite a un administrador crear una nueva marca. Solo los administradores pueden acceder a este endpoint.

#### Ejemplo de respuesta exitosa

```json
{
    "id": 2,
    "nombre": "Nueva Marca"
}
```

#### Ejemplo de respuesta en caso de permisos insuficientes

```json
{
    "Mensaje": "Solo el admin puede crear nuevas marcas"
}
```

---

### Borrar una marca

- **Método**: `POST`
- **Endpoint**: `/marca/borrar`
- **Encabezado de la solicitud**: 
  - `Authorization: Bearer <tu_token_de_acceso>`
- **Cuerpo de la solicitud**

    ```json
    {
        "id": 1
    }
    ```

- **Descripción**: Este endpoint permite marcar una marca como inactiva. Solo los usuarios con rol de administrador o editor pueden acceder a este endpoint.

#### Ejemplo de respuesta exitosa

```json
{
    "Mensaje": "El borrado fue exitoso",
    "Marca": "Marca Ejemplo"
}
```

#### Ejemplo de respuesta en caso de permisos insuficientes

```json
{
    "Mensaje": "Usted no tiene permiso de borrar marca"
}
```

#### Ejemplo de respuesta si la marca ya está borrada

```json
{
    "Mensaje": "Esta marca fue borrada anteriormente",
    "Marca": "Marca Ejemplo"
}
```

---

### Editar una marca

- **Método**: `POST`
- **Endpoint**: `/marca/editar`
- **Encabezado de la solicitud**: 
  - `Authorization: Bearer <tu_token_de_acceso>`
- **Cuerpo de la solicitud**

    ```json
    {
        "id": 1,
        "nombre": "Nombre Editado"
    }
    ```

- **Descripción**: Este endpoint permite editar el nombre de una marca activa. Solo los usuarios con rol de administrador o editor pueden acceder a este endpoint.

#### Ejemplo de respuesta exitosa

```json
{
    "Mensaje": "La marca fue editada exitosamente",
    "Marca": "Nombre Editado"
}
```

#### Ejemplo de respuesta en caso de permisos insuficientes

```json
{
    "Mensaje": "Usted no tiene permiso de editar marca"
}
```

#### Ejemplo de respuesta si la marca ya está borrada

```json
{
    "Mensaje": "Esta marca fue borrada"
}
```


---

## Endpoints de Modelo

### Obtener todos los modelos

- **Método**: `GET`
- **Endpoint**: `/modelo`
- **Encabezado de la solicitud**: 
  - `Authorization: Bearer <tu_token_de_acceso>`
- **Descripción**: Este endpoint permite obtener una lista de todos los modelos activos. Solo los usuarios con rol de administrador o visor pueden acceder a este endpoint.

#### Ejemplo de respuesta

```json
[
    {
        "id": 1,
        "nombre": "Modelo Ejemplo",
        "id_marca": 2,
    },
    // Otros objetos de modelo
]
```

### Crear un nuevo modelo

- **Método**: `POST`
- **Endpoint**: `/modelo`
- **Encabezado de la solicitud**: 
  - `Authorization: Bearer <tu_token_de_acceso>`
- **Cuerpo de la solicitud**

    ```json
    {
        "nombre": "Nuevo Modelo",
        "id_marca": 1
    }
    ```

- **Descripción**: Este endpoint permite a un administrador crear un nuevo modelo asociado a una marca específica. Solo los administradores pueden acceder a este endpoint.

#### Ejemplo de respuesta exitosa

```json
{
    "id": 3,
    "nombre": "Nuevo Modelo",
    "id_marca": 1,
}
```

#### Ejemplo de respuesta en caso de permisos insuficientes

```json
{
    "Mensaje": "Solo el admin puede crear nuevos modelos"
}
```

---

### Borrar un modelo

- **Método**: `POST`
- **Endpoint**: `/modelo/borrar`
- **Encabezado de la solicitud**: 
  - `Authorization: Bearer <tu_token_de_acceso>`
- **Cuerpo de la solicitud**

    ```json
    {
        "id": 1
    }
    ```

- **Descripción**: Este endpoint permite marcar un modelo como inactivo. Solo los usuarios con rol de administrador o editor pueden acceder a este endpoint.

#### Ejemplo de respuesta exitosa

```json
{
    "Mensaje": "El borrado fue exitoso",
    "Modelo": "Modelo Ejemplo"
}
```

#### Ejemplo de respuesta en caso de permisos insuficientes

```json
{
    "Mensaje": "Usted no tiene permiso de borrar modelo"
}
```

#### Ejemplo de respuesta si el modelo ya está borrado

```json
{
    "Mensaje": "Este modelo fue borrado anteriormente",
    "Modelo": "Modelo Ejemplo"
}
```

---

### Editar un modelo

- **Método**: `POST`
- **Endpoint**: `/modelo/editar`
- **Encabezado de la solicitud**: 
  - `Authorization: Bearer <tu_token_de_acceso>`
- **Cuerpo de la solicitud**

    ```json
    {
        "id": 1,
        "nombre": "Nombre Editado",
        "id_marca": 2
    }
    ```

- **Descripción**: Este endpoint permite editar el nombre de un modelo activo y asociarlo a otra marca. Solo los usuarios con rol de administrador o editor pueden acceder a este endpoint.

#### Ejemplo de respuesta exitosa

```json
{
    "Mensaje": "El modelo fue editado exitosamente",
    "Modelo": "Nombre Editado"
}
```

#### Ejemplo de respuesta en caso de permisos insuficientes

```json
{
    "Mensaje": "Usted no tiene permiso de editar Modelos"
}
```

#### Ejemplo de respuesta si el modelo ya está borrado

```json
{
    "Mensaje": "El modelo fue borrado"
}
```