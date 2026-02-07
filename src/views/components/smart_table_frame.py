from ttkbootstrap import Frame, Entry, Combobox, Button, StringVar, Label
from ttkbootstrap.constants import BOTH, LEFT, READONLY, TOP, X, PRIMARY
from ttkbootstrap.tableview import Tableview
from views.components.ui_tokens import PADDING_COMPACT, PADDING_PANEL


class SmartTableFrame(Frame):
    """Tabla reusable con barra de búsqueda y estado."""

    def __init__(
        self,
        master=None,
        coldata=None,
        search_fields=None,
        on_search=None,
        on_refresh=None,
        show_refresh=False,
        var_buscar=None,
        bootstyle=PRIMARY,
        paginated=False,
        searchable=False,
        autofit=True,
        **kwargs,
    ):
        super().__init__(master, **kwargs)

        self.coldata = coldata or []
        self.search_fields = search_fields or []
        self.on_search = on_search
        self.on_refresh = on_refresh
        self.var_buscar = var_buscar or StringVar()

        self.ent_buscar = None
        self.cbx_campos = None
        self.btn_buscar = None
        self.btn_refrescar = None
        self.lbl_estado = None
        self.table_view = None

        self._crear_widgets(
            bootstyle=bootstyle,
            paginated=paginated,
            searchable=searchable,
            autofit=autofit,
            show_refresh=show_refresh,
        )

    def _crear_widgets(self, bootstyle, paginated, searchable, autofit, show_refresh):
        toolbar = Frame(self)
        toolbar.pack(
            side=TOP,
            fill=X,
            padx=PADDING_PANEL,
            pady=(PADDING_COMPACT, PADDING_PANEL),
        )

        self.ent_buscar = Entry(toolbar, textvariable=self.var_buscar)
        self.ent_buscar.pack(side=LEFT, fill=X, expand=True, padx=(0, PADDING_PANEL))
        self.ent_buscar.bind("<Return>", self._on_search_event)

        if self.search_fields:
            self.cbx_campos = Combobox(toolbar, values=self.search_fields, state=READONLY, width=14)
            self.cbx_campos.current(0)
            self.cbx_campos.pack(side=LEFT, padx=(0, PADDING_PANEL))

        self.btn_buscar = Button(toolbar, text="Buscar", command=self._on_search_click, style="primary")
        self.btn_buscar.pack(side=LEFT)

        if show_refresh:
            self.btn_refrescar = Button(
                toolbar,
                text="Refrescar",
                command=self._on_refresh_click,
                style="secondary-toolbutton",
            )
            self.btn_refrescar.pack(side=LEFT, padx=(PADDING_PANEL, 0))

        self.table_view = Tableview(
            master=self,
            coldata=self.coldata,
            paginated=paginated,
            searchable=searchable,
            autofit=autofit,
            bootstyle=bootstyle,
        )
        self.table_view.pack(side=TOP, fill=BOTH, expand=True, padx=PADDING_COMPACT, pady=PADDING_COMPACT)

        self.lbl_estado = Label(self, text="")
        self.lbl_estado.pack(
            side=TOP,
            fill=X,
            padx=PADDING_PANEL,
            pady=(PADDING_COMPACT, 0),
        )

    def _on_search_event(self, _event):
        self._on_search_click()

    def _on_search_click(self):
        if callable(self.on_search):
            self.on_search()

    def _on_refresh_click(self):
        if callable(self.on_refresh):
            self.on_refresh()

    def set_estado(self, texto):
        self.lbl_estado.config(text=texto)

    def get_campo_busqueda(self):
        if self.cbx_campos:
            return self.cbx_campos.get()
        return ""

    def get_termino_busqueda(self):
        return self.var_buscar.get().strip()
