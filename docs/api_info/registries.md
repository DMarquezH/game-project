# Documentación de la API de Registros (RegistryAPI) #

Permite definir registros (objetos Registry[T]) para el registro controlado de objetos de un tipo, y que
requieren ser accedidos de forma recurrente por clases consumidoras.

Los registros son colecciones especiales que permiten almacenar instancias de un tipo de objeto concreto,
identificadas cada una por una clave.

El objetivo principal de un registro es registrar objetos bajo clave en fase de arranque, de tal forma que puedan
ser accedidos