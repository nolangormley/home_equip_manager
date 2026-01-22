# Home Equipment Manager

A Django-based application for managing home equipment, tracking maintenance tasks, and logging updates. Features a Kanban board for task management and a modern, dark-themed UI.

## Features

*   **Equipment Management**: Track equipment with details like location, purchase date, and images.
*   **Task Tracking**: Manage maintenance tasks with due dates and completion status.
*   **Kanban Board**: Drag-and-drop interface for managing tasks across "To Do", "In Progress", and "Done" states.
*   **Activity Logging**: Log updates and notes for each piece of equipment.
*   **Modern UI**: Responsive dark mode design with real-time updates using HTMX.

## Technology Stack

*   **Backend**: Python, Django 4.2
*   **Frontend**: HTML5, CSS3, HTMX, SortableJS
*   **Database**: SQLite (default)

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd home_equip_manager
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations**:
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser** (optional, for admin access):
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server**:
    ```bash
    python manage.py runserver
    ```

    Access the application at `http://127.0.0.1:8000/`.

## Usage

*   **Dashboard**: View all your equipment. Click "Add Equipment" to register new items.
*   **Equipment Detail**: Click on an item to view its details, add tasks, or log updates.
*   **Kanban Board**: Click "Task Board" in the header to view and manage all tasks visually. Drag cards to update their status.
