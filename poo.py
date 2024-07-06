class Ownable:
    def __init__(self, owner):
        self.owner = owner


class Billetera(Ownable):
    def __init__(self, owner, saldo_inicial):
        super().__init__(owner)
        self.saldo = saldo_inicial

    def deducir(self, cantidad):
        if cantidad > self.saldo:
            return False
        self.saldo -= cantidad
        return True

    def recargar(self, cantidad):
        self.saldo += cantidad

    def transferir(self, cantidad, otra_billetera):
        if self.deducir(cantidad):
            otra_billetera.recargar(cantidad)
            return True
        return False


class Producto(Ownable):
    def __init__(self, owner, numero, nombre, precio, cantidad):
        super().__init__(owner)
        self.numero = numero
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad


class Carrito(Ownable):
    def __init__(self, owner):
        super().__init__(owner)
        self.items = []

    def agregar_producto(self, producto, cantidad):
        for item in self.items:
            if item['producto'].numero == producto.numero:
                item['cantidad'] += cantidad
                return
        self.items.append({'producto': producto, 'cantidad': cantidad})

    def monto_total(self):
        return sum(item['producto'].precio * item['cantidad'] for item in self.items)

    def mostrar(self):
        print("Contenido del carrito")
        print("+------+-------------+-------+--------+")
        print("| número | nombre producto | precio | cantidad |")
        print("+======+=============+=======+========+")
        for item in self.items:
            print(f"| {item['producto'].numero} | {item['producto'].nombre} | {item['producto'].precio} | {item['cantidad']} |")
        print("+------+-------------+-------+--------+")

    def vaciar(self):
        self.items = []

    def transferir_propiedad(self):
        for item in self.items:
            item['producto'].owner = self.owner

    def generar_factura(self):
        print("\nFactura de compra:")
        print("+------+-------------+-------+--------+")
        print("| número | nombre producto | precio | cantidad |")
        print("+======+=============+=======+========+")
        for item in self.items:
            print(f"| {item['producto'].numero} | {item['producto'].nombre} | {item['producto'].precio} | {item['cantidad']} |")
        print("+------+-------------+-------+--------+")
        print(f"Total: {self.monto_total()}")


class Tienda(Ownable):
    def __init__(self, owner):
        super().__init__(owner)
        self.productos = [
            Producto(owner, 0, "SSD 2.5 pulgadas", 13370, 10),
            Producto(owner, 1, "HDD 3.5 pulgadas", 10980, 10),
            Producto(owner, 2, "CPU", 40830, 10),
            Producto(owner, 3, "Enfriador de CPU", 13400, 10),
            Producto(owner, 4, "SSD M.2", 12980, 10),
            Producto(owner, 5, "Caja de PC", 8727, 10),
            Producto(owner, 6, "Tarjeta gráfica", 23800, 10),
            Producto(owner, 7, "Placa madre", 28980, 10),
            Producto(owner, 8, "Memoria", 13880, 10),
            Producto(owner, 9, "Unidad de fuente de poder", 8980, 10)
        ]

    def mostrar_productos(self):
        print("Lista de productos")
        print("+------+-------------+-------+--------+")
        print("| número | nombre producto | precio | cantidad |")
        print("+======+=============+=======+========+")
        for producto in self.productos:
            print(f"| {producto.numero} | {producto.nombre} | {producto.precio} | {producto.cantidad} |")
        print("+------+-------------+-------+--------+")

    def obtener_producto(self, numero_producto):
        for producto in self.productos:
            if producto.numero == numero_producto:
                return producto
        return None


def main():
    propietario_tienda = "DIC Store"
    propietario_usuario = "Kei Kamiguchi"

    billetera_tienda = Billetera(propietario_tienda, 0)
    billetera_usuario = Billetera(propietario_usuario, 1000000)

    tienda = Tienda(propietario_tienda)
    carrito = Carrito(propietario_usuario)

    while True:
        print("\n1. Empezar a comprar\n2. Salir")
        opcion = input("Elige una opción: ")
        if opcion == "2":
            break

        if opcion == "1":
            tienda.mostrar_productos()
            numero_producto = int(input("Por favor, introduce el número del producto: "))
            cantidad_producto = int(input("Introduce la cantidad del producto: "))

            producto = tienda.obtener_producto(numero_producto)
            if producto and producto.cantidad >= cantidad_producto:
                carrito.agregar_producto(producto, cantidad_producto)
                producto.cantidad -= cantidad_producto
            else:
                print("Producto no disponible o cantidad insuficiente.")
                continue

            carrito.mostrar()
            print(f"Monto total: {carrito.monto_total()}")
            terminar_compras = input("¿Deseas finalizar las compras? (sí/no): ")

            if terminar_compras.lower() in ["sí", "si"]:
                metodo_pago = input("Introduce el método de pago (tarjeta/billetera): ")
                total = carrito.monto_total()
                print(f"Total a transferir: {total}")
                print(f"Método de pago seleccionado: {metodo_pago}")

                print("Intentando transferir fondos...")
                if billetera_usuario.transferir(total, billetera_tienda):
                    print("¡Compra exitosa!")
                    print(f"Saldo de la billetera de {propietario_usuario}: {billetera_usuario.saldo}")
                    print(f"Saldo de la billetera de {propietario_tienda}: {billetera_tienda.saldo}")
                    carrito.transferir_propiedad()
                    carrito.generar_factura()
                    carrito.vaciar()
                else:
                    print("Fondos insuficientes.")
                    carrito.vaciar()
            else:
                print("Continuar comprando")
                continue

if __name__ == "__main__":
    main()
