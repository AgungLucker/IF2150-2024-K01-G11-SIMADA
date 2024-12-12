import sqlite3
from LogActivity.log_activity import LogActivity
from Inventaris.inventaris import Inventaris

class ResourceManager:
    def __init__(self, db_name):
        self.db_name = "SIMADA.db"

    def connect(self):
        return sqlite3.connect(self.db_name)

    def check_existing_resource(self, resource_name: str):
        """Memeriksa apakah ada sumber daya dengan nama yang sama"""
        conn = self.connect()
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM Resources WHERE name = ?", (resource_name,))
        existing_resource = cur.fetchall()  
        
        conn.close()
        
        return (len(existing_resource)>0)
    
    def create_resource(self, name:str, quantity:int):
        '''Menambahkan jenis resource baru yang di inginkan oleh user'''
        conn = self.connect()
        cur = conn.cursor()

        if not (self.check_existing_resource(name)):
            cur.execute("""
            INSERT INTO Resources (name, quantity, total_quantity)
            VALUES (?, ?, ?)
            """, (name, quantity, quantity))
            conn.commit()  # simpan ke database
            conn.close()
            return True #berhasil ditambahkan
        else :
            conn.close()
            return False  # Jika nama sudah ada (duplicate entry)
        
    def delete_resource(self, id: int):
        '''Menghapus resource berdasarkan ID'''
        if not isinstance(id, int) or id <= 0:
            print("ID tidak valid.")
            return False

        try:
            # Membuka koneksi ke database
            with self.connect() as conn:
                cur = conn.cursor()  # Membuat cursor

                # Mengecek apakah ID ada di tabel
                cur.execute("SELECT 1 FROM Resources WHERE id = ?", (id,))
                if cur.fetchone() is None:
                    print(f"Resource dengan ID {id} tidak ditemukan.")
                    return False

                # Menjalankan query untuk menghapus resource
                cur.execute("DELETE FROM Resources WHERE id = ?", (id,))
                conn.commit()
                print(f"Berhasil menghapus resource dengan ID {id}.")
                return True

        except Exception as e:
            # Menangani kesalahan
            print(f"Terjadi kesalahan: {e}")
            return False



    def add_or_subtract_resource_quantity(self, id, quantity, add: bool):
        '''Menambahkan jumah quantity yang diinginkan pada resource'''
        conn = self.connect()
        cur = conn.cursor()

        cur.execute("SELECT * FROM Resources WHERE id = ?", (id,))
        existing_resource = cur.fetchone()

        current_quantity = existing_resource[2]  
        total=existing_resource[3]
        new_quantity=0
        if (add):
            new_quantity = current_quantity + quantity
            total+=quantity
        else:
            if current_quantity - quantity<0:
                return False
            new_quantity = current_quantity - quantity
            total -= quantity

        cur.execute("UPDATE Resources SET quantity = ?, total_quantity = ? WHERE id = ?", (new_quantity, total, id))
        id_resource = existing_resource[0]
        conn.commit() 
        conn.close()
        log = LogActivity()
        if add:
            log.log_new_activity(id_resource, "increase", quantity, False)
        else:
            log.log_new_activity(id_resource, "decrease", quantity, False)
    
        return True

    def get_resource_quantity(self, id):
        '''Mendapatkan quantity dari resource yang dipilih user'''
        conn = self.connect()
        cur = conn.cursor()

        cur.execute("SELECT quantity FROM Resources WHERE id = ?", (id,))
        resource_quantity = cur.fetchone()

        conn.close()

        return resource_quantity
    
    def get_all_resource(self):
        conn = self.connect()
        cur = conn.cursor()
        '''Mendapatkan seluruh informasi yang ada dalam table resource'''
        cur.execute("SELECT * FROM Resources")
        list_of_resource = cur.fetchall()
        conn = self.connect()
        cur = conn.cursor()
        print(list_of_resource)
        conn.close()  
        
        return list_of_resource

    def allocate(self, resource_id: int, quantity: int, location: str):
        '''Mengalokasikan sejumlah sumberdaya ke suatu tempat'''
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Resources WHERE id = ?", (resource_id,))
        resource=  cur.fetchone()
        curr_quantity= resource[2]

        if curr_quantity - quantity < 0 :
            conn.close()
            return False
        
        cur.execute("SELECT * FROM Inventaris WHERE location = ? AND resource_id = ?", (location.upper(), resource_id))
        locationArr = cur.fetchall()
        
        inven = Inventaris()
        isExist = False
        if len(locationArr)>0:
            isExist = True
            allocQuantity = quantity + locationArr[0][3]
            state = inven.allocate(resource_id, allocQuantity, location.upper(), isExist)    
            print("masuk") 
        else:
            state = inven.allocate(resource_id, quantity, location.upper(), isExist)    
            
        updated = curr_quantity-quantity
        print(updated)
        cur.execute("UPDATE Resources SET quantity = ? WHERE id = ?", (updated, resource_id))
        conn.commit()
    
        cur.execute("SELECT * FROM Resources WHERE id = ?", (resource_id,))
        new_rec=  cur.fetchone()
        print(new_rec)
        log = LogActivity()
        log.log_new_activity(resource_id, "allocate", quantity, True, location.upper())
        
        conn.close()
        return state


