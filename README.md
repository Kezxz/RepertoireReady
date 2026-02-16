# RepertoireReady
*RepertoireReady* is a music-focused repertoire and performance planning tool designed to help musicians organize their library of pieces and build setlists based on what is performance-ready. The long-term goal of this project is to support real musical workflows by tracking repertoire readiness, organizing pieces by musical attributes, and planning performances more effectively than generic task managers or spreadsheets.

# Sprint 2 Scope 
For the second sprint, we focued on testing and simplifying the structure of the project.

**Deliverables:**
- Codebase Simplification
    - shifted *main.py* to menus and load/save only
    - moved all CLI actions to *services.py*
    - centralized CSV persistence in *storage.py*
- Packaging and Imports
    - made *app/* a package (*app/__init__.py*)
    - test imports via this package for consistency across machines
- Automated tests
    - *test_piece_logic.py:* add/edit/delete behaviors and timestamps
    - *test_setlist_logic.py:* add/remove with correct ordering and empty-view output
    - *test_storage.py:* round-trip save/load for pieces and setlists
    - *smoke_test.py:* end-to-end flow test
- Repo Hygiene 
    - updated *.gitignore*
    - moved all test scripts to *tests/* folder

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

# How to Run
From the root folder, run: python app/main.py

# How to Run Tests
From the root folder, run:
python -m pytest -q
*if there's a module mismatch issue, run:* py -3.13 -m pytest (use your installed version)

# Notes
This repository is intended to be built incrementally through multiple sprints. Features such as performance events, user accounts, and a full UI are planned for future sprints after the core functionality is complete.