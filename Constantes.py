dbname = 'postgres'
user = 'postgres'
password = 'root'
host = 'localhost'
port= '5432'


QUERY_CLIENTES_ACTIVOS = ('SELECT * FROM scexamen.personas  WHERE estado = 1')
QUERY_VUELOS = ('SELECT * FROM scexamen.vuelos')

QUERY_VUELOS_BY_PASAJERO = ('SELECT c.nombre as "Ciudad origen", c2.nombre as "Ciudad destino" FROM scexamen.vuelos v JOIN scexamen.usuariosvuelo uv ON v.id=uv.idvuelo JOIN scexamen.personas p ON p.id=uv.idpasajero '
                            'JOIN scexamen.ciudades c ON c.id=v.idciudadorigen JOIN scexamen.ciudades c2 ON c2.id=v.idciudaddestino WHERE p.id=%(id_pasajero)s')
QUERY_DIRECCION_BY_PASAJERO = 'SELECT d.calle, d.cp FROM scexamen.direccion d JOIN scexamen.personas p ON d.id=p.iddireccion WHERE p.id = %(id_pasajero)s'

QUERY_PASAJEROS_BY_VUELO = ('SELECT p.nombre, p.apellidos, c.nombre as "Ciudad origen", c2.nombre as "Ciudad destino", uv.preciobillete as "Precio_billete" FROM scexamen.vuelos v JOIN scexamen.usuariosvuelo uv ON v.id=uv.idvuelo JOIN scexamen.personas p ON p.id=uv.idpasajero '
                            'JOIN scexamen.ciudades c ON c.id=v.idciudadorigen JOIN scexamen.ciudades c2 ON c2.id=v.idciudaddestino WHERE v.id=%(id_vuelo)s')

QUERY_UPDATE_PASAJEROS = ('SELECT p.* FROM scexamen.vuelos v JOIN scexamen.usuariosvuelo uv ON v.id=uv.idvuelo JOIN scexamen.personas p ON p.id=uv.idpasajero '
                          'WHERE v.id=%(id_vuelo)s')
UPDATE_PASAJEROS_MUERTOS = 'UPDATE scexamen.personas set fechadefuncion = CURRENT_DATE, estado = 2 WHERE id=%(id_cliente)s'
UPDATE_VUELO = 'UPDATE scexamen.vuelos set estadovuelo=\'No Destino\' WHERE id=%(id_vuelo)s'