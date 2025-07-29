# estrategia-datos-AWS-

 Ejercicio 1
Una compañía comercializadora de energía compra la electricidad a los generadores en el mercado mayoritario, donde después de una serie de contratos y control riesgos de precios esta se vende a los usuarios finales que pueden ser clientes residenciales, comerciales o industriales. 
El sistema de la compañía que administra este producto tiene la capacidad de exportar la información de proveedores, clientes y transacciones en archivos CSV. 
Requisitos técnicos: 
1.	Crear una estrategia de datalake en s3 con las capas que usted considere necesario tener y cargue esta información de manera automática y periódica. Los archivos deben particionarse por fecha de carga. 
2.	Realice 3 transformaciones básicas de datos utilizando AWS Glue y transforme la información para que esta sea almacenada en formato parquet en una zona procesada. 
3.	Utilizando AWS Glue, crea un proceso que detecte y catalogue automáticamente los esquemas de los datos almacenados en el datalake. 
4.	Utilizando Amazon Athena desde Python, realiza consultas SQL básicas sobre los datos que han sido transformados. 

Documentación: 
1.	Realiza una descripción detallada del pipeline de datos construido. 
2.	Indica que proceso es necesario seguir para configurar permisos y políticas para los diferentes servicios de AWS utilizados. 

 Puntos adicionales (plus) 
1.	Crea la IaC (Infraestructura como código) necesaria para desplegar esta solución en AWS. 
2.	Configure AWS Lakeformation para centralizar el gobierno, la seguridad y compartir los datos alojados en el datalake creado. 
3.	Construya un pipeline de datos que permita cargar esta información desde el datalake en la zona procesada a un datawarehouse en redshift. 

Utilice información ficticia en los archivos csv que se simula entregue el sistema transaccional. A continuación, tendrá una recomendación de columnas de estos archivos, pero podrá ajustarla a sus necesidades:
Archivo proveedores: nombre de proveedor, tipo de energía (eólica, hidroeléctrica, nuclear). Archivo clientes: tipo de identificación, identificación, nombre, ciudad. 
Archivo transacciones: tipo de transacción (venta o compra), nombre del cliente/proveedor, cantidad comprada, precio, tipo de energía. 
Importante: El código fuente creado deberá ser desplegado en una herramienta de control de versiones como github, azure devops, gitlab o similares.

SOLUCION PLANTEADA

Descripción del desarrollo del Ejercicio 1
Para el desarrollo del ejercicio, el primer paso consistió en la creación de tres fuentes de datos ficticias (clientes, proveedores y transacciones), con la estructura definida previamente. Estas fuentes fueron generadas en formato CSV, tal como se evidencia en las imágenes adjuntas.
A continuación, se procedió a configurar el servicio Amazon S3, donde se crearon dos buckets:
•	datalake-energia-carlos (zona de entrada del data lake)
•	datawarehouse-energia-carlos (zona de salida o procesada)
Dentro de cada bucket, se organizaron carpetas correspondientes a cada tipo de dato: clientes/, proveedores/ y transacciones/, con el fin de almacenar los archivos de manera estructurada y particionada por fecha de carga.
El siguiente paso fue utilizar el servicio AWS Glue, específicamente la herramienta Data Catalog. Allí se creó un crawler, que se encargó de identificar automáticamente los esquemas de las fuentes de datos en S3, mapearlas y registrarlas en una base de datos del catálogo. Para su correcta ejecución, fue necesario:
•	Crear y configurar una política de permisos (IAM Role) con acceso tanto a los buckets de S3 como a los recursos de Glue.
•	Definir correctamente la ruta de origen del bucket y carpeta donde se encuentran los archivos CSV.
•	Crear una base de datos en Glue que almacenara los metadatos generados por el crawler.
Una vez ejecutado el crawler, se validó que las tablas fueran correctamente creadas en la base de datos del Data Catalog. Posteriormente, se utilizó el servicio Amazon Athena para realizar consultas SQL y explorar los datos catalogados directamente desde S3.
Después de validar los datos, se procedió a la creación de un ETL Job en AWS Glue, el cual permitió transformar los datos de manera sencilla:
•	Se unieron las tablas de clientes y transacciones a través del campo id_cliente.
•	Se transformaron los archivos CSV al formato Parquet, lo cual optimiza el rendimiento de las consultas y reduce el almacenamiento.
•	La salida de este proceso se almacenó en la zona procesada del bucket datawarehouse-energia-carlos.
Para esta etapa también fue necesario:
•	Configurar la base de datos de destino que recibiría la información transformada.
•	Asignar adecuadamente los permisos del rol IAM utilizado, asegurando que tuviera autorización para escribir en el bucket de salida.




