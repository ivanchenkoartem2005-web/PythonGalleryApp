# PythonGalleryApp
Simple Gallery App made in Python
# Art Gallery Manager

A simple desktop application built with Python and Tkinter to manage an art gallery collection.

## Features
- Add new artwork with title, artist, creation year, and price.
- View all artworks in a table.
- Search artworks by title.
- Update artwork prices.
- Mark artworks as sold.
- Automatically record the sale date.
- Delete artworks from the gallery.
- View gallery statistics, including total artworks, sold artworks, available artworks, total gallery value, and highest artwork price.
- Save gallery information locally using JSON.

## Technologies Used
- Python 3
- Tkinter
- JSON
- OS module
- Datetime module

## How to Run
1. Make sure Python 3 is installed.
2. Clone or download this repository.
3. Open a terminal in the project folder.
4. Run the application:

```bash
python main.py
```

On some systems, use:
```bash
python3 main.py
```

## Project Structure
```text
Art-Gallery-Manager/
│
├── app.py
├── README.md
├── .gitignore
└── gallery.json (created automatically)
```

## Data Storage
Artwork information is stored locally in a JSON file named `gallery.json`.
This file is excluded from Git using `.gitignore` to prevent personal gallery data from being uploaded accidentally.

## Notes
- Artwork titles must be unique.
- The application is designed for local desktop use.
- No additional Python packages are required beyond the standard library and Tkinter.

## Author
Created as a Python desktop application project.
If you find this project useful, feel free to star the repository!
