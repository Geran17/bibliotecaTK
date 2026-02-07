from tkinter import Menu


class ContextMenuFactory:
    """Crea y vincula menús contextuales para widgets con selección por clic derecho."""

    @staticmethod
    def build_for_treeview(master, treeview, actions, select_row=True):
        menu = Menu(master, tearoff=0)

        for action in actions:
            if action.get("separator"):
                menu.add_separator()
                continue
            menu.add_command(label=action["label"], command=action["command"])

        def _on_right_click(event):
            if select_row:
                item_id = treeview.identify_row(event.y)
                if item_id:
                    treeview.selection_set(item_id)
                    treeview.focus(item_id)
            menu.tk_popup(event.x_root, event.y_root)

        treeview.bind("<Button-3>", _on_right_click)
        return menu
