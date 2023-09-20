## Proyecto 1 

En este primer proyecto vamos a desarrollar una applicación web sencilla
utilizando solamente la librería estándar de python y *Redis* un almacen de
datos en memoria.

Para darte una idea del tipo de aplicación que vamos a programar, ejecuta el
servidor HTTP Básico de Python en el directorio `Books`.

```bash
python3 -m http.server 8000
```

Como puedes ver esta es una aplicación muy sencilla para ver unos libros en una
biblioteca. La página principal simplemente nos muestra la lista actual de
cuatro libros con un enlace al detalle de cada uno.  Como es un sitio estático,
cada enlace nos lleva a un archivo en el directorio `Books` donde se muestra la
descripción detallada del libro.

Vamos a modificar el servidor como vimos en clase para agregar algo de
funcionalidad al sitio.

### Almacena los libros en redis

En lugar de guardar las páginas de l:wos libros en archivos `.html`, los 
vamos a guardar en redis. Como es un almacen en memoria la recuperación será 
mucho más rápida.

#### Carga el sitio desde  `Books\`

Haz un programa que carge todos los archivos que tenemos en el directorio
`Books\' a redis. Utiliza el nombre del archivo o el número de libro para
generar la llave con la que vamos a almacenar el documento html. También puedes
almacenar solamente partes del documento, esto lo decides tu.


#### Genera las páginas a partir de los datos

Intenta generar la página principal Define una estratégia para generar las
páginas que hasta este momento son estáticas.

### Sesiones

#### Una sesión para cada usuario

Utilizando Cookies, genera una sesión distinta para cada usuario que llegue al
sitio. Para verificar que se está generando la sesión debes desplegar en número
de sesión al final de la página. La sesión debe vencer en 10 segundos.

Es una buena idea utilizar un generador de identificadores para que cada número
de sesión sea único. Puedes utilizar el módulo
[uuid](https://docs.python.org/3/library/uuid.html#uuid.uuid4).


#### Rastreo de la navegación

Ya que tenemos una sesión distinta para cada usuario, vamos a guardar en la
sesión los libros que ha visitado para recomendarle algún libro. 

Utilizando el número de sesión como llave, guarda en redis la lista de libros
que ha visitado el usuario. 

Puedes utilizar alguna de las estructuras que nos ofrece. Ya que el usuario
haya visistado tres libros, agrega uno que no haya visto al principio de la
lista.

### Formulario de Búsqueda

Implementa un formulario de búsqueda dónde se puedan agregar tres términos,
genera una página con los libros que concuerden en la búsqueda. Dependiendo de
la experiencia que tengas esto se puede hacer muy elaborado. Por ejemplo, se
puede utilizar Redis para indexar las descripciones de los libros. A esto se le
conoce como Full-Text search.

En este caso la forma debe realizar a una petición `GET` y debes extraer los
términos del `QueryString`.

Bibliografía:

* [Librería de redis para python](https://redis-py.readthedocs.io/en/stable/)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [Redis](https://redis.com/glossary/full-text-search/)

#### Reto opcional: Sesiones sin cookies

Hay una estratégia para mantener una sesión activa sin utilizar cookies. La
idea es incluir en todos los enlaces un identificador de sesión como
QueryString. Utilzando esta idea, puedes almacenar el estado de la navegación
sin el uso de cookies. De seguro haz visto este tipo de URL en los enlaces de
Amazon:

```text
https://www.amazon.com/s?k=gaming+mouse&language=es&_encoding=UTF8&content-id=amzn1.sym.8148f1e1-83ed-498f-85be-ff288b197da7&pd_rd_r=d802ef30-2ad7-430f-b7ec-b5dc31e02478&pd_rd_w=cYFhX&pd_rd_wg=gVbFZ&pf_rd_p=8148f1e1-83ed-498f-85be-ff288b197da7&pf_rd_r=KMECK499C701MHB8A56R&ref=pd_gw_unk
```

En este caso se almacena información relacionada con los productos, los
términos de la búsqueda entre otras variables.

### Información Adicional

* Debes agregar libros con información real.
* Puedes generar un directorio con datos reales de alguna fuente abierta.
* Puedes agregegar otros elementos a la página, imágenes, etc.
* Es importante *no* darle estilo a la página.

