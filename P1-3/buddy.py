# buddy.py
# Kevin Briceño 15-11661
# Implementación simple del Buddy System en Python

"""
API principal:
- BuddyAllocator(total_blocks)
- reserve(k_blocks, name) -> (start, order)
- free(name)
- show() -> str
- run_cli(total_blocks) -> bucle interactivo (RESERVAR/LIBERAR/MOSTRAR/SALIR)

Notas:
- total_blocks debe ser potencia de dos.
- Las direcciones/starts son índices en unidades (0..N-1).
- 'order' significa tamaño = 2**order.
"""

from math import log2
from typing import Dict, List, Tuple

class BuddyError(Exception):
    """Excepción específica del manejador buddy."""
    pass

class BuddyAllocator:
    """Clase que implementa un buddy allocator sencillo."""

    def __init__(self, total_blocks: int):
        # Validaciones iniciales
        if total_blocks <= 0:
            raise BuddyError("Total de bloques debe ser positivo")
        if (total_blocks & (total_blocks - 1)) != 0:
            raise BuddyError("Total de bloques debe ser potencia de dos (p. ej. 8, 16, 32)")
        self.N = total_blocks
        self.max_order = int(log2(self.N))
        # free_lists[order] = lista de starts libres para bloques de tamaño 2**order
        self.free_lists: Dict[int, List[int]] = {o: [] for o in range(self.max_order + 1)}
        # inicialmente todo libre en el order máximo, inicio 0
        self.free_lists[self.max_order].append(0)
        # asignaciones activas: name -> (start, order)
        self.allocated: Dict[str, Tuple[int,int]] = {}

    def _find_suitable_order(self, k_blocks: int) -> int:
        """Devuelve el menor order tal que 2**order >= k_blocks.
        Lanza BuddyError si k_blocks <= 0."""
        if k_blocks <= 0:
            raise BuddyError("Cantidad de bloques solicitada debe ser positiva")
        order = 0
        while (1 << order) < k_blocks:
            order += 1
        return order

    def reserve(self, k_blocks: int, name: str) -> Tuple[int,int]:
        """Reservar al menos k_blocks (unidades) con identificador name.
        Devuelve (start, order). Lanza BuddyError si falla."""
        if name in self.allocated:
            raise BuddyError(f"El nombre '{name}' ya está reservado")
        order = self._find_suitable_order(k_blocks)
        # buscar un bloque libre en order >= desired
        chosen_order = None
        for o in range(order, self.max_order + 1):
            if self.free_lists[o]:
                chosen_order = o
                break
        if chosen_order is None:
            raise BuddyError("No hay bloque suficientemente grande para la solicitud")
        # tomar el bloque y dividir hasta llegar al order deseado
        start = self.free_lists[chosen_order].pop(0)
        for o in range(chosen_order - 1, order - 1, -1):
            # al dividir, creamos el buddy superior y lo añadimos a free_lists[o]
            buddy_start = start + (1 << o)
            self.free_lists[o].append(buddy_start)
            # start (la mitad baja) se mantiene para seguir dividiendo si hace falta
        # registrar asignación
        self.allocated[name] = (start, order)
        return (start, order)

    def free(self, name: str) -> None:
        """Liberar una asignación por nombre y coalescer con su buddy si es posible."""
        if name not in self.allocated:
            raise BuddyError(f"El nombre '{name}' no fue encontrado")
        cur_start, cur_order = self.allocated.pop(name)
        # intentar fusionar con buddy mientras sea posible
        while True:
            buddy = cur_start ^ (1 << cur_order)  # cálculo XOR para obtener buddy
            fl = self.free_lists[cur_order]
            if buddy in fl:
                # si el buddy está libre, lo removemos y subimos un order
                fl.remove(buddy)
                cur_start = min(cur_start, buddy)  # el start del bloque fusionado
                cur_order += 1
                if cur_order > self.max_order:
                    # no sobrepasar el order máximo
                    break
                # continuar intentando fusionar en el siguiente nivel
            else:
                # si no hay buddy libre, insertamos el bloque en su lista y terminamos
                fl.append(cur_start)
                break

    def show(self) -> str:
        """Representación textual del estado actual: listas libres y asignaciones."""
        lines = [f"Total blocks: {self.N} (orders 0..{self.max_order})", "Free lists:"]
        for o in range(self.max_order, -1, -1):
            size = 1 << o
            starts = sorted(self.free_lists[o])
            lines.append(f"  order {o} (size={size}): {starts}")
        lines.append("Allocations:")
        for name, (start, order) in sorted(self.allocated.items()):
            lines.append(f"  {name}: start={start}, size={1<<order} (order {order})")
        return "\n".join(lines)

def run_cli(total_blocks: int):
    """Bucle interactivo simple. Comandos:
    RESERVAR <cantidad> <nombre>
    LIBERAR <nombre>
    MOSTRAR
    SALIR
    """
    allocator = BuddyAllocator(total_blocks)
    print(f"Buddy allocator iniciado con {total_blocks} bloques (unidad)")
    while True:
        try:
            cmd = input("ACTION> ").strip()
        except EOFError:
            break
        if not cmd:
            continue
        toks = cmd.split()
        verb = toks[0].upper()
        try:
            if verb == "RESERVAR":
                if len(toks) != 3:
                    print("Uso: RESERVAR <cantidad> <nombre>")
                    continue
                k = int(toks[1])
                name = toks[2]
                start, order = allocator.reserve(k, name)
                print(f"Reservado '{name}' en start {start}, size {1<<order} (order {order})")
            elif verb == "LIBERAR":
                if len(toks) != 2:
                    print("Uso: LIBERAR <nombre>")
                    continue
                name = toks[1]
                allocator.free(name)
                print(f"Liberado '{name}'")
            elif verb == "MOSTRAR":
                print(allocator.show())
            elif verb == "SALIR":
                print("Bye")
                break
            else:
                print("Acción desconocida. Válidas: RESERVAR, LIBERAR, MOSTRAR, SALIR")
        except BuddyError as e:
            print("ERROR:", e)
        except ValueError:
            print("ERROR: se esperaba un valor numérico donde corresponde")
