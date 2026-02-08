# RepertoireReady
*RepertoireReady* is a music-focused repertoire and performance planning tool designed to help musicians organize their library of pieces and build setlists based on what is performance-ready. The long-term goal of this project is to support real musical workflows by tracking repertoire readiness, organizing pieces by musical attributes, and planning performances more effectively than generic task managers or spreadsheets.

# Sprint 1 Scope 
For the first sprint, this project will be developed as a terminal-based MVP to establish the core data model and functionality before implementing a full UI.
The goals are to implement the following features:
- Repertoire management
    - Users can add, view, edit, and delete pieces
- Setlist management
    - Users can create setlists and attach pieces to them
- Readiness tracking and filtering
    - Pieces can be tracked as learning/rehearsing/performance-ready and filtered by other attributes
- Persistence
    - Save/load piece and setlist data using simple .csv format
- Piece detail (stretch goal)
    - Users can select a piece and view a 'detail screen' that includes notes and other info associated with the piece
- Setlist ordering (stretch goal)
    - Users can reorder setlists (move up/down) and the change is automatically saved

# File Descriptions
*main.py*
    - entry point for terminal application, handles the main menu and user interaction
*models.py*
    - defines the core data structure used in the program
*piece_logic.py*
    - implements all repertoire-related functionality
*setlist_logic.py*
    - implements all setlist-related functionality
*storage.py*
    - handles saving and loading data for pieces and setlists
*data/*
    - stores persistence files in .csv format

# How to Run
From the root folder, just run: python app/main.py

# Notes
This repository is intended to be built incrementally through multiple sprints. Features such as performance events, user accounts, and a full UI are planned for future sprints after the core functionality is complete.