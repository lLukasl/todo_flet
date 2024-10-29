# app.py
import flet as ft
import requests

API_URL = "http://127.0.0.1:8000/api/tasks/"

def main(page: ft.Page):
    page.title = "To-Do List"
    page.padding = 20
    page.scroll = "auto"
    page.theme_mode = ft.ThemeMode.LIGHT

    # Definindo cores
    primary_color = ft.colors.PURPLE_500
    accent_color = ft.colors.PURPLE_100

    task_input = ft.TextField(
        label="New Task",
        width=400,
        border_radius=8,
        content_padding=10,
        filled=True,
        bgcolor=ft.colors.WHITE,
    )
    
    task_list = ft.Column(spacing=10, expand=True)

    def load_tasks():
        response = requests.get(API_URL)
        if response.status_code == 200:
            task_list.controls.clear()
            for task in response.json():
                # Definindo o estilo da tarefa com base no status
                title_text = ft.Text(
                    value=task["title"],
                    size=16,
                    color=ft.colors.GREY if task["completed"] else ft.colors.BLACK,
                    weight=ft.FontWeight.W_300 if task["completed"] else ft.FontWeight.NORMAL,
                )
                
                def enable_editing(e):
                    task_input.value = task["title"]
                    task_input.focus()
                    task_input.update()
                    page.update()

                # Criando uma linha para cada tarefa com alinhamento dos ícones
                task_item = ft.Row(
                    controls=[
                        ft.Checkbox(
                            value=task["completed"],
                            on_change=lambda e, task_id=task["id"]: update_task_status(e, task_id),
                        ),
                        ft.Container(
                            content=title_text,
                            expand=True,
                            bgcolor=ft.colors.WHITE,
                            padding=8,
                            border_radius=5,
                        ),
                        ft.IconButton(
                            icon=ft.icons.EDIT,
                            icon_size=20,
                            tooltip="Edit",
                            on_click=enable_editing,
                            icon_color=primary_color,
                        ),
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            icon_size=20,
                            tooltip="Delete",
                            on_click=lambda e, task_id=task["id"]: delete_task(task_id),
                            icon_color=primary_color,
                        ),
                    ],
                    alignment="spaceBetween",
                    vertical_alignment="center",
                )
                task_list.controls.append(task_item)
            page.update()

    def add_task(e):
        task_title = task_input.value
        if task_title:
            response = requests.post(API_URL, json={"title": task_title, "completed": False})
            if response.status_code == 201:
                load_tasks()
                task_input.value = ""
                page.update()

    def update_task_status(e, task_id):
        response = requests.put(
            f"{API_URL}{task_id}/", json={"completed": e.control.value}
        )
        if response.status_code == 200:
            load_tasks()

    def delete_task(task_id):
        response = requests.delete(f"{API_URL}{task_id}/")
        if response.status_code == 204:
            load_tasks()

    def save_edited_task(e, task_id):
        new_title = task_input.value
        response = requests.put(f"{API_URL}{task_id}/", json={"title": new_title})
        if response.status_code == 200:
            load_tasks()

    page.add(
        ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("To-Do List", style="headlineMedium", color=primary_color),
                            task_input,
                            ft.ElevatedButton(
                                "Add Task",
                                icon=ft.icons.ADD,
                                on_click=add_task,
                                bgcolor=primary_color,
                                color=ft.colors.WHITE,
                                width=200,
                                height=45,
                            ),
                            ft.Divider(height=20, thickness=1),
                            task_list,
                        ],
                        spacing=10,
                        horizontal_alignment="center",
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                    padding=20,
                    border_radius=8,
                    bgcolor=accent_color,
                )
            ],
            alignment="center",
        ),
    )

    load_tasks()

if __name__ == "__main__":
    ft.app(target=main)
