import flet as ft
from flet import (
    Page,
    UserControl,
    Container,
    Row,
    AppBar,
    FilledButton,
    IconButton,
    icons,
    Text,
    TextField,
    Tabs,
    Tab,
    Icon,
    colors,
    AlertDialog,
    TextButton,
    MainAxisAlignment,
    border,
    Ref,
)
from graphic_area import GraphicArea


class DataAnalysisApp(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.expand = True

        self.appbar = self.create_appbar()
        self.page.appbar = self.appbar

        self.dlg_modal_add_tab = AlertDialog(
            modal=True,
            title=Text("Добавить вкладку"),
            content=TextField(label="Название вкладки", autofocus=True, on_submit=self.add_tab),
            actions = [
                TextButton("Добавить", on_click=self.add_tab),
                TextButton("Отмена", on_click=self.close_dlg)
            ],
            actions_alignment=MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.tabs_bar = Tabs(animation_duration=200)

        # ВРЕМЕННОЕ ПРЕДСТАВЛЕНИЕ ВКЛАДКИ РАБОТЫ С ИЗОБРАЖЕНИЯМИ ->
        self.image_area = Row(
            controls=[
                Container(
                    border=border.all(colors.RED),
                    content=Row(
                        controls=[
                            ft.ListView(
                                controls=[
                                    Text('Область для работы с изображениями'),
                                    Text('Область для работы с изображениями'),
                                ]
                            ),
                            ft.ListView(
                                controls=[
                                    Text('Область для работы с изображениями'),
                                ]
                            )
                        ]
                    )
                )
            ]
        )


    def build(self) -> Tabs:
        '''
        Строит вкладки и возвращает панель вкладок.

        :return: Экземпляр класса Tabs, представляющий панель вкладок.
        :rtype: Tabs
        '''
        return self.tabs_bar
    

    def create_appbar(self) -> AppBar:
        '''
        Создает и возвращает экземпляр класса AppBar.
        '''
        appbar_actions = [
            Container(
                content=Row(
                    controls=[
                        FilledButton(
                            text="График", icon="add", data="Graphic",
                            on_click=self.open_dlg_modal
                        ),
                        FilledButton(
                            text="Изображение", icon="add", data="Image",
                            on_click=self.open_dlg_modal
                        ),
                    ],
                ),
                margin=10
            )
        ]
        appbar = AppBar(
            leading=Icon(icons.ANALYTICS),
            leading_width=40,
            title=Text(value="Data Analysis App", text_align="start"),
            center_title=False,
            bgcolor=colors.SURFACE_VARIANT,
            actions=appbar_actions,
        )
        return appbar


    def add_tab(self, e) -> None:
        '''
        Добавляет вкладку в список вкладок tabs_bar
        '''
        # Определяем тип вкладки на основе данных из диалогового окна
        tab_type = self.dlg_modal_add_tab.data

        # Значения по умолчанию для значков и виджета содержимого вкладки
        tab_icon = "question_mark"
        tab_content_widget = None

        # Определяем значок и виджет содержимого вкладки на основе типа
        match tab_type:
            case "Graphic":
                tab_icon = "area_chart"
                tab_content_widget = GraphicArea(self, self.page)
            case "Image":
                tab_icon = "image"
                tab_content_widget = self.image_area
        
        # Определяем заголовок вкладки, используя введенное пользователем значение или значение по умолчанию
        tab_title = self.dlg_modal_add_tab.content.value
        if not tab_title:
            tab_title = 'Вкладка ' + tab_type
        
        # Создаем ссылку на вкладку и создаем объект вкладки
        tab_ref = Ref[Tab]()
        tab = Tab(
            ref=tab_ref,
            tab_content=Row(
                controls=[
                    Icon(name=tab_icon),
                    Text(value=tab_title),
                    IconButton(icon=icons.CLOSE, data=tab_ref, on_click=self.delete_tab),
                ]
            ),
            content=tab_content_widget
        )

        # Добавляем вкладку в список вкладок и выбираем ее
        self.tabs_bar.tabs.append(tab)
        self.tabs_bar.selected_index = len(self.tabs_bar.tabs) - 1

        self.close_dlg(self)
    

    def delete_tab(self, e) -> None:
        '''
        Удаляет вкладку
        '''
        deleted_tab = e.control.data.current
        self.tabs_bar.tabs.remove(deleted_tab)
        self.update()


    def open_dlg_modal(self, e) -> None:
        '''
        Открывает диалоговое окно для добавления вкладки
        '''
        button_name = e.control.data
        match button_name:
            case "Graphic":
                self.dlg_modal_add_tab.title.value = "Добавить график"
            case "Image":
                self.dlg_modal_add_tab.title.value = "Добавить изображение"
            case _:
                self.dlg_modal_add_tab.title.value = "Добавить вкладку"
        
        self.dlg_modal_add_tab.data = button_name
        self.page.dialog = self.dlg_modal_add_tab
        self.dlg_modal_add_tab.open = True
        self.page.update()


    def close_dlg(self, e) -> None:
        '''
        Закрывает диалоговое окно для добавления вкладки
        '''
        self.dlg_modal_add_tab.open = False
        self.dlg_modal_add_tab.data = ''
        self.dlg_modal_add_tab.content.value = ''
        self.page.update()
        self.update()



def main(page: Page):
    page.title = "Data Analysis App"
    page.padding = 0
    # page.bgcolor = colors.BLUE_200
    app = DataAnalysisApp(page)
    page.add(app)
    page.update()

ft.app(target=main)#, view=ft.AppView.WEB_BROWSER)


# ===================================
# |        ЗАПУСК ПРИЛОЖЕНИЯ        |
# ===================================

# .venv\Scripts\activate
# flet run .\my-app\src\main.py -d

# ===================================
