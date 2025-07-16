from config import *

class DB:
    conn = None
    cursor = None

    @classmethod
    def connect(cls, db_name):
        try:
            cls.conn = sqlite3.connect(db_name)
            cls.cursor = cls.conn.cursor()
        except sqlite3.Error as e:
            Messagebox.show_error(f"Failed to connect to database: {e}")

    @classmethod
    def insert(cls, table, columns, values, commit=True):
        """Insert a new row into the database."""
        col = ", ".join(columns)
        placeholders = ", ".join(["?" for _ in values])
        query = f'INSERT INTO {table} ({col}) VALUES ({placeholders});'
        try:
            cls.cursor.execute(query, tuple(values))
            if commit:
                cls.conn.commit()
            return True
        except sqlite3.Error as error:
            Messagebox.show_error(f"The process couldn't be completed by the system: {error}")
            return False

    @classmethod
    def select(cls, table, columns, conditions="", values=()):
        """Get data from the database."""
        col = ", ".join(columns)
        query = f"SELECT {col} FROM {table}"
        if conditions:
            query += " WHERE " + conditions
        try:
            cls.cursor.execute(query + ";", tuple(values))
            return [list(record) for record in cls.cursor.fetchall()]
        except sqlite3.Error as error:
            Messagebox.show_error(f"The process couldn't be completed by the system: {error}")
            return []

    @classmethod
    def update(cls, table, columns, conditions, values, commit=True):
        """Update records in the database that meet the conditions."""
        col_set = ", ".join([f"{column}=?" for column in columns])
        query = f"UPDATE {table} SET {col_set} WHERE {conditions};"
        try:
            cls.cursor.execute(query, tuple(values))
            if commit:
                cls.conn.commit()
            return True
        except sqlite3.Error as error:
            Messagebox.show_error(f"The process couldn't be completed by the system: {error}")
            return False

    @classmethod
    def delete(cls, table, conditions, values=(), commit=True):
        """Delete records from the database that meet the conditions."""
        query = f"DELETE FROM {table}"
        if conditions:
            query += " WHERE " + conditions
        query += ";"
        try:
            cls.cursor.execute(query, tuple(values))
            if commit:
                cls.conn.commit()
            return True
        except sqlite3.Error as error:
            Messagebox.show_error(f"The process couldn't be completed by the system: {error}")
            return False

    @classmethod
    def close(cls):
        """Close the database connection."""
        try:
            if cls.conn:
                cls.conn.close()
        except Exception:
            pass
