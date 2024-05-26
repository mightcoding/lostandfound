import sqlite3
import numpy as np
import cv2

DATABASE = 'store.db'

class StoreManager:
    def __init__(self, database):
        self.database = database

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS items (
                                item_id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                date TEXT,
                                img TEXT
                            )''')

            conn.commit()

    def add_items(self, name, img, date):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute("INSERT INTO items (name, date, img) VALUES (?, ?, ?)", (name,date,img))
            conn.commit()

    def date_selector(self,date,todaydate):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute("select * from store where date = ? - todaydate = ? > '3'", (date,todaydate)) #Где дата меньше 3 дней от нынешней
            conn.commit()

    def get_items(self):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * from items")
            return cur.fetchall()
        
    def get_items_data(self,item_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * from items where item_id = ?", (item_id))
            return cur.fetchall()
        
    def collage_creation(self,paths,output):
        images = [cv2.imread(x) for x in paths]
        col = []
        images = [cv2.resize(x, (200,200)) for x in images]
        if len(images) == 3:
            col.append(np.hstack(images[:3]))
        elif len(images) == 1:
            col.append(images[0])
        else:
            col.append(np.vstack(images[:2]))
            if len(images) > 2:
                col.append(np.vstack(images[2:]))
        if len(col) > 1:
            collage = np.hstack(col)
        else:
            collage = col[0]


        
        cv2.imwrite(output,collage)




    


    def show_items(self):
        pass
    
if __name__ == '__main__':
    manager = StoreManager(DATABASE)
    
    manager.collage_creation(["img/666.jpg","img/745.jpg", "img/745.jpg", "img/745.jpg"], "output.png")
    
    