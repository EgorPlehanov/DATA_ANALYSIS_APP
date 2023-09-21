import flet as ft
from flet import (
    Page,
    UserControl,
    Row,
    Text,
    IconButton,
    Container,
    Column,
    icons,
    colors
)



class TabsBar(Row):
    def __init__(self, app_layout, page: Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_layout = app_layout
        self.page = page
        self.tabs = [
            CastomTab(self.page)
        ]
        self.tabs_button = Row(
            controls=[
                IconButton(
                    icon="delete",
                )
            ]
        )
        self.controls = [self.tabs, self.tabs_button]

    
    def add_tab(self, tab):
        self.controls.append(tab)
        return self
    
    def remove_tab(self, tab):
        self.controls.remove(tab)
        return self