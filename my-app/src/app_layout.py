from flet import (
    Row,
    Page,
    Column,
    Text,
    UserControl
)

# from tabs_bar import TabsBar


class AppLayout(Row):
    def __init__(self, app, page: Page, tabs, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.page = page
        self.tabs = tabs
        # self.tabs_bar = TabsBar(self, self.page)

        self.controls = [
            self.tabs
        ]

