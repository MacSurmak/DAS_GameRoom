from aiogram_dialog.widgets.kbd import Group, ListGroup, Button
from aiogram_dialog.widgets.text import Format

from services import save_lang

def create_language_buttons():
    return Group(
            ListGroup(
                Button(
                    text = Format("{item[name]}"),
                    id = "lang_button",
                    on_click = lambda callback, button, manager: save_lang(
                        callback,
                        button,
                        manager,
                        session=manager.middleware_data["session"]
                    ),
                ),
                id="langs_list_group",
                item_id_getter=lambda item: item["code"],
                items="languages"
            ),
            width = 3
        )
