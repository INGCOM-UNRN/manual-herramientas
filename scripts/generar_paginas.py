#!/usr/bin/env python3
"""Genera las páginas de herramientas del manual desde sus repositorios.

Cada página sale de dos fuentes que mantiene cada herramienta:

- su README (alcance, requisitos, uso, contrato con el ecosistema), adaptado a MyST:
  sin el título, sin la tabla de contenidos ni las secciones de contacto y licencia,
  con los enlaces relativos apuntando al repositorio;
- la ayuda real de la CLI (`<ejecutable> --help` y la de cada subcomando), tomada del
  entorno de la herramienta (`<repo>/.venv/bin`), así las opciones no derivan.

Requiere los repositorios clonados junto a este (`--raiz`, por defecto la carpeta padre)
con su entorno creado (`uv sync`). Las páginas que no salen de un repositorio con README
(gestion, el catálogo, los índices y el ciclo docente). Un repositorio sin CLI
(cyberdeck, p1-tools) sale sólo del README se escriben a mano.

Uso:
    scripts/generar_paginas.py actualizar [--raiz DIR] [PAGINA ...]
    scripts/generar_paginas.py verificar  [--raiz DIR] [PAGINA ...]

PAGINA es la ruta de la página (p. ej. analisis_estatico/ferro.md) o el nombre del repo.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tomllib
import unicodedata
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

MANUAL = Path(__file__).resolve().parent.parent

# página → repositorio (carpeta junto al manual y nombre en ecosistema.toml)
PAGINAS = {
    "autoria/deckard.md": "deckard",
    "autoria/alucard.md": "alucarD",
    "autoria/idkfa.md": "idkfa",
    "autoria/voight.md": "voight",
    "autoria/myst_tools.md": "myst-tools",
    "autoria/scorm_tools.md": "scorm-tools",
    "autoria/tyrell.md": "tyrell",
    "autoria/corbel.md": "corbel",
    "evaluacion/dredd.md": "dredd",
    "evaluacion/weyl.md": "weyl",
    "evaluacion/cyberdeck.md": "cyberdeck",
    "evaluacion/p1_tools.md": "p1-tools",
    "evaluacion/meet_tools.md": "meet-tools",
    "evaluacion/slide_tools.md": "slide-tools",
    "aula/construct.md": "construct",
    "aula/hardboiled.md": "hardboiled",
    "aula/uatu_tools.md": "uatu-tools",
    "diagnostico_avanzado/callahan.md": "callahan",
    "diagnostico_avanzado/dietrich.md": "dietrich",
    "diagnostico_avanzado/tetsuo.md": "tetsuo",
    "diagnostico_avanzado/vasquez.md": "vasquez",
    "diagnostico_avanzado/vassili.md": "vassili",
    "analisis_estatico/brett.md": "brett",
    "analisis_estatico/crowe.md": "crowe",
    "analisis_estatico/drake.md": "drake",
    "analisis_estatico/ferro.md": "ferro",
    "analisis_estatico/giger.md": "giger",
    "analisis_estatico/holden.md": "holden",
    "analisis_estatico/kane.md": "kane",
    "analisis_estatico/motoko.md": "motoko",
    "analisis_estatico/parker.md": "parker",
    "analisis_estatico/rachel.md": "rachel",
    "analisis_estatico/sebastian.md": "sebastian",
    "analisis_estatico/wierzbowski.md": "wierzbowski",
    "analisis_estatico/zhora.md": "zhora",
}

# Secciones del README que no van al manual: navegación propia del README o datos que el sitio
# ya da (el pie lleva el contacto).
SECCIONES_OMITIDAS = re.compile(
    r"^(?:tabla de contenidos?|índice|contenido|contribuir|contribuciones|licencia|agradecimientos|contacto|autor(?:es)?)$",
    re.IGNORECASE)
RE_EMOJI = re.compile(r"[\U0001F000-\U0001FAFF☀-➿️‍]+")
RE_ENLACE = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)\)")
RE_ALERTA = re.compile(r"^> \[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*$")
RE_ARROBA = re.compile(r"(?<![\\\w])@(?=[A-Za-z])")
# Una línea que sólo tiene insignias (shields.io): adorno del README que el sitio no necesita.
RE_INSIGNIAS = re.compile(r"^\s*(?:\[?!\[[^\]]*\]\(https://img\.shields\.io/[^)]*\)(?:\]\([^)]*\))?\s*)+$")
RE_ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
RE_PANEL_COMANDOS = re.compile(r"╭─ (?:Commands|Comandos)\b")
RE_FILA_COMANDO = re.compile(r"^│ ([a-z][a-z0-9-]*)\s")
RE_ARGPARSE_ELECCION = re.compile(r"^  \{([^}]*)\}\s*$")
FUERZAN_TERMINAL = ("GITHUB_ACTIONS", "FORCE_COLOR", "PY_COLORS", "TTY_COMPATIBLE", "TTY_INTERACTIVE")
ENTORNO = {**{k: v for k, v in os.environ.items() if k not in FUERZAN_TERMINAL},
           "NO_COLOR": "1", "TERM": "dumb", "COLUMNS": "100", "LANG": "es_AR.UTF-8"}
ENTORNO.pop("http_proxy", None)
ENTORNO.pop("https_proxy", None)
MAX_PROFUNDIDAD = 2  # herramienta → grupo → subcomando


def manifiesto(raiz: Path) -> dict[str, dict]:
    datos = tomllib.loads((raiz / "p1-tools" / "ecosistema.toml").read_text(encoding="utf-8"))
    return {r["nombre"]: r for r in datos["repo"]}


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True).stdout.strip()


def _fuera_de_codigo(lineas: list[str]):
    """(índice, línea, dentro_de_un_bloque_de_código) para cada línea."""
    cerca = None
    for i, linea in enumerate(lineas):
        m = re.match(r"^\s*(`{3,}|~{3,})", linea)
        if m:
            marca = m.group(1)
            if cerca is None:
                cerca = marca[0] * len(marca)
                yield i, linea, True
                continue
            if marca.startswith(cerca):
                cerca = None
                yield i, linea, True
                continue
        yield i, linea, cerca is not None


def _escapar_arrobas(linea: str) -> str:
    """`@brief` fuera de código es una cita para MyST: se escapa (el código en línea queda igual)."""
    partes = re.split(r"(`+[^`]*`+)", linea)
    return "".join(p if p.startswith("`") else RE_ARROBA.sub(r"\\@", p) for p in partes)


def _enlace_absoluto(destino: str, base_blob: str, base_raw: str, imagen: bool) -> str:
    if destino.startswith("#"):
        return urllib.parse.unquote(destino)
    if re.match(r"^(?:[a-z][a-z0-9+.-]*:|/)", destino, re.IGNORECASE):
        return destino
    destino = destino.removeprefix("./")
    if not base_blob:
        return destino
    return f"{base_raw}/{destino}" if imagen else f"{base_blob}/{destino}"


def adaptar_readme(texto: str, base_blob: str, base_raw: str, prefijo: str) -> tuple[str, str]:
    """(subtítulo, cuerpo MyST) a partir del README."""
    lineas = texto.splitlines()
    titulo = ""
    salida: list[str] = []
    omitiendo = False
    nivel_omitido = 0
    for _, linea, en_codigo in _fuera_de_codigo(lineas):
        if not en_codigo:
            encabezado = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", linea)
            if encabezado:
                nivel = len(encabezado.group(1))
                texto_h = RE_EMOJI.sub("", encabezado.group(2)).strip()
                if nivel == 1 and not titulo:
                    titulo = texto_h
                    continue
                if omitiendo and nivel <= nivel_omitido:
                    omitiendo = False
                if not omitiendo and SECCIONES_OMITIDAS.match(texto_h):
                    omitiendo, nivel_omitido = True, nivel
                    continue
                if not omitiendo:
                    # Bajo el título de la página, los `#` sueltos del README pasan a `##`.
                    salida.append("#" * max(nivel, 2) + " " + texto_h)
                continue
            if omitiendo:
                continue
            # El enlace al MANUAL.md del repo: el manual del sitio ya trae la referencia completa.
            if re.match(r"^>\s*.*\]\((?:\./)?MANUAL\.md\)", linea):
                continue
            if re.match(r"^<!-- (?:p1|corbel):[^>]*-->$", linea.strip()):
                continue
            if RE_INSIGNIAS.match(linea):
                continue
            linea = _escapar_arrobas(linea)
            linea = RE_ENLACE.sub(lambda m: f"{m.group(1)}[{m.group(2)}]"
                                  f"({_enlace_absoluto(m.group(3), base_blob, base_raw, bool(m.group(1)))})", linea)
        elif omitiendo:
            continue
        salida.append(linea)
    cuerpo = _anclas_explicitas(_alertas_a_myst("\n".join(salida)), prefijo)
    cuerpo = re.sub(r"\n{3,}", "\n\n", cuerpo).strip()
    cuerpo = re.sub(r"^(?:---\s*\n+)+", "", cuerpo)  # separador que quedaba debajo del título
    return titulo, cuerpo


def _slug_github(texto: str) -> str:
    texto = re.sub(r"[`*_\[\]()]|<[^>]+>", lambda m: "" if m.group(0) not in "()" else "", texto)
    return re.sub(r"[^\w\- ]", "", texto.strip().lower()).replace(" ", "-")


def _anclas_explicitas(texto: str, prefijo: str) -> str:
    """Los enlaces `#ancla` del README siguen los identificadores de GitHub, que MyST arma distinto
    (los acentos, sobre todo): cada título enlazado recibe una etiqueta MyST y el enlace apunta a ella."""
    lineas = texto.splitlines()
    enlazadas = {m.group(1) for linea in lineas for m in re.finditer(r"\]\(#([^)\s]+)\)", linea)}
    if not enlazadas:
        return texto
    etiquetas: dict[str, str] = {}
    salida: list[str] = []
    for _, linea, en_codigo in _fuera_de_codigo(lineas):
        m = None if en_codigo else re.match(r"^#{2,6}\s+(.*)$", linea)
        if m and (slug := _slug_github(m.group(1))) in enlazadas and slug not in etiquetas:
            ascii_ = unicodedata.normalize("NFKD", slug).encode("ascii", "ignore").decode()
            etiquetas[slug] = f"{prefijo}-" + re.sub(r"-+", "-", ascii_).strip("-")
            salida.append(f"({etiquetas[slug]})=")
        salida.append(linea)
    texto = "\n".join(salida)
    return re.sub(r"\]\(#([^)\s]+)\)", lambda m: f"](#{etiquetas.get(m.group(1), m.group(1))})", texto)


def _alertas_a_myst(texto: str) -> str:
    """`> [!NOTE]` de GitHub → `:::{note}` de MyST."""
    lineas = texto.splitlines()
    salida: list[str] = []
    i = 0
    while i < len(lineas):
        m = RE_ALERTA.match(lineas[i])
        if not m:
            salida.append(lineas[i])
            i += 1
            continue
        tipo = m.group(1).lower()
        i += 1
        cuerpo = []
        while i < len(lineas) and lineas[i].startswith(">"):
            cuerpo.append(lineas[i][1:].removeprefix(" "))
            i += 1
        salida += [f":::{{{tipo}}}", *cuerpo, ":::"]
    return "\n".join(salida)


def ayuda(binario: Path, args: list[str], cwd: Path) -> str:
    try:
        res = subprocess.run([str(binario), *args, "--help"], capture_output=True, text=True, timeout=90,
                             env=ENTORNO, cwd=cwd, stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return ""
    texto = RE_ANSI.sub("", res.stdout or res.stderr)
    return "\n".join(linea.rstrip() for linea in texto.splitlines()).strip("\n")


def subcomandos(texto: str) -> list[str]:
    panel = RE_PANEL_COMANDOS.search(texto)
    if panel:
        nombres = []
        for linea in texto[panel.start():].splitlines()[1:]:
            if linea.startswith("╰"):
                break
            if m := RE_FILA_COMANDO.match(linea):
                nombres.append(m.group(1))
        return nombres
    for linea in texto.splitlines():  # argparse: «  {a,b,c}»
        if m := RE_ARGPARSE_ELECCION.match(linea):
            return [n.strip() for n in m.group(1).split(",") if n.strip()]
    return []


def referencia_cli(repo: Path, ejecutables: list[str]) -> list[str]:
    """Bloques MyST con la ayuda de cada ejecutable y sus subcomandos."""
    bin_dir = repo / ".venv" / "bin"

    def explorar(exe: str, ruta: list[str]) -> list[tuple[list[str], str]]:
        texto = ayuda(bin_dir / exe, ruta, repo)
        res = [(ruta, texto)] if texto else []
        if texto and len(ruta) < MAX_PROFUNDIDAD:
            subs = subcomandos(texto)
            with ThreadPoolExecutor(max_workers=8) as ex:
                for r in ex.map(lambda s: explorar(exe, ruta + [s]), subs):
                    res += r
        return res

    bloques: list[str] = []
    for exe in ejecutables:
        if not (bin_dir / exe).exists():
            raise SystemExit(f"{repo.name}: falta {bin_dir / exe} (¿`uv sync` en el repo?)")
        for ruta, texto in explorar(exe, []):
            comando = " ".join([exe, *ruta])
            bloques.append(f":::{{dropdown}} `{comando}`")
            if not ruta:
                bloques.append(":open:")
            bloques += ["", "```text", texto, "```", ":::", ""]
    return bloques


def _remoto(repo: Path) -> str:
    try:
        return git(repo, "remote", "get-url", "origin").removesuffix(".git")
    except subprocess.CalledProcessError:
        return ""  # sin publicar todavía (cyberdeck)


def pagina(ruta: str, raiz: Path, repos: dict[str, dict]) -> str:
    nombre = PAGINAS[ruta]
    repo_dir = raiz / nombre
    datos = repos.get(nombre, {})
    url = datos.get("url") or _remoto(repo_dir)
    rama = git(repo_dir, "branch", "--show-current") or "main"
    commit = git(repo_dir, "rev-parse", "--short", "HEAD")
    base_blob = f"{url}/blob/{rama}" if url else ""
    base_raw = url.replace("https://github.com/", "https://raw.githubusercontent.com/") + f"/{rama}"
    slug = Path(ruta).stem
    titulo, cuerpo = adaptar_readme((repo_dir / "README.md").read_text(encoding="utf-8"), base_blob, base_raw,
                                    f"manual-{slug}")
    partes = re.split(r"\s+[—–-]\s+", titulo, maxsplit=1)
    subtitulo = partes[1].strip() if len(partes) > 1 else ""
    ruta_pyproject = repo_dir / "pyproject.toml"
    pyproject = tomllib.loads(ruta_pyproject.read_text(encoding="utf-8")) if ruta_pyproject.is_file() else {"project": {}}
    ejecutables = datos.get("ejecutables") or list(pyproject["project"].get("scripts", {}))
    # Los alias de la misma CLI (alucarD: generador-examenes = alucard) se muestran una vez.
    scripts = pyproject["project"].get("scripts", {})
    vistos: dict[str, str] = {}
    for exe in ejecutables:
        vistos.setdefault(scripts.get(exe, exe), exe)
    ejecutables = list(vistos.values())

    lineas = ["---", f'title: "{nombre}"']
    if subtitulo:
        lineas.append(f'subtitle: "{subtitulo}"')
    lineas += ["---", "",
               f"<!-- Generado por scripts/generar_paginas.py desde {nombre}@{commit}: no editar a mano. -->", "",
               f"(manual-{slug})=", f"# {nombre}" + (f" — {subtitulo}" if subtitulo else ""), "",
               *([f"Repositorio: [{url.removeprefix('https://')}]({url}).", ""] if url else []),
               cuerpo, ""]
    if ejecutables:
        lineas += [f"(manual-{slug}-comandos)=", "## Ayuda de los comandos", "",
                   "La ayuda que muestra cada comando (`--help`), tal como la imprime la versión documentada.", ""]
        lineas += referencia_cli(repo_dir, ejecutables)
    origen = f"[`{nombre}@{commit}`]({url}/tree/{commit})" if url else f"`{nombre}@{commit}`"
    lineas += [f"Generado desde {origen}.", ""]
    return "\n".join(lineas)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("accion", choices=["actualizar", "verificar"])
    ap.add_argument("paginas", nargs="*")
    ap.add_argument("--raiz", type=Path, default=MANUAL.parent)
    a = ap.parse_args(argv)
    por_repo = {v: k for k, v in PAGINAS.items()}
    elegidas = [por_repo.get(p, p) for p in a.paginas] or list(PAGINAS)
    desconocidas = [p for p in elegidas if p not in PAGINAS]
    if desconocidas:
        ap.error(f"páginas desconocidas: {', '.join(desconocidas)}")
    repos = manifiesto(a.raiz)
    desactualizadas = []
    for ruta in elegidas:
        nuevo = pagina(ruta, a.raiz, repos)
        destino = MANUAL / ruta
        actual = destino.read_text(encoding="utf-8") if destino.exists() else None
        if actual == nuevo:
            continue
        if a.accion == "actualizar":
            destino.write_text(nuevo, encoding="utf-8")
            print(f"actualizada: {ruta}")
        else:
            desactualizadas.append(ruta)
    for ruta in desactualizadas:
        print(f"desactualizada: {ruta}", file=sys.stderr)
    return 1 if desactualizadas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
