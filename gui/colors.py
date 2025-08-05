# gui/colors.py

class _ThemeState:
    def __init__(self):
        self.color_base = "azul"  # verde, azul, rojo, naranja
        self.modo = "oscuro"       # oscuro / claro
        self._refresh()

    def _refresh(self):
        # bases
        base_paletas = {
            "verde": {"principal": "#1DB954", "hover": "#1AA34A"},
            "azul": {"principal": "#007ACC", "hover": "#005F99"},
            "rojo": {"principal": "#E22134", "hover": "#B71C2B"},
            "naranja": {"principal": "#FF6F00", "hover": "#E65C00"},
        }
        base = base_paletas.get(self.color_base, base_paletas["verde"])
        if self.modo == "oscuro":
            self.COLOR_FONDO = "#121212"
            self.COLOR_FONDO_SECUNDARIO = "#181818"
            self.COLOR_TEXTO_CLARO = "#FFFFFF"
            self.COLOR_TEXTO_SECUNDARIO = "#B3B3B3"
            self.COLOR_BORDE = base["principal"]
            self.COLOR_BORDE_SUAVE = "#2A2A2A"
            self.COLOR_GRIS_OSCURO = "#1A1A1A"
        else:
            self.COLOR_FONDO = "#FFFFFF"
            self.COLOR_FONDO_SECUNDARIO = "#F0F0F0"
            self.COLOR_TEXTO_CLARO = "#000000"
            self.COLOR_TEXTO_SECUNDARIO = "#666666"
            self.COLOR_BORDE = base["principal"]
            self.COLOR_BORDE_SUAVE = "#CCCCCC"
            self.COLOR_GRIS_OSCURO = "#DDDDDD"

        self.COLOR_PRINCIPAL = base["principal"]
        self.COLOR_HOVER = base["hover"]

# estado global único
_theme = _ThemeState()

# "alias" exportados que los frames usan directamente
def set_theme(color_base=None, modo=None):
    if color_base:
        _theme.color_base = color_base
    if modo:
        _theme.modo = modo
    _theme._refresh()

# nombres que usaban antes (se mantienen, se actualizan dinámicamente)
COLOR_FONDO = lambda: _theme.COLOR_FONDO
COLOR_FONDO_SECUNDARIO = lambda: _theme.COLOR_FONDO_SECUNDARIO
COLOR_TEXTO_CLARO = lambda: _theme.COLOR_TEXTO_CLARO
COLOR_TEXTO_SECUNDARIO = lambda: _theme.COLOR_TEXTO_SECUNDARIO
COLOR_BORDE = lambda: _theme.COLOR_BORDE
COLOR_BORDE_SUAVE = lambda: _theme.COLOR_BORDE_SUAVE
COLOR_PRINCIPAL = lambda: _theme.COLOR_PRINCIPAL  # para compatibilidad con ese nombre
COLOR_HOVER = lambda: _theme.COLOR_HOVER
COLOR_GRIS_OSCURO = lambda: _theme.COLOR_GRIS_OSCURO
