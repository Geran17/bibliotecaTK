from ttkbootstrap import Frame, Label
from ttkbootstrap.constants import EW
from views.components.ui_tokens import PADDING_COMPACT, PADDING_PANEL


class BaseFormFrame(Frame):
    """Formulario compacto con grilla adaptable para campos simples."""

    def __init__(self, master=None, columns=2, label_width=14, **kwargs):
        super().__init__(master, **kwargs)
        self.columns = max(1, int(columns))
        self.label_width = label_width
        self._index = 0

        for col in range(self.columns * 2):
            self.columnconfigure(col, weight=1 if col % 2 == 1 else 0)

    def add_labeled_widget(
        self,
        label_text,
        widget,
        row=None,
        column=None,
        sticky=EW,
        widget_columnspan=1,
    ):
        if row is None or column is None:
            row = self._index // self.columns
            column = self._index % self.columns

        label_col = column * 2
        widget_col = label_col + 1

        lbl = Label(self, text=label_text, anchor="w", width=self.label_width)
        lbl.grid(
            row=row,
            column=label_col,
            padx=(PADDING_COMPACT, PADDING_PANEL),
            pady=PADDING_COMPACT,
            sticky="w",
        )
        widget.grid(
            row=row,
            column=widget_col,
            columnspan=widget_columnspan,
            padx=(0, PADDING_PANEL * 2),
            pady=PADDING_COMPACT,
            sticky=sticky,
        )

        self._index += 1
        return lbl, widget
