# Anteproyecto Formal

## Big Data y Mineria de Datos para la Identificacion de Perfiles de Riesgo en Registros de Intento de Suicidio

**Autor:** [Nombre del estudiante]  
**Programa:** [Nombre del programa academico]  
**Asignatura:** [Nombre de la asignatura]  
**Institucion:** Institucion Universitaria Salazar y Herrera  
**Fecha:** Abril de 2026

## 1. Introduccion

El analisis de datos en salud publica se ha convertido en un elemento fundamental para comprender fenomenos complejos, identificar poblaciones vulnerables y apoyar procesos de toma de decisiones. En este contexto, los registros asociados al intento de suicidio constituyen una fuente de informacion de alto valor, debido a que permiten estudiar factores demograficos, sociales, clinicos y territoriales vinculados con conductas de riesgo.

No obstante, el valor analitico de estos datos depende de dos condiciones esenciales. La primera es contar con una infraestructura capaz de almacenar y procesar grandes volumenes de informacion de manera eficiente, escalable y ordenada. La segunda es disponer de tecnicas analiticas que permitan transformar dichos datos en conocimiento util. En otras palabras, no es suficiente con mover y limpiar datos; tambien es necesario interpretarlos, modelarlos y convertirlos en evidencia aplicable.

Bajo esta perspectiva, el presente anteproyecto propone la integracion de dos enfoques complementarios. Por un lado, se plantea una arquitectura de Big Data en AWS para la ingesta, transformacion, almacenamiento y consulta del dataset SIVIGILA relacionado con intento de suicidio. Por otro lado, se incorpora la metodologia CRISP-DM como marco para el desarrollo de un proceso de mineria de datos que permita identificar perfiles de riesgo, patrones territoriales y variables asociadas al fenomeno de estudio.

La integracion de ambos enfoques permite construir una propuesta unificada en la que Big Data actua como soporte tecnologico y la mineria de datos como mecanismo de generacion de conocimiento. De esta manera, el proyecto trasciende la implementacion de un pipeline tecnico y se orienta hacia una solucion analitica con posible utilidad en contextos de vigilancia epidemiologica y prevencion.

## 2. Planteamiento del problema

El incremento en la disponibilidad de registros epidemiologicos y administrativos en salud ha generado la necesidad de contar con soluciones tecnologicas que permitan su procesamiento de manera eficiente. En el caso del intento de suicidio, los datos reportados en sistemas de vigilancia contienen informacion relevante para analizar tendencias, factores asociados y perfiles poblacionales con mayor exposicion al riesgo. Sin embargo, en muchos casos estos datos se encuentran dispersos, en formatos heterogeneos o sin una estructura analitica adecuada para su explotacion.

Desde la perspectiva de ingenieria de datos, uno de los principales desafios consiste en construir un flujo de procesamiento capaz de recibir los datos, depurarlos, transformarlos y disponibilizarlos para consulta de forma escalable. Desde la perspectiva analitica, el reto consiste en aplicar tecnicas de mineria de datos que permitan descubrir relaciones no evidentes, segmentar perfiles y apoyar procesos de evaluacion del riesgo.

Actualmente, ambos enfoques suelen abordarse por separado. Esto genera una desconexion entre la infraestructura que procesa los datos y los modelos que deberian aprovecharlos. En consecuencia, se pierde la oportunidad de construir una solucion integral en la que la arquitectura Big Data no sea un fin en si misma, sino una base para la generacion de conocimiento aplicable.

En este escenario surge la siguiente pregunta de investigacion: **como integrar una arquitectura Big Data en AWS con tecnicas de mineria de datos para identificar perfiles de riesgo y patrones relevantes en registros de intento de suicidio reportados en SIVIGILA**.

## 3. Justificacion

La pertinencia de este proyecto puede analizarse desde tres dimensiones. En primer lugar, desde el componente tecnico, la propuesta permite consolidar una arquitectura de procesamiento de datos basada en servicios de AWS tales como Amazon S3, AWS Glue, AWS Step Functions y Amazon Athena. Esta arquitectura facilita la organizacion del flujo de datos mediante capas Bronze, Silver y Gold, lo cual mejora la trazabilidad, la calidad y la disponibilidad de la informacion para fines analiticos.

En segundo lugar, desde el componente academico, el proyecto permite articular de manera coherente el anteproyecto de Big Data con los lineamientos de mineria de datos y la metodologia CRISP-DM. Esta integracion fortalece la solidez conceptual del trabajo, dado que vincula la infraestructura de datos con una metodologia formal para la exploracion, preparacion, modelado, evaluacion y posible despliegue de resultados.

En tercer lugar, desde el componente social, el fenomeno del intento de suicidio representa una problematica de interes en salud publica que requiere herramientas analiticas para identificar grupos vulnerables, zonas de mayor incidencia y posibles factores asociados. Si bien el proyecto no pretende sustituir el analisis clinico o institucional, si busca aportar una base tecnica y analitica que favorezca el uso de datos para procesos de observacion, seguimiento y prevencion.

Por lo anterior, la integracion entre Big Data y mineria de datos no solo es viable, sino necesaria, ya que permite pasar de un enfoque centrado exclusivamente en infraestructura a un modelo de analitica aplicada con potencial valor para la toma de decisiones.

## 4. Objetivos

### 4.1 Objetivo general

Disenar e implementar una solucion integrada de Big Data y mineria de datos para procesar registros de intento de suicidio, identificar perfiles de riesgo y generar conocimiento analitico que apoye procesos de prevencion y vigilancia epidemiologica.

### 4.2 Objetivos especificos

1. Construir un pipeline de procesamiento de datos en AWS con arquitectura Bronze, Silver y Gold para el tratamiento del dataset SIVIGILA.
2. Estandarizar, depurar y transformar los datos con el fin de mejorar su calidad y disponibilidad para el analisis.
3. Generar tablas analiticas en la capa Gold que faciliten consultas epidemiologicas y sirvan como base para el modelado.
4. Aplicar la metodologia CRISP-DM para el entendimiento del negocio, la comprension de los datos, la preparacion, el modelado y la evaluacion.
5. Identificar variables asociadas al riesgo, patrones territoriales y perfiles poblacionales vulnerables mediante tecnicas de mineria de datos.
6. Evaluar modelos de clasificacion o segmentacion que aporten evidencia para la interpretacion del fenomeno estudiado.

## 5. Marco conceptual y metodologico

La propuesta se fundamenta en la complementariedad entre Big Data y mineria de datos. Big Data proporciona la infraestructura necesaria para almacenar, transformar y consultar grandes volumenes de informacion, mientras que la mineria de datos permite extraer patrones, relaciones y conocimiento a partir de dichos datos.

En el presente proyecto, la arquitectura tecnologica se apoya en servicios de AWS. Amazon S3 cumple la funcion de lago de datos. AWS Glue se emplea para los procesos ETL. AWS Step Functions permite la orquestacion del flujo de procesamiento. Finalmente, Amazon Athena facilita la consulta sobre las tablas analiticas generadas. Esta combinacion permite estructurar el proceso en capas: Bronze para la ingesta cruda, Silver para los datos limpios y estandarizados, y Gold para los conjuntos de datos enriquecidos y orientados a analitica.

Sobre esta base tecnologica se incorpora la metodologia CRISP-DM como marco de trabajo para la mineria de datos. En la fase de comprension del negocio se define el problema y su valor dentro del contexto de salud publica. En la fase de comprension de los datos se examina la estructura del dataset, la calidad de la informacion y las distribuciones iniciales. En la fase de preparacion se realizan procesos de limpieza, transformacion, codificacion y construccion de variables. En la fase de modelado se evalua el uso de tecnicas de clasificacion o segmentacion. Posteriormente, en la fase de evaluacion se comparan resultados y se determina la utilidad del modelo seleccionado. Finalmente, la fase de despliegue se orienta a la publicacion de resultados agregados y al consumo analitico mediante consultas o visualizaciones.

## 6. Descripcion de la solucion propuesta

La solucion propuesta integra una arquitectura Big Data y una estrategia de mineria de datos en un mismo flujo de trabajo. El dataset de intento de suicidio es almacenado inicialmente en formato crudo dentro de la capa Bronze. A continuacion, un proceso ETL en AWS Glue transforma dicho conjunto de datos hacia una capa Silver, donde se realizan tareas de limpieza, normalizacion de columnas, depuracion de nulos, tratamiento de duplicados y validacion de columnas criticas.

Posteriormente, un segundo proceso ETL construye la capa Gold, orientada a analitica. Dentro de esta capa se generan al menos dos estructuras principales. La primera corresponde a una tabla de resumen por comuna y anio, util para analisis descriptivo y territorial. La segunda corresponde a una tabla de perfil de riesgo individual, en la cual se integran variables demograficas y factores disponibles para construir un puntaje de riesgo y una clasificacion analitica.

Estas tablas Gold constituyen la base para el desarrollo de tecnicas de mineria de datos. En funcion del objetivo final, el proyecto puede orientarse hacia modelos de clasificacion, cuando se busque estimar niveles de riesgo, o hacia modelos de segmentacion, cuando se pretenda agrupar perfiles poblacionales con caracteristicas similares. En ambos casos, el componente de Big Data garantiza que el proceso de analitica se soporte sobre una estructura organizada y escalable.

## 7. Datos y variables de interes

El proyecto utiliza como fuente principal un dataset de registros de intento de suicidio con variables asociadas a edad, sexo, comuna, hospitalizacion, antecedentes, metodo del intento y otros factores psicosociales o clinicos disponibles en la fuente. Estas variables permiten abordar el fenomeno desde diferentes niveles de analisis.

En el nivel descriptivo, es posible examinar distribuciones por grupo etario, sexo, comuna y periodo. En el nivel explicativo, se pueden explorar asociaciones entre hospitalizacion, intentos previos, factores de riesgo y metodos utilizados. En el nivel predictivo o de segmentacion, estas mismas variables sirven como insumo para construir modelos que permitan identificar perfiles con caracteristicas semejantes o niveles de riesgo diferenciados.

Las estructuras Gold actualmente definidas resultan especialmente pertinentes para este fin. La tabla de resumen por comuna y anio permite identificar concentraciones de casos y tendencias territoriales. La tabla de perfil de riesgo, por su parte, constituye una base adecuada para procesos de clasificacion o clustering, dado que concentra atributos individuales relevantes para la analitica.

## 8. Metodologia de desarrollo

El desarrollo del proyecto se llevara a cabo siguiendo las fases de CRISP-DM, articuladas con la arquitectura de datos implementada en AWS.

En la fase de comprension del negocio se definira con precision el problema analitico, las preguntas de interes y el aporte esperado del estudio. En la fase de comprension de los datos se realizara un analisis exploratorio apoyado en estadistica descriptiva, revision de tipos de datos, deteccion de nulos, duplicados, valores atipicos e inconsistencias.

En la fase de preparacion de los datos se construira el dataset final para modelado, incluyendo procesos de codificacion de variables categoricas, transformacion de atributos, seleccion de variables relevantes y eventual escalamiento de variables numericas cuando el modelo lo requiera. En la fase de modelado se entrenaran distintos algoritmos, entre ellos modelos de clasificacion como Regresion Logistica, Arbol de Decision o Random Forest, y modelos de segmentacion como K-Means, de acuerdo con el objetivo analitico definitivo.

En la fase de evaluacion se utilizaran metricas apropiadas al tipo de problema. Para clasificacion podran emplearse accuracy, precision, recall, F1-score y ROC-AUC. Para segmentacion se podran considerar metricas como Silhouette Score. Finalmente, en la fase de despliegue se dejara preparada la consulta de resultados sobre Athena y la posibilidad de construir visualizaciones o tableros para comunicacion de hallazgos.

## 9. Alcance

El alcance del proyecto comprende la ingesta, limpieza, transformacion y organizacion del dataset en una arquitectura Big Data sobre AWS, asi como la aplicacion de tecnicas de mineria de datos orientadas al descubrimiento de perfiles y patrones de riesgo. Tambien incluye la construccion de tablas analiticas, la realizacion de analisis exploratorio, la preparacion de datos para modelado y la evaluacion de modelos seleccionados.

No forma parte del alcance de esta propuesta el despliegue clinico en ambientes productivos, la integracion operativa en tiempo real con entidades prestadoras de salud ni la implementacion completa de procesos MLOps. Tales elementos pueden considerarse como trabajo futuro o lineas de ampliacion posteriores.

## 10. Resultados esperados

Se espera que el proyecto permita obtener una arquitectura reproducible para el procesamiento de datos de salud en AWS, asi como un conjunto de tablas analiticas confiables y utiles para la exploracion y el modelado. Adicionalmente, se espera identificar patrones, perfiles o asociaciones relevantes dentro de los registros analizados, con especial interes en variables demograficas, territoriales y de riesgo.

Desde el punto de vista academico, se espera demostrar que la combinacion entre Big Data y mineria de datos no solo es metodologicamente coherente, sino tecnicamente funcional. Desde el punto de vista aplicado, se espera generar insumos que puedan orientar la interpretacion del fenomeno y servir como base para estudios posteriores o estrategias de seguimiento.

## 11. Conclusiones preliminares

La principal fortaleza de esta propuesta radica en que integra dos dimensiones que usualmente se desarrollan de manera separada: la infraestructura de datos y la analitica avanzada. Bajo este enfoque, Big Data deja de ser un ejercicio exclusivamente tecnico para convertirse en el soporte de un proceso de mineria de datos con valor interpretativo. A su vez, la mineria de datos deja de depender de procesos aislados o manuales, al apoyarse en una arquitectura organizada, escalable y preparada para el analisis.

En consecuencia, el proyecto propone una narrativa unica y formalmente consistente: una plataforma de Big Data en AWS que procesa registros de intento de suicidio y una estrategia de mineria de datos basada en CRISP-DM para identificar perfiles de riesgo y patrones relevantes para la prevencion. Esta integracion ofrece una base solida para el desarrollo del trabajo academico y para futuras extensiones analiticas.

## 12. Titulo definitivo sugerido

**Big Data y Mineria de Datos para la Identificacion de Perfiles de Riesgo en Registros de Intento de Suicidio mediante AWS y CRISP-DM**