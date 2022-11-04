import sqlite3


def under(stroke):
    return f'<sub>{str(stroke)}</sub>'


def up(stroke):
    return f'<sup>{str(stroke)}</sup>'


def elem_parameters(name):
    connection = sqlite3.connect('Theory.db')
    a = connection.cursor().execute("""SELECT * FROM elements WHERE symbol = ?""", (name,)).fetchone()
    connection.commit()
    return a