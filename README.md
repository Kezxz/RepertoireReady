# RepertoireReady
*RepertoireReady* is a music-focused repertoire and performance planning tool designed to help musicians organize their library of pieces and build setlists based on what is performance-ready. The long-term goal of this project is to support real musical workflows by tracking repertoire readiness, organizing pieces by musical attributes, and planning performances more effectively than generic task managers or spreadsheets.

# Sprint 2 Scope 
For the third sprint, the goal is to start a simple web-based UI using Flask.

**Deliverables:**
- Web UI base layer
    - added a *web/* layer with an app initialization and a run script
    - added placeholder route modules for pieces and setlists
    - added basic template structure
- Read-only web pages
    - */pieces* will display the current piece library
    - */setlists* will display the current setlist library
- Web UI base layer
    - added a *web/* layer with an app initialization and a run script
    - added placeholder route modules for pieces and setlists
    - added basic template structure
- Read-only web pages
    - */pieces* will display the current piece library
    - */setlists* will display the current setlist library
- Differentiate between Setlists and Performances
    - - Web UI base layer
    - added a *web/* layer with an app initialization and a run script
    - added placeholder route modules for pieces and setlists
    - added basic template structure
- Read-only web pages
    - */pieces* will display the current piece library
    - */setlists* will display the current setlist library
- Stretch Goals
    - Differentiate between Setlists and Performances
        - a **Setlist** is a reusable template (title/ordered pieces), while a **Performance** is a specific instance of a setlist (date/location/venue and which setlist it uses)
        - split code of *setlist_logic.py* between it and a new *performance_logic*?
        - new .cvs *(performance_library.csv)*?
        - update *storage.py* to include performances?
    - write *web/pieces_form.html*
        - create a new piece
        - edit an existing piece
    -write *web/setlist_form.html*
        - create a new setlist
        - edit an existing setlist
    - add new html scripts for *piece_detail* and *setlist_detail*

# File Descriptions
- *main.py*
    - entry point for terminal application, handles the main menu and user interaction
- *piece_logic.py*
    - implements all repertoire-related functionality
- *setlist_logic.py*
    - implements all setlist-related functionality
- *storage.py*
    - handles saving and loading data for pieces and setlists
- *services.py*
    - houses the CLI actions for pieces and setlists
- *data/*
    - stores persistence files in .csv format
- *tests/*
    - automated tests
- *web/*
    - Flask-based web UI layer

# Setup/Install Requirements
This project uses a virtual environment (.venv). From the root folder, run:
py -m venv .venv      
.\.venv\Scripts\activate

Then, install dependencies:
pip install -r requirements.txt

# How to Run Web UI via Flask
From the root folder, run:
python -m web.run

# How to Run CLI
From the root folder, run: python app/main.py

# How to Run Tests
From the root folder, run:
python -m pytest -q
*if there's a Python interpreter mismatch issue on Windows, run:* py -3.13 -m pytest (use your installed version)

# Notes
This repository is intended to be built incrementally through multiple sprints. Features such as performance events, user accounts, and a full UI are planned for future sprints after the core functionality is complete.