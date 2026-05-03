import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ========== DATABASE CONFIG ==========
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'ecommerce_db')
}

# ========== TABLE METADATA ==========
TABLES = {
    'users': ['user_id','username','full_name','email','phone','role'],
    'products': ['product_id','name','category','price','stock'],
    'orders': ['order_id','user_id','order_date','status'],
    'order_items': ['item_id','order_id','product_id','quantity'],
    'payments': ['payment_id','order_id','amount','method','status','paid_at']
}

# ========== DATABASE CLASS ==========
class DB:
    def __init__(self, cfg):
        self.cfg = cfg
        self.conn = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**self.cfg)
        except Error as e:
            messagebox.showerror('DB Error', str(e))
            raise

    def query(self, sql, params=None, commit=False):
        cur = self.conn.cursor(dictionary=True)
        cur.execute(sql, params or ())
        if commit:
            self.conn.commit()
            last = cur.lastrowid
            cur.close()
            return last
        rows = cur.fetchall()
        cur.close()
        return rows

    def close(self):
        if self.conn:
            self.conn.close()

# ========== SQL HELPERS ==========
def build_select_all(table):
    return f"SELECT * FROM {table} ORDER BY 1 LIMIT 200"

def build_insert_sql(table, cols):
    cols_no_id = cols[1:]
    cols_list = ','.join(cols_no_id)
    placeholders = ','.join(['%s'] * len(cols_no_id))
    return f"INSERT INTO {table} ({cols_list}) VALUES ({placeholders})", cols_no_id

def build_update_sql(table, cols):
    cols_no_id = cols[1:]
    set_clause = ','.join([f"{c}=%s" for c in cols_no_id])
    return f"UPDATE {table} SET {set_clause} WHERE {cols[0]}=%s", cols_no_id

def build_delete_sql(table, idcol):
    return f"DELETE FROM {table} WHERE {idcol}=%s"

# ========== MAIN APP CLASS ==========
class ModernApp(ttk.Frame):
    def __init__(self, root, db):
        super().__init__(root)
        self.root = root
        self.db = db
        self.root.title("E-COMMERCE MANAGEMENT SYSTEM")
        self.root.geometry("1200x700")
        self.pack(fill='both', expand=True)

        self.style_ui()

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill='both', expand=True, padx=10, pady=10)

        for table, cols in TABLES.items():
            self.create_table_tab(table, cols)

    # ---------- Styling ----------
    def style_ui(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('TNotebook.Tab', font=('Segoe UI', 11, 'bold'), padding=[12, 6])
        style.configure('Treeview', background='#eef6f9', rowheight=25, font=('Consolas', 10))
        style.configure('Treeview.Heading', font=('Segoe UI Semibold', 11))

        style.map("Treeview",
                  background=[('selected', '#0f6cbf')],
                  foreground=[('selected', 'white')])

        style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=6)

        self.root.configure(bg='#eaf3f6')

    # ---------- Table Tab ----------
    def create_table_tab(self, table, cols):
        frame = ttk.Frame(self.nb)
        frame.pack(fill='both', expand=True)
        self.nb.add(frame, text=table)

        # TOP BAR
        top = ttk.Frame(frame)
        top.pack(side='top', fill='x', pady=6)

        ttk.Label(top, text=f"Table: {table}",
                  font=('Segoe UI', 12, 'bold')).pack(side='left', padx=10)

        ttk.Button(top, text="🔄 Refresh",
                   command=lambda t=table: self.refresh_data(t)).pack(side='right', padx=5)

        ttk.Button(top, text="➕ Add New",
                   command=lambda t=table: self.open_edit_window(t, cols)).pack(side='right', padx=5)

        # TABLE
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)

        tree = ttk.Treeview(tree_frame, columns=cols, show='headings', selectmode='browse')

        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor='center')

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)

        tree.configure(yscroll=vsb.set, xscroll=hsb.set)

        tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # BOTTOM BUTTONS
        bottom = ttk.Frame(frame)
        bottom.pack(side='bottom', fill='x', pady=10)

        ttk.Button(bottom, text='✏️ Edit',
                   command=lambda t=table, c=cols, tr=tree: self.edit_selected(t, c, tr)).pack(side='left', padx=5)

        ttk.Button(bottom, text='🗑 Delete',
                   command=lambda t=table, tr=tree: self.delete_selected(t, tr)).pack(side='left', padx=5)

        frame.tree = tree
        self.refresh_data(table)

    # ---------- Refresh ----------
    def refresh_data(self, table):
        frame = self.get_frame(table)
        tree = frame.tree

        for i in tree.get_children():
            tree.delete(i)

        rows = self.db.query(build_select_all(table))

        for r in rows:
            vals = [r[c] for c in TABLES[table]]
            tree.insert('', 'end', values=vals)

    # ---------- Get Frame ----------
    def get_frame(self, table):
        for f in self.nb.winfo_children():
            if self.nb.tab(f, "text") == table:
                return f

    # ---------- Edit ----------
    def edit_selected(self, table, cols, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showinfo('Select', 'Select a record')
            return

        item = tree.item(selected[0])
        self.open_edit_window(table, cols, existing=item['values'])

    # ---------- Delete ----------
    def delete_selected(self, table, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showinfo('Select', 'Select a record')
            return

        item = tree.item(selected[0])
        idval = item['values'][0]
        idcol = TABLES[table][0]

        if messagebox.askyesno('Confirm', 'Delete this record?'):
            self.db.query(build_delete_sql(table, idcol), (idval,), commit=True)
            self.refresh_data(table)

    # ---------- Edit Window ----------
    def open_edit_window(self, table, cols, existing=None):
        win = tk.Toplevel(self.root)
        win.title(f"{table} Form")
        win.geometry("450x500")

        entries = {}

        for i, col in enumerate(cols):
            ttk.Label(win, text=col).grid(row=i, column=0, padx=10, pady=5)
            ent = ttk.Entry(win, width=40)
            ent.grid(row=i, column=1, padx=10, pady=5)
            entries[col] = ent

            if i == 0:
                ent.config(state='readonly')

        if existing:
            for c, v in zip(cols, existing):
                entries[c].insert(0, v)

        def save():
            try:
                # Basic Validation
                for col, ent in entries.items():
                    if col != cols[0] and not ent.get().strip():
                        messagebox.showwarning('Validation', f'{col} cannot be empty')
                        return

                # Type Validation for specific tables
                if table == 'products':
                    try:
                        float(entries['price'].get())
                        int(entries['stock'].get())
                    except ValueError:
                        messagebox.showwarning('Validation', 'Price must be decimal and Stock must be integer')
                        return

                if existing:
                    sql, cols_no_id = build_update_sql(table, cols)
                    vals = [entries[c].get() for c in cols_no_id]
                    vals.append(entries[cols[0]].get())
                else:
                    sql, cols_no_id = build_insert_sql(table, cols)
                    vals = [entries[c].get() for c in cols_no_id]

                self.db.query(sql, vals, commit=True)
                self.refresh_data(table)
                win.destroy()

            except Exception as e:
                messagebox.showerror('Error', str(e))

        ttk.Button(win, text="💾 Save", command=save).grid(row=len(cols)+1, columnspan=2, pady=10)

# ========== RUN ==========
if __name__ == '__main__':
    root = tk.Tk()
    db = DB(DB_CONFIG)
    db.connect()

    app = ModernApp(root, db)

    root.protocol("WM_DELETE_WINDOW", lambda: (db.close(), root.destroy()))
    root.mainloop()