"""Genera los diagramas UML de ``docs/uml`` desde el código, y sus imágenes PNG.

Uso:

    python -m scripts.generar_uml                  # todo: los .puml derivados y las PNG
    python -m scripts.generar_uml --sin-imagenes   # solo los .puml (no necesita Java)

Hay dos clases de diagramas en ``docs/uml``:

- **Derivados del código** (este script los reescribe enteros; no se editan a mano):
  ``01-paquetes.puml`` (carpetas reales e importaciones entre ellas),
  ``02-clases-entidades.puml`` (los modelos de SQLAlchemy) y ``03-clases-capas.puml``
  (``rutas.py`` → ``servicio.py`` → ``modelos.py`` de cada módulo, con sus endpoints y
  funciones).
- **Escritos a mano** con los nombres del código (componentes, despliegue, casos de uso y
  secuencias). ``tests/test_diagramas_uml.py`` falla si nombran un endpoint que no existe.

Las imágenes las dibuja PlantUML con Java (``java -jar``), usando su motor interno
"smetana": no hace falta Graphviz. El .jar no se sube al repositorio: se busca en
``.herramientas/`` y, si no está, se descarga ahí la versión fijada en ``VERSION_PLANTUML``
(se verifica su SHA-256). Con ``PLANTUML_JAR`` se indica otro .jar ya descargado.
"""

import argparse
import ast
import hashlib
import os
import shutil
import subprocess
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DIR_UML = RAIZ / "docs" / "uml"
DIR_MODULOS = RAIZ / "app" / "modulos"
# Carpetas de primer nivel que acompañan a app/ en el diagrama de paquetes.
OTRAS_CARPETAS = ("simulador_gps", "frontend")

VERSION_PLANTUML = "1.2025.2"
SHA256_PLANTUML = "862c7d6d0d3bde3c819eac4dfc03cf549046bf1d49c04d18a779eb2d834b77c9"
URL_PLANTUML = (
    "https://github.com/plantuml/plantuml/releases/download/"
    f"v{VERSION_PLANTUML}/plantuml-{VERSION_PLANTUML}.jar"
)
DIR_HERRAMIENTAS = RAIZ / ".herramientas"

AVISO = "' GENERADO por scripts/generar_uml.py desde el código. No editar a mano."
METODOS_HTTP = ("get", "post", "put", "patch", "delete")
# Archivos de un módulo que no son una capa: se listan aparte, sin caja propia.
_SIN_CAPA = {"esquemas", "esquemas_gestion", "excepciones", "modelos"}


# --- Lectura del código (AST: no importa la aplicación ni necesita el .env) ------------------


def _arbol(archivo: Path) -> ast.Module:
    return ast.parse(archivo.read_text(encoding="utf-8"))


def _modulos() -> list[str]:
    return sorted(p.name for p in DIR_MODULOS.iterdir() if (p / "__init__.py").exists())


def _archivos(carpeta: Path) -> list[Path]:
    return sorted(p for p in carpeta.glob("*.py") if p.name != "__init__.py")


def _importaciones(archivo: Path) -> set[str]:
    """Módulos de ``app`` que importa el archivo, con puntos (``app.modulos.pagos.servicio``)."""
    encontrados = set()
    for nodo in ast.walk(_arbol(archivo)):
        if isinstance(nodo, ast.ImportFrom) and nodo.module and nodo.module.split(".")[0] == "app":
            encontrados.add(nodo.module)
            # "from app.modulos.pagos import servicio" también nombra app.modulos.pagos.servicio
            encontrados.update(f"{nodo.module}.{alias.name}" for alias in nodo.names)
    return encontrados


def _funciones_publicas(archivo: Path) -> list[str]:
    return [
        n.name
        for n in _arbol(archivo).body
        if isinstance(n, ast.FunctionDef | ast.AsyncFunctionDef) and not n.name.startswith("_")
    ]


def _clases_con_metodos(archivo: Path) -> list[str]:
    """Clases públicas con al menos un método público (p. ej. ``PasarelaPagos``)."""
    clases = []
    for nodo in _arbol(archivo).body:
        if isinstance(nodo, ast.ClassDef) and not nodo.name.startswith("_"):
            metodos = [
                m.name
                for m in nodo.body
                if isinstance(m, ast.FunctionDef) and not m.name.startswith("_")
            ]
            decoradores = {
                ast.unparse(d) for m in nodo.body for d in getattr(m, "decorator_list", [])
            }
            if metodos and "property" not in decoradores:
                clases.append(nodo.name)
    return clases


def _enrutadores(arbol: ast.Module) -> dict[str, str]:
    """``{nombre_del_enrutador: prefijo}`` de un ``rutas.py``."""
    enrutadores = {}
    for nodo in arbol.body:
        if (
            isinstance(nodo, ast.Assign)
            and isinstance(nodo.value, ast.Call)
            and ast.unparse(nodo.value.func) == "APIRouter"
        ):
            prefijo = next((k.value.value for k in nodo.value.keywords if k.arg == "prefix"), "")
            enrutadores[nodo.targets[0].id] = prefijo
    return enrutadores


def endpoints(archivo: Path) -> list[tuple[str, str, str, str]]:
    """``(enrutador, MÉTODO, ruta completa, función)`` de cada endpoint del archivo."""
    arbol = _arbol(archivo)
    prefijos = _enrutadores(arbol) | {"app": ""}
    resultado = []
    for nodo in arbol.body:
        if not isinstance(nodo, ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        for decorador in nodo.decorator_list:
            if (
                isinstance(decorador, ast.Call)
                and isinstance(decorador.func, ast.Attribute)
                and decorador.func.attr in METODOS_HTTP
                and isinstance(decorador.func.value, ast.Name)
                and decorador.func.value.id in prefijos
            ):
                enrutador = decorador.func.value.id
                ruta = prefijos[enrutador] + decorador.args[0].value
                resultado.append((enrutador, decorador.func.attr.upper(), ruta, nodo.name))
    return resultado


def _encabezado(titulo: str) -> list[str]:
    return ["@startuml", AVISO, "!include estilo.iuml", f"title {titulo}", ""]


def _en_lineas(nombres: list[str], por_linea: int = 3) -> str:
    """Los nombres en letra pequeña, de a ``por_linea``. La etiqueta de tamaño va en cada
    línea (PlantUML no la mantiene tras un salto) y ``__`` se escapa para que no subraye.
    """
    grupos = [nombres[i : i + por_linea] for i in range(0, len(nombres), por_linea)]
    lineas = (" · ".join(g).replace("__", "~__") for g in grupos)
    return "\\n".join(f"<size:10>{linea}</size>" for linea in lineas)


# --- 01: paquetes ----------------------------------------------------------------------------


def _nodo_de(modulo_importado: str) -> str | None:
    """A qué caja del diagrama de paquetes pertenece ``app.x.y``."""
    partes = modulo_importado.split(".")
    if len(partes) < 2:
        return None
    if partes[1] == "modulos":
        return f"m_{partes[2]}" if len(partes) > 2 else None
    if partes[1] == "comun":
        return "comun"
    return f"a_{partes[1]}" if (RAIZ / "app" / f"{partes[1]}.py").exists() else None


def generar_paquetes() -> str:
    """Las carpetas reales del repositorio y qué importa a qué."""
    modulos = _modulos()
    sueltos = [p for p in _archivos(RAIZ / "app")]
    lineas = _encabezado("Diagrama de paquetes — TransportExperience (carpetas reales del código)")
    lineas.append('package "app/" as app {')
    for archivo in sueltos:
        lineas.append(f'  artifact "{archivo.name}" as a_{archivo.stem}')
    comunes = [p.name for p in _archivos(RAIZ / "app" / "comun")]
    lineas.append(f'  folder "comun/\\n{_en_lineas(comunes)}" as comun')
    lineas.append('  package "modulos/" as modulos {')
    for modulo in modulos:
        nombres = [p.name for p in _archivos(DIR_MODULOS / modulo)]
        lineas.append(f'    folder "{modulo}/\\n{_en_lineas(nombres)}" as m_{modulo}')
    lineas.extend(["  }", "}"])
    for carpeta in OTRAS_CARPETAS:
        nombres = sorted(
            p.name for p in (RAIZ / carpeta).iterdir() if p.is_file() and p.name != "__init__.py"
        )
        lineas.append(f'folder "{carpeta}/\\n{_en_lineas(nombres)}" as c_{carpeta}')
    lineas.append("")

    # main.py -> cada módulo cuyo enrutador reúne.
    for destino in sorted({_nodo_de(i) for i in _importaciones(RAIZ / "app" / "main.py")} - {None}):
        if destino.startswith("m_"):
            lineas.append(f"a_main --> {destino} : include_router")
        elif destino != "a_main":
            lineas.append(f"a_main ..> {destino}")

    # Entre módulos: una flecha por par; doble punta si se importan mutuamente.
    entre = set()
    transversales = set()
    for modulo in modulos:
        for archivo in _archivos(DIR_MODULOS / modulo):
            for importado in _importaciones(archivo):
                destino = _nodo_de(importado)
                if destino is None or destino == f"m_{modulo}":
                    continue
                if destino.startswith("m_"):
                    entre.add((f"m_{modulo}", destino))
                else:
                    transversales.add(destino)
    for origen, destino in sorted(entre):
        if (destino, origen) in entre:
            if origen < destino:
                lineas.append(f"{origen} <..> {destino}")
        else:
            lineas.append(f"{origen} ..> {destino}")

    usados = [
        "comun/" if t == "comun" else f"{t.removeprefix('a_')}.py" for t in sorted(transversales)
    ]

    # Archivos sueltos de app/ entre sí (menos modelos.py, que solo registra las tablas).
    for archivo in sueltos:
        if archivo.stem in {"main", "modelos"}:
            continue
        destinos = {_nodo_de(i) for i in _importaciones(archivo)} - {None, f"a_{archivo.stem}"}
        for destino in sorted(destinos):
            lineas.append(f"a_{archivo.stem} ..> {destino}")

    # Los dos programas que hablan con la API por HTTP (no la importan).
    lineas.extend(
        [
            "",
            "c_frontend ..> a_main : HTTP/JSON",
            "c_simulador_gps ..> a_main : HTTP (posiciones GPS)",
            "",
            "legend right",
            "  Flecha continua: main.py reúne el enrutador del módulo (include_router).",
            "  Flecha punteada: un paquete importa a otro (doble punta: en ambos sentidos).",
            f"  Los módulos de app/modulos/ usan además: {', '.join(usados)}.",
            "  app/modelos.py solo importa los modelos para que Alembic vea las tablas.",
            "end legend",
            "@enduml",
        ]
    )
    return "\n".join(lineas) + "\n"


# --- 02: clases (entidades de SQLAlchemy) ----------------------------------------------------


def _paquete_de(clase: type) -> str:
    partes = clase.__module__.split(".")
    return partes[2] if partes[1] == "modulos" else f"{partes[1]}.py"


def generar_entidades() -> str:
    """Las clases mapeadas por SQLAlchemy, con su tabla, columnas, enumeraciones y relaciones."""
    from sqlalchemy import Enum

    from app import modelos as _modelos  # noqa: F401  registra todas las tablas
    from app.db import Base
    from scripts.generar_diagrama_er import _tipo

    clases = sorted((m.class_ for m in Base.registry.mappers), key=lambda c: c.__name__)
    por_tabla = {c.__table__.name: c for c in clases}
    por_paquete = defaultdict(list)
    for clase in clases:
        por_paquete[_paquete_de(clase)].append(clase)

    lineas = _encabezado(f"Diagrama de clases — entidades de SQLAlchemy ({len(clases)} tablas)")
    lineas.append("set separator none")
    # Cada enumeración va una sola vez, en el paquete del módulo que la define.
    enumeraciones = defaultdict(dict)
    for clase in clases:
        for columna in clase.__table__.columns:
            if isinstance(columna.type, Enum) and columna.type.enum_class is not None:
                enumeracion = columna.type.enum_class
                enumeraciones[_paquete_de(enumeracion)][enumeracion.__name__] = columna.type.enums

    relaciones, usos = [], []
    for paquete in sorted(por_paquete):
        lineas.append(f'package "{paquete}" {{')
        for clase in por_paquete[paquete]:
            tabla = clase.__table__
            lineas.append(f"  class {clase.__name__} <<{tabla.name}>> {{")
            for columna in tabla.columns:
                if isinstance(columna.type, Enum) and columna.type.enum_class is not None:
                    tipo = columna.type.enum_class.__name__
                    usos.append(f"{clase.__name__} ..> {tipo}")
                else:
                    tipo = _tipo(columna)
                marcas = ("PK " if columna.primary_key else "") + (
                    "FK " if columna.foreign_keys else ""
                )
                opcional = " [0..1]" if columna.nullable else ""
                lineas.append(f"    {marcas}{columna.name} : {tipo}{opcional}")
                for fk in columna.foreign_keys:
                    padre = por_tabla[fk.column.table.name].__name__
                    cardinalidad = "0..1" if columna.nullable else "1"
                    relaciones.append(
                        f'{clase.__name__} "*" --> "{cardinalidad}" {padre} : {columna.name}'
                    )
            calculados = sorted(
                nombre
                for nombre, valor in vars(clase).items()
                if isinstance(valor, property) and not nombre.startswith("_")
            )
            if calculados:
                lineas.append("    --")
                lineas.extend(f"    {nombre}  <<property>>" for nombre in calculados)
            lineas.append("  }")
        for nombre, valores in sorted(enumeraciones[paquete].items()):
            lineas.append(f"  enum {nombre} {{")
            lineas.extend(f"    {valor}" for valor in valores)
            lineas.append("  }")
        lineas.append("}")
    lineas.append("")
    lineas.extend(sorted(relaciones))
    lineas.extend(sorted(set(usos)))
    lineas.append("@enduml")
    return "\n".join(lineas) + "\n"


# --- 03: clases por capas (rutas -> servicio -> modelos) -------------------------------------


def _modelos_de(archivo: Path) -> list[str]:
    """``Clase <<tabla>>`` de cada entidad y ``enum X`` de cada enumeración del archivo."""
    miembros = []
    for nodo in _arbol(archivo).body:
        if not isinstance(nodo, ast.ClassDef):
            continue
        bases = {ast.unparse(b) for b in nodo.bases}
        if "Base" in bases:
            tabla = next(
                (
                    s.value.value
                    for s in nodo.body
                    if isinstance(s, ast.Assign) and ast.unparse(s.targets[0]) == "__tablename__"
                ),
                "",
            )
            miembros.append(f"{nodo.name}  <<{tabla}>>")
        elif "StrEnum" in bases:
            miembros.append(f"enum {nodo.name}")
    return miembros


def generar_capas() -> str:
    """``main.py`` reúne los enrutadores; en cada módulo, rutas → servicio → modelos."""
    principal = RAIZ / "app" / "main.py"
    lineas = _encabezado(
        "Diagrama de clases por capas — rutas.py → servicio.py → modelos.py de cada módulo"
    )
    lineas.append("set separator none")
    lineas.append("left to right direction")
    lineas.append("")

    # main.py: el "control maestro" que reúne los enrutadores.
    reunidos = [
        ast.unparse(n.args[0])
        for n in ast.walk(_arbol(principal))
        if isinstance(n, ast.Call) and ast.unparse(n.func) == "app.include_router"
    ]
    lineas.append('class "app/main.py" as main <<control maestro>> {')
    lineas.append("  app = FastAPI(...)")
    lineas.append("  registrar_manejadores(app)")
    lineas.extend(f"  app.include_router({nombre})" for nombre in reunidos)
    lineas.append("  --")
    lineas.extend(f"  {metodo} {ruta} → {f}()" for _, metodo, ruta, f in endpoints(principal))
    lineas.append("}")
    lineas.append("")

    flechas = []
    for modulo in _modulos():
        carpeta = DIR_MODULOS / modulo
        archivos = {p.stem: p for p in _archivos(carpeta)}
        de_rutas = sorted(n for n in archivos if n.startswith("rutas"))
        propio = f"app.modulos.{modulo}."

        def internos(nombre: str, archivos=archivos, propio=propio) -> set[str]:
            """Archivos del mismo módulo que importa ``nombre``."""
            return {
                i.removeprefix(propio)
                for i in _importaciones(archivos[nombre])
                if i.startswith(propio) and i.removeprefix(propio) in archivos
            } - {nombre}

        # Capa de servicio: servicio.py y lo que las rutas llaman directamente.
        de_servicio = {"servicio"} & set(archivos)
        for nombre in de_rutas:
            de_servicio |= internos(nombre) - _SIN_CAPA - set(de_rutas)
        de_servicio = sorted(de_servicio)
        mostrados = set(de_rutas) | set(de_servicio) | ({"modelos"} & set(archivos))
        ademas = sorted(f"{n}.py" for n in set(archivos) - mostrados)

        titulo = f"app/modulos/{modulo}"
        if ademas:
            titulo += f"\\n<size:10>además: {', '.join(ademas)}</size>"
        lineas.append(f'package "{titulo}" {{')
        for nombre in de_rutas:
            lineas.append(f'  class "{nombre}.py" as {modulo}_{nombre} <<rutas>> {{')
            for _, metodo, ruta, funcion in endpoints(archivos[nombre]):
                lineas.append(f"    {metodo} {ruta} → {funcion}()")
            lineas.append("  }")
        for nombre in de_servicio:
            lineas.append(f'  class "{nombre}.py" as {modulo}_{nombre} <<servicio>> {{')
            lineas.extend(f"    class {c}" for c in _clases_con_metodos(archivos[nombre]))
            lineas.extend(f"    {f}()" for f in _funciones_publicas(archivos[nombre]))
            lineas.append("  }")
        if "modelos" in archivos:
            lineas.append(f'  class "modelos.py" as {modulo}_modelos <<modelos>> {{')
            lineas.extend(f"    {m}" for m in _modelos_de(archivos["modelos"]))
            lineas.append("  }")
        lineas.append("}")
        lineas.append("")

        for nombre in sorted(mostrados):
            for destino in sorted(internos(nombre) & mostrados):
                # Las rutas importan los modelos solo por sus tipos: flecha punteada.
                punta = "..>" if nombre in de_rutas and destino == "modelos" else "-->"
                flechas.append(f"{modulo}_{nombre} {punta} {modulo}_{destino}")
        # main.py -> el rutas.py que define cada enrutador.
        for nombre in de_rutas:
            definidos = [e for e in _enrutadores(_arbol(archivos[nombre])) if e in reunidos]
            if definidos:
                flechas.append(f"main --> {modulo}_{nombre} : {', '.join(definidos)}")

    lineas.extend(flechas)
    lineas.append("@enduml")
    return "\n".join(lineas) + "\n"


# --- Escritura y dibujo ----------------------------------------------------------------------

GENERADOS = {
    "01-paquetes.puml": generar_paquetes,
    "02-clases-entidades.puml": generar_entidades,
    "03-clases-capas.puml": generar_capas,
}


def escribir_generados() -> None:
    for nombre, generar in GENERADOS.items():
        (DIR_UML / nombre).write_text(generar(), encoding="utf-8", newline="\n")
        print(f"  {nombre}  (desde el código)")


def _sha256(archivo: Path) -> str:
    return hashlib.sha256(archivo.read_bytes()).hexdigest()


def obtener_plantuml() -> Path:
    """El .jar de PlantUML: el de ``PLANTUML_JAR``, el de ``.herramientas/`` o uno descargado."""
    indicado = os.environ.get("PLANTUML_JAR")
    if indicado:
        if not Path(indicado).is_file():
            sys.exit(f"PLANTUML_JAR apunta a un archivo que no existe: {indicado}")
        return Path(indicado)
    jar = DIR_HERRAMIENTAS / f"plantuml-{VERSION_PLANTUML}.jar"
    if not jar.exists():
        DIR_HERRAMIENTAS.mkdir(exist_ok=True)
        print(f"Descargando PlantUML {VERSION_PLANTUML} en {jar} ...")
        temporal = jar.with_suffix(".descarga")
        urllib.request.urlretrieve(URL_PLANTUML, temporal)  # noqa: S310  URL fija, https
        if SHA256_PLANTUML and _sha256(temporal) != SHA256_PLANTUML:
            temporal.unlink()
            sys.exit("El .jar descargado no coincide con el SHA-256 esperado. No se usa.")
        temporal.rename(jar)
    return jar


def dibujar() -> None:
    """Una PNG por cada .puml, al lado, con el mismo nombre."""
    if shutil.which("java") is None:
        sys.exit(
            "No se encontró Java, que PlantUML necesita para dibujar las imágenes.\n"
            "Los .puml sí quedaron actualizados. Instala Java (17 o más) y repite."
        )
    fuentes = sorted(DIR_UML.glob("*.puml"))
    orden = [
        "java",
        "-Djava.awt.headless=true",
        "-DPLANTUML_LIMIT_SIZE=16384",  # los diagramas de clases son grandes
        "-jar",
        str(obtener_plantuml()),
        "-tpng",
        "-charset",
        "UTF-8",
        "-failfast2",
        *[str(f) for f in fuentes],
    ]
    resultado = subprocess.run(orden, cwd=DIR_UML, check=False)
    if resultado.returncode != 0:
        sys.exit("PlantUML encontró errores en algún diagrama (ver arriba).")
    for fuente in fuentes:
        print(f"  {fuente.with_suffix('.png').name}")


def main(argumentos: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="python -m scripts.generar_uml", description=__doc__.split("\n")[0]
    )
    parser.add_argument(
        "--sin-imagenes", action="store_true", help="Solo reescribe los .puml; no usa Java."
    )
    args = parser.parse_args(argumentos)
    print("Diagramas derivados del código:")
    escribir_generados()
    if not args.sin_imagenes:
        print("Imágenes:")
        dibujar()


if __name__ == "__main__":
    main()
