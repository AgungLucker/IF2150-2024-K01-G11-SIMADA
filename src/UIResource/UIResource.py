import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import PhotoImage, Button, Label, Toplevel, Text, Frame
from ResourceControl.resource_control import ResourceControl

class UIResource:
    def __init__(self, root):
        self.root = root
        self.root.title("SIMADA")
        self.resourceControl = ResourceControl()

        # Ukuran window
        self.root.geometry("778x539")
        self.root.config(bg='#2F0160')
        
        # Penyimpanan untuk mekanisme update Daftar Resource
        self.resource_canvases = []

        # Setup halaman pertama
        self.setupFirstPage()

    def setupFirstPage(self):
        """Membuat halaman pertama dengan scrollable canvas"""
        self.firstPage = tk.Frame(self.root)
        self.firstPage.pack(fill=tk.BOTH, expand=True)

        self.firstPageCanvasFrame = tk.Frame(self.firstPage)
        self.firstPageCanvasFrame.pack(fill=tk.BOTH, expand=True)

        self.firstPageCanvas = tk.Canvas(self.firstPageCanvasFrame, bg='#2F0160', highlightthickness=0)
        self.firstPageCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.firstPageScrollbar = tk.Scrollbar(self.firstPageCanvasFrame, orient="vertical", command=self.firstPageCanvas.yview, width=20)
        self.firstPageScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.firstPageCanvas.configure(yscrollcommand=self.firstPageScrollbar.set)

        self.firstPageScrollableFrame = tk.Frame(self.firstPageCanvas, bg='#2F0160')
        self.firstPageCanvas.create_window((0, 0), window=self.firstPageScrollableFrame, anchor="nw")
        
        self.firstPageScrollableFrame.bind("<Configure>", lambda e: self.firstPageCanvas.configure(scrollregion=self.firstPageCanvas.bbox("all")))
        self.firstPageCanvas.bind_all("<MouseWheel>", self.onMouseWheelFirst)
        self.setupFirstPageContent()
        
    def onMouseWheelFirst(self, event):
        """Menangani event scroll menggunakan mouse wheel atau trackpad"""
        if event.delta: 
            self.firstPageCanvas.yview_scroll(int(-1*(event.delta/120)), "units")
        elif event.num == 5:  
            self.firstPageCanvas.yview_scroll(1, "units")
        elif event.num == 4: 
            self.firstPageCanvas.yview_scroll(-1, "units")

    # Konten Daftar Resource
    def setupFirstPageContent(self):
        headerAwal = tk.Label(self.firstPageScrollableFrame, text="SIMADA", font=("Arial", 20, "bold"), bg='#2F0160', fg='yellow')
        headerAwal.pack(pady=(30, 0), anchor="w", padx=(50, 10))  

        namaPage = tk.Label(self.firstPageScrollableFrame, text="Daftar Resource", font=("Arial", 25, "bold"), bg='#2F0160', fg='white')
        namaPage.pack(pady=(0, 6), anchor="w", padx=(245, 10))  # 

        self.loadImage = tk.PhotoImage(file="img/tambahButton.png")  

        self.tambahButton = tk.Button(self.firstPageScrollableFrame, image=self.loadImage, command=self.formCreateResource, bd=0, highlightthickness=0)
        self.tambahButton.pack(pady=20, anchor="w", padx=(50, 10))  

        self.bgImage = PhotoImage(file="img/bar.png")
        self.allocateButtonImage = PhotoImage(file="img/allocateButton.png")
        self.deleteButton1Image = PhotoImage(file="img/deleteButton1.png")
        self.editButtonImage = PhotoImage(file="img/editButton.png")
        self.InventarisButtonImage = PhotoImage(file="img/InventarisButton.png")
        
        self.updateResourceList()
   
    # Mekanisme refresh daftar resource
    def updateResourceList(self):
        for resource_canvas in self.resource_canvases:
            resource_canvas.destroy()

        # Kosongkan list referensi resource_canvases
        self.resource_canvases.clear()

        # Cek placeholder kosong
        if hasattr(self, 'no_resource_label') and self.no_resource_label:
            self.no_resource_label.destroy()

        resources = self.resourceControl.get_all_resource_information()

        if resources:
            self.resources = resources
            # cek
            print(resources)
            for resource in resources:
                self.createResourceRow(resource)
        else:
            self.no_resource_label = tk.Label(self.firstPageScrollableFrame, text="Tidak ada resource", font=("Arial", 18, "bold"), bg="#2F0160", fg="white")
            self.no_resource_label.pack(padx=(265,10), pady=10, anchor="w")

    def createResourceRow(self, resource):   
        resourceCanvas = tk.Canvas(self.firstPageScrollableFrame, width=678, height=91, bg='#2F0160', highlightthickness=0)
        resourceCanvas.pack(anchor="w", padx=50, pady=(10, 10), fill="x")  

        resourceCanvas.create_image(0, 0, anchor="nw", image=self.bgImage)
        resourceCanvas.image = self.bgImage
        nameLabel = tk.Label(self.firstPageScrollableFrame, text=resource[1], font=("Arial", 20, "bold"), bg="#F7F7F7", fg="black")
        resourceCanvas.create_window(30, 45, anchor="w", window=nameLabel)  

        # Button-button pada ResourceRow
        allocateButton = tk.Button(
            self.firstPageScrollableFrame, image=self.allocateButtonImage,
            command=lambda: self.formAllocateResource(resource[0], resource[1]),
            bd=0,  
            highlightthickness=0,  
            bg="#2F0160",  
            activebackground="#2F0160"  
        )
        resourceCanvas.create_window(340, 45, anchor="w", window=allocateButton)
        
        editButton = tk.Button(
            self.firstPageScrollableFrame,image=self.editButtonImage,
            command=lambda : self.formUpdateResource(resource[0], resource[1]),
            bd=0,  
            highlightthickness=0,  
            bg="#2F0160",  
            activebackground="#2F0160"  
        )
        resourceCanvas.create_window(425, 45, anchor="w", window=editButton)

        deleteButton1 = tk.Button(
            self.firstPageScrollableFrame,
            image=self.deleteButton1Image,
            command=lambda: self.deleteResource(resource[0], resource[1]),
            bd=0,
            highlightthickness=0,
            bg="#2F0160",
            activebackground="#2F0160"
        )
        resourceCanvas.create_window(505, 45, anchor="w", window=deleteButton1)

        InventarisButton = tk.Button(
            self.firstPageScrollableFrame,
            image=self.InventarisButtonImage,
            command=lambda: self.goToSecondPage(resource),
            bd=0,
            highlightthickness=0,
            bg="#2F0160",
            activebackground="#2F0160"
        )
        resourceCanvas.create_window(590, 45, anchor="w", window=InventarisButton)
        
        self.resource_canvases.append(resourceCanvas)

    # PopUp UI untuk membuat Resource
    def formCreateResource(self):
        createWindow = tk.Toplevel(self.root)
        createWindow.title("Tambah Resource")
        createWindow.config(bg='#2F0160')
        createWindow.geometry("510x310")  

        # Load gambar input field
        inputFieldBG = tk.PhotoImage(file="img/inputField.png")

        # Header Form
        headerPage = tk.Label(createWindow, text="Create Resource", font=("Arial", 16, "bold"), bg='#2F0160', fg='white')
        headerPage.pack(pady=(10, 2), anchor="w", padx=15)

        descPage = tk.Label(createWindow, text="Silakan lengkapi isian berikut untuk menambah resource baru", font=("Arial", 10), bg='#2F0160', fg='white')
        descPage.pack(pady=(2, 12), anchor="w", padx=15)

        # Nama Resource
        nameFrame = tk.Frame(createWindow, bg='#2F0160')
        nameFrame.pack(anchor="w", padx=15, pady=(5, 5))

        nameLabel = tk.Label(nameFrame, text="Nama Resource:", bg='#2F0160', fg='white', font=("Arial", 12))
        nameLabel.pack(side="left")

        nameCanvas = tk.Canvas(nameFrame, width=230, height=32, bg='#2F0160', highlightthickness=0)
        nameCanvas.pack(side="left", padx=(10, 0))
        nameCanvas.create_image(0, 0, image=inputFieldBG, anchor="nw")
        
        nameEntry = tk.Entry(nameCanvas, font=("Arial", 12), bg="#ffffff", bd=0, justify="left")
        nameEntry.place(x=10, y=5, width=210, height=22)  # Sesuaikan ukuran dan posisi entry

        # quantity Resource
        quantityFrame = tk.Frame(createWindow, bg='#2F0160')
        quantityFrame.pack(anchor="w", padx=15, pady=(5, 5))

        quantityLabel = tk.Label(quantityFrame, text="Jumlah Resource:", bg='#2F0160', fg='white', font=("Arial", 12))
        quantityLabel.pack(side="left")

        quantityCanvas = tk.Canvas(quantityFrame, width=230, height=32, bg='#2F0160', highlightthickness=0)
        quantityCanvas.pack(side="left", padx=(10, 0))
        quantityCanvas.create_image(0, 0, image=inputFieldBG, anchor="nw")
        
        quantityEntry = tk.Entry(quantityCanvas, font=("Arial", 12), bg="#ffffff", bd=0, justify="left")
        quantityEntry.place(x=10, y=5, width=210, height=22)  

        submitButton = tk.Button(
        createWindow,
        text="Tambah",
        bg="darkorange",
        fg="white",
        activebackground="orange",
        activeforeground="black",
        relief="flat",
        font=("Arial", 12),
        command=lambda: self.addNewResource(nameEntry, quantityEntry, createWindow)
        )
        submitButton.pack(anchor="w", padx=(310, 25), pady=(10, 10))  
        
        createWindow.inputFieldBG = inputFieldBG

    # Mekanisme create resource baru
    def addNewResource(self, nameEntry, quantityEntry, window):
        name = nameEntry.get()
        if not name:
            messagebox.showerror("Fail", "Nama Resource tidak boleh kosong!")
            window.destroy()
            return
            
        try:
            name = nameEntry.get()
            quantity = int(quantityEntry.get())
            isSuccess = self.resourceControl.create_new_resource(name.upper(), quantity)
            if isSuccess == 0:
                messagebox.showerror("Fail", f"Quantity yang dimasukkan tidak valid!")
            elif isSuccess == 1:
                messagebox.showerror("Fail", f"Resource sudah terdaftar dalam sistem!")
            else:
                self.updateResourceList()
                messagebox.showinfo("Success", f"Resource '{name}' berhasil ditambahkan dengan jumlah {quantity}.")
        except ValueError:
            messagebox.showerror("Fail", "Quantity yang dimasukkan tidak valid!")
        window.destroy()
    
    # PopUp UI untuk alokasi resource
    def formAllocateResource(self, resource_id, resource_name):    
        allocateWindow = tk.Toplevel(self.root)
        allocateWindow.title("Allocate Resource")
        allocateWindow.config(bg='#2F0160')
        allocateWindow.geometry("510x265")

        inputFieldBG = tk.PhotoImage(file="img/inputField.png")

        headerPage = tk.Label(allocateWindow, 
                          text=f"Allocate Resource {resource_name}",  # Nama resource disisipkan ke dalam teks
                          font=("Arial", 16, "bold"),
                          bg='#2F0160', fg='white')
        headerPage.pack(pady=(10, 2), anchor="w", padx=15)
        
        descPage = tk.Label(allocateWindow, text="Silakan alokasi Resource pada lokasi yang ingin dituju beserta quantity nya", font=("Arial", 10), bg='#2F0160', fg='white')
        descPage.pack(pady=(2, 12), anchor="w", padx=15)

        # Lokasi Resource yang ingin dialokasi
        newLocationFrame = tk.Frame(allocateWindow, bg='#2F0160')
        newLocationFrame.pack(anchor="w", padx=15, pady=(5, 5))

        newLocationLabel = tk.Label(newLocationFrame, text="Lokasi Tujuan Resource:", bg='#2F0160', fg='white', font=("Arial", 12))
        newLocationLabel.pack(side="left")

        newLocationCanvas = tk.Canvas(newLocationFrame, width=230, height=32, bg='#2F0160', highlightthickness=0)
        newLocationCanvas.pack(side="left", padx=(10, 0))
        newLocationCanvas.create_image(0, 0, image=inputFieldBG, anchor="nw")
        
        newLocationEntry = tk.Entry(newLocationCanvas, font=("Arial", 12), bg="#ffffff", bd=0, justify="left")
        newLocationEntry.place(x=10, y=5, width=210, height=22)  
        
        # Alokasi Quantity
        quantityFrame = tk.Frame(allocateWindow, bg='#2F0160')
        quantityFrame.pack(anchor="w", padx=15, pady=(5, 5))

        quantityLabel = tk.Label(quantityFrame, text="Jumlah Quantity alokasi:", bg='#2F0160', fg='white', font=("Arial", 12))
        quantityLabel.pack(side="left")

        quantityCanvas = tk.Canvas(quantityFrame, width=233, height=32, bg='#2F0160', highlightthickness=0)
        quantityCanvas.pack(side="left", padx=(10, 0))
        quantityCanvas.create_image(3, 0, image=inputFieldBG, anchor="nw")
        
        quantityEntry = tk.Entry(quantityCanvas, font=("Arial", 12), bg="#ffffff", bd=0, justify="left")
        quantityEntry.place(x=13, y=5, width=210, height=22)  

        submitButton = tk.Button(
            allocateWindow,
            text="Allocate",
            bg="blue",
            fg="white",
            activebackground="darkblue",
            activeforeground="yellow",
            relief="flat",
            font=("Arial", 12),
            command=lambda: self.allocateResourceQuantity(resource_id, newLocationEntry, quantityEntry, resource_name, allocateWindow)
        )
        submitButton.pack(anchor="w", padx=(360, 25), pady=(10, 10))
        
        allocateWindow.inputFieldBG = inputFieldBG
        
    def allocateResourceQuantity(self, ResourceID, newLocationEntry, quantityEntry, resource_name,  allocateWindow):
        """Mengupdate jumlah resource."""        
        resource_id = ResourceID
        location = newLocationEntry.get()
        
        if not location:
            messagebox.showerror("Fail", "Lokasi alokasi tidak boleh kosong!")
            allocateWindow.destroy()
            return
        try:
            quantity = int(quantityEntry.get())
            isSuccess = self.resourceControl.allocate(resource_id, quantity, location.upper())
            if isSuccess == 0:
                messagebox.showerror("Fail", f"Quantity yang dialokasikan tidak valid!")
                
            elif isSuccess == 1:
                messagebox.showerror("Fail", f"Quantity yang dialokasikan melebihi total quantity!")
            else:
                self.updateResourceList()
                messagebox.showinfo("Success", f"Resource {resource_name} berhasil ditambahkan dengan jumlah {quantity}.")
        except ValueError:
            messagebox.showerror("Fail", "Quantity yang dialokasikan tidak valid!")
        allocateWindow.destroy()

    # PopUp UI untuk update resource
    def formUpdateResource(self, resource_id, resource_name):  
        updateWindow = tk.Toplevel(self.root)
        updateWindow.title("Update Resource")
        updateWindow.config(bg='#2F0160')
        updateWindow.geometry("510x250")
        
        # Load gambar input field
        inputFieldBG = tk.PhotoImage(file="img/inputField.png")
        nameEntry = resource_name

        # Header Form
        headerPage = tk.Label(updateWindow, 
                            text=f"Update Resource {nameEntry}", 
                            font=("Arial", 16, "bold"), 
                            bg='#2F0160', fg='white')
        headerPage.pack(pady=(10, 2), anchor="w", padx=15)
        
        descPage = tk.Label(updateWindow, 
                            text="Silakan update quantity resource", 
                            font=("Arial", 10),
                            bg='#2F0160', fg='white')
        descPage.pack(pady=(2, 12), anchor="w", padx=15)
        
        # Toggle switch (Tambah / Kurang)
        self.isAdd = tk.BooleanVar(value=True)  

        toggleFrame = tk.Frame(updateWindow, bg="#2F0160")
        toggleFrame.pack(pady=(4,10))
        
        self.addButton = tk.Button(
            toggleFrame,
            text="Tambah",
            bg="gray" if self.isAdd.get() else "#D3D3D3",  
            fg="white",
            font=("Arial", 12),
            relief="flat",
            command=lambda: self.toggleSwitch(True)  
        )
        self.addButton.pack(side="left", padx=(60,1))

        self.kurangButton = tk.Button(
            toggleFrame,
            text="Kurang",
            bg="gray" if not self.isAdd.get() else "#D3D3D3",  
            fg="white",
            font=("Arial", 12),
            relief="flat",
            command=lambda: self.toggleSwitch(False)  
        )
        self.kurangButton.pack(side="left", padx=(1,5))

        newQuantityFrame = tk.Frame(updateWindow, bg='#2F0160')
        newQuantityFrame.pack(anchor="w", padx=15, pady=(5, 5))

        newQuantityLabel = tk.Label(newQuantityFrame, text="Perubahan quantity:", bg='#2F0160', fg='white', font=("Arial", 12))
        newQuantityLabel.pack(side="left")

        newQuantityCanvas = tk.Canvas(newQuantityFrame, width=230, height=32, bg='#2F0160', highlightthickness=0)
        newQuantityCanvas.pack(side="left", padx=(10, 0))
        newQuantityCanvas.create_image(0, 0, image=inputFieldBG, anchor="nw")
        
        newQuantityEntry = tk.Entry(newQuantityCanvas, font=("Arial", 12), bg="#ffffff", bd=0, justify="left")
        newQuantityEntry.place(x=10, y=5, width=210, height=22)  

        # Tombol Update
        submitButton = tk.Button(
            updateWindow, text="Update",
            bg="blue",
            fg="white",
            activebackground="darkblue",
            activeforeground="yellow",
            relief="flat",
            font=("Arial", 12),
            command=lambda: self.updateResourceQuantity(resource_id, newQuantityEntry, self.isAdd.get(), updateWindow)
        )
        submitButton.pack(anchor="w", padx=(340, 25), pady=(10, 10))
        
        updateWindow.inputFieldBG = inputFieldBG

    def toggleSwitch(self, action):
        self.isAdd.set(action)
        self.updateToggleButtonColor()  

    # Mekanisme toggle warna untuk mode button
    def updateToggleButtonColor(self):
        if self.isAdd.get():  
            self.addButton.config(bg="gray")  
            self.kurangButton.config(bg="#D3D3D3")  
        else:  # "Kurang" aktif
            self.kurangButton.config(bg="gray")  
            self.addButton.config(bg="#D3D3D3")  


    def updateResourceQuantity(self, resourceID, newQuantityEntry, add, updateWindow):  
        resource_id = resourceID
        try:
            new_quantity = int(newQuantityEntry.get())
            isSuccess = self.resourceControl.update_resource_quantity(resource_id, new_quantity, add)
            if (isSuccess):
                messagebox.showinfo("Success", f" Quantity resource dengan Resouce ID {resource_id} berhasil di-update.")
                self.updateResourceList()
            else:
                messagebox.showinfo("Fail", f" Quantity yang dimasukkan tidak valid!")
        except ValueError:
            messagebox.showerror("Error", "Quantity yang dimasukkan tidak valid!")
        updateWindow.destroy()

    # Mekanisme delete Resource
    def deleteResource(self, resource_id, resource_name ):   
        isSuccess = self.resourceControl.delete_available_resource(resource_id)
        
        self.updateResourceList()
        if (isSuccess):
            messagebox.showinfo("Success", f"Resource {resource_name} telah dihapus.")
        else:
            messagebox.showerror("Fail", f"Resource {resource_name} gagal dihapus.")

        
    def setupSecondPage(self, resource):
        self.secondPage = tk.Frame(self.root)
        self.secondPage.pack(fill=tk.BOTH, expand=True)  

        # Membuat canvas dan scrollable area untuk halaman kedua
        self.canvasFrameSecond = tk.Frame(self.secondPage)
        self.canvasFrameSecond.pack(fill=tk.BOTH, expand=True)  

        self.canvas_second = tk.Canvas(self.canvasFrameSecond, bg='#2F0160', highlightthickness=0)
        self.canvas_second.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) 

        self.scrollbar_second = tk.Scrollbar(self.canvasFrameSecond, orient="vertical", command=self.canvas_second.yview, width=20)
        self.scrollbar_second.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas_second.configure(yscrollcommand=self.scrollbar_second.set)

        self.secondPageScrollableFrame = tk.Frame(self.canvas_second, bg='#2F0160')
        self.canvas_second.create_window((0, 0), window=self.secondPageScrollableFrame, anchor="nw")

        self.secondPageScrollableFrame.bind("<Configure>", lambda e: self.canvas_second.configure(scrollregion=self.canvas_second.bbox("all")))
        self.canvas_second.bind_all("<MouseWheel>", self.onMouseWheelSecond)
        self.setupSecondPageContent(resource)

    def onMouseWheelSecond(self, event):
        """Menangani event scroll menggunakan mouse wheel atau trackpad"""
        if event.delta: 
            self.canvas_second.yview_scroll(int(-1*(event.delta/120)), "units")
        elif event.num == 5:  
            self.canvas_second.yview_scroll(1, "units")
        elif event.num == 4: 
            self.canvas_second.yview_scroll(-1, "units")

    def setupSecondPageContent(self, resource):
        self.currentActiveTab = 'inventaris'  
        
        tabControlFrame = tk.Frame(self.secondPageScrollableFrame, bg="#2F0160")
        tabControlFrame.pack(fill=tk.X)

        self.tabContentFrame = tk.Frame(self.secondPageScrollableFrame, bg="#2F0160")
        self.tabContentFrame.pack(fill=tk.BOTH, expand=True, pady=(2, 0))

        tabCanvas = tk.Canvas(tabControlFrame, bg="#2F0160", height=70, width=778, highlightthickness=0, bd=0)
        tabCanvas.pack(anchor="w", pady=(20, 2), fill=tk.X)
        
        self.InventarisImage = tk.PhotoImage(file="img/InventarisTab.png")  
        self.LogActivityImage = tk.PhotoImage(file="img/InventarisTab.png") 
        self.backButtonImage = tk.PhotoImage(file="img/xButton.png")  
        
        self.inventarisButton = tk.Button(
            tabCanvas, image=self.InventarisImage, text="Inventaris",  
            font=("Arial", 22, "bold"), bg="#2F0160", fg="white", 
            command=lambda: self.togglesecondPageTab('inventaris', resource), borderwidth=0,
            highlightthickness=0, relief="flat",  
            compound="center"  
        )
        tabCanvas.create_window(145, 37, window=self.inventarisButton)

        self.logActivityButton = tk.Button(
            tabCanvas, image=self.LogActivityImage, text="Log Activity", 
            font=("Arial", 22, "bold"), bg="#2F0160", fg="#2F0160", 
            command=lambda: self.togglesecondPageTab('logActivity', resource), borderwidth=0,
            highlightthickness=0, relief="flat",  
            compound="center"  
        )
        
        tabCanvas.create_window(400, 37, window=self.logActivityButton)
        
        self.backButtonImage = tk.PhotoImage(file="img/xButton.png")  
        backButton = tk.Button(
            tabCanvas, image=self.backButtonImage, command=self.goToFirstPage,bg="#2F0160",
            borderwidth=0, highlightthickness=0  
        )
        tabCanvas.create_window(735, 15, anchor="ne", window=backButton)
        
        tabCanvas.create_line(0, 65, 778, 65, fill="white", width=2)

        self.showTab(lambda: self.showInventoryContent(resource))
        self.updateTabState()

    def updateTabState(self):
        if self.currentActiveTab == 'inventaris':  
            self.inventarisButton.config(image=self.InventarisImage, fg="#2F0160") 
        else:  
            self.inventarisButton.config(image="", fg="white")  
        
        if self.currentActiveTab == 'logActivity':  
            self.logActivityButton.config(image=self.LogActivityImage, fg="#2F0160")  
        else:   
            self.logActivityButton.config(image="", fg="white")  

    def togglesecondPageTab(self, tabName, resource):
        if tabName == 'inventaris':
            self.currentActiveTab = 'inventaris'  
            self.showTab(lambda: self.showInventoryContent(resource))  
        elif tabName == 'logActivity':
            self.currentActiveTab = 'logActivity'  
            self.showTab(lambda: self.showLogActivityContent(resource[0]))

        self.updateTabState()

    # Konten untuk tab Inventaris
    def showInventoryContent(self, resource):
        self.inventaris_canvases = []
        
        for widget in self.tabContentFrame.winfo_children():
            widget.destroy()

        self.bgImage = PhotoImage(file="img/barInventory.png")
        self.quantityImage = PhotoImage(file="img/quantityInventory.png")
        self.distributeButtonImage = PhotoImage(file="img/distributeButton.png")
        self.deallocateButtonImage = PhotoImage(file="img/deleteButton2.png")
        
        self.currentQuantity = tk.Label(self.tabContentFrame, text=f"{resource[2]} / {resource[3]}", font=("Arial", 18, "bold"), bg="#2F0160", fg="white")
        self.currentQuantity.pack(padx=(65,10), pady=10, anchor="w")
        
        self.updateInventaris(resource[0])
            
    # Mekanisme refresh konten Inventaris
    def updateInventaris(self, resource_id):
        print(resource_id)
        self.updateResourceList()
        
        # Update Resource
        print(f"hasil {self.resources[0]}")
        updatedResource = None
        for resource in self.resources:
            if resource[0] == resource_id:
                updatedResource = resource
                break  # 
            
        for inventaris_canvas in self.inventaris_canvases:
            inventaris_canvas.destroy()  
        
        self.inventaris_canvases.clear()
        
        # Cek placeholder kosong
        if hasattr(self, 'no_inventory_label') and self.no_inventory_label:
            self.no_inventory_label.destroy()
            
        Inventaris = self.resourceControl.get_all_inventaris(resource_id)
        
        if Inventaris:
            for Inventory in Inventaris:
                self.createInventoryRow(Inventory)
            self.currentQuantity.config(text=f"{updatedResource[2]} / {updatedResource[3]}") 
        else:
            # Jika tidak ada inventaris
            self.no_inventory_label = tk.Label(self.tabContentFrame, text="Tidak ada inventory yang dialokasikan", font=("Arial", 18, "bold"), bg="#2F0160", fg="white")
            self.no_inventory_label.pack(padx=(135,10), pady=10, anchor="w")
    
    # Bagian menampilkan data Inventory
    def createInventoryRow(self, inventory):
        inventoryCanvas = tk.Canvas(self.tabContentFrame, width=678, height=91, bg='#2F0160', highlightthickness=0)
        inventoryCanvas.pack(anchor="w", padx=50, pady=(10, 10), fill="x")  #

        inventoryCanvas.create_image(0, 0, anchor="nw", image=self.bgImage)
        inventoryCanvas.image = self.bgImage 
        
        nameLabel = tk.Label(self.tabContentFrame, text=inventory[2], font=("Arial", 20, "bold"), bg="#F7F7F7", fg="black")
        inventoryCanvas.create_window(30, 45, anchor="w", window=nameLabel)  
        
        inventoryCanvas.create_image(315, 22, anchor="nw", image=self.quantityImage)
        inventoryCanvas.image = self.quantityImage 
        
        QuantityLabel = tk.Label(self.tabContentFrame, text=inventory[3], font=("Arial", 20, "bold"), bg="#2F0160", fg="white")
        inventoryCanvas.create_window(405, 45, anchor="w", window=QuantityLabel) 
        
        deallocateButton = tk.Button(
            self.tabContentFrame,
            image=self.deallocateButtonImage,
            command=lambda: self.formDeallocateInventory(inventory[0], inventory[1], inventory[3]),
            bd=0,
            highlightthickness=0,
            bg="#2F0160",
            activebackground="#2F0160"
        )
        inventoryCanvas.create_window(515, 45, anchor="w", window=deallocateButton)
        
        self.inventaris_canvases.append(inventoryCanvas)
        
        distributeButton = tk.Button(
            self.tabContentFrame,
            image=self.distributeButtonImage,
            command=lambda: self.formDistributeInventory(inventory[0], inventory[1], inventory[2], inventory[3]),
            bd=0,
            highlightthickness=0,
            bg="#2F0160",
            activebackground="#2F0160"
        )
        inventoryCanvas.create_window(605, 45, anchor="w", window=distributeButton)    
        
    # PopUp deallocate
    def formDeallocateInventory(self, Inventaris_id, resource_id, quantity):
        deallocateWindow = tk.Toplevel(self.root)
        deallocateWindow.title("Deallocate Resource ")
        deallocateWindow.config(bg='#2F0160')
        deallocateWindow.geometry("510x300")  
        
        # Load gambar 
        inputFieldBG = tk.PhotoImage(file="img/inputField.png")

        # Header Form
        headerPage = tk.Label(deallocateWindow, 
                            text=f"Deallocate Resource", 
                            font=("Arial", 16, "bold"), 
                            bg='#2F0160', fg='white')
        headerPage.pack(pady=(10, 2), anchor="w", padx=15)
        
        descPage = tk.Label(deallocateWindow, 
                            text="Silakan dealokasi quantity resource dengan quantity yang diinginkan", 
                            font=("Arial", 10),
                            bg='#2F0160', fg='white')
        descPage.pack(pady=(2, 12), anchor="w", padx=15)

        deallocQuantityFrame = tk.Frame(deallocateWindow, bg='#2F0160')
        deallocQuantityFrame.pack(anchor="w", padx=15, pady=(5, 5))

        deallocQuantityLabel = tk.Label(deallocQuantityFrame, text="Dealokasi quantity:", bg='#2F0160', fg='white', font=("Arial", 12))
        deallocQuantityLabel.pack(side="left")

        deallocQuantityCanvas = tk.Canvas(deallocQuantityFrame, width=230, height=32, bg='#2F0160', highlightthickness=0)
        deallocQuantityCanvas.pack(side="left", padx=(10, 0))
        deallocQuantityCanvas.create_image(0, 0, image=inputFieldBG, anchor="nw")
        
        deallocQuantityEntry = tk.Entry(deallocQuantityCanvas, font=("Arial", 12), bg="#ffffff", bd=0, justify="left")
        deallocQuantityEntry.place(x=10, y=5, width=210, height=22)  
        
        isDelete = tk.BooleanVar(value=False)

        checkboxButtonDealloctFrame = tk.Frame(deallocateWindow, bg='#2F0160')
        checkboxButtonDealloctFrame.pack(anchor="w", padx=15, pady=(10, 10), fill="x")

        deleteFrame = tk.Frame(checkboxButtonDealloctFrame, bg='#2F0160')
        deleteFrame.pack(side="left", padx=15) 
        deleteFrame.pack_forget()  

        deleteCheckbox = tk.Checkbutton(
            deleteFrame,
            text="Delete Location",
            variable=isDelete,
            onvalue=True,
            offvalue=False,
            bg='#2F0160',
            fg='white',
            selectcolor="#2F0160",
            font=("Arial", 12),
            activebackground="#2F0160",
            activeforeground="white"
        )
        deleteCheckbox.pack(anchor="w", padx=(95,5))

        # Tombol submit
        submitButton = tk.Button(
            checkboxButtonDealloctFrame, text="Update",
            bg="blue",
            fg="white",
            activebackground="darkblue",
            activeforeground="yellow",
            relief="flat",
            font=("Arial", 12),
            command=lambda: self.deallocateResource(Inventaris_id, resource_id, deallocQuantityEntry, isDelete.get(), deallocateWindow)
        )
        submitButton.pack(side="right", padx=(0, 105))

        # bandingkan quantity
        def matchDealloctQuantity(*args):
            try:
                inputQuantity = int(deallocQuantityEntry.get())
                if inputQuantity == quantity:
                    deleteFrame.pack(side="left", padx=(0, 10))  
                else:
                    deleteFrame.pack_forget()  
            except ValueError:
                deleteFrame.pack_forget()  

        # Bind perubahan pada entry ke fungsi matchQuantity
        deallocQuantityEntry.bind("<KeyRelease>", matchDealloctQuantity)

        deallocateWindow.inputFieldBG = inputFieldBG

        
    def deallocateResource(self, inventaris_id, resource_id, deallocQuantityEntry, isDelete, deallocateWindow):
        try:
            quantity = int(deallocQuantityEntry.get())
            isSuccess = self.resourceControl.deallocate(inventaris_id, quantity, isDelete)
            if isSuccess == 0:
                messagebox.showwarning("Fail", f"Quantity yang dialokasikan tidak valid!")
            elif isSuccess == 1:
                messagebox.showwarning("Fail", f"Quantity yang dialokasikan melebihi total quantity!")
            elif isSuccess == 2:
                messagebox.showinfo("Success", f"Resource pada lokasi didealokasi untuk sejumlah {quantity}.")
                self.updateInventaris(resource_id)
            else:
                if (isDelete):
                    messagebox.showinfo("Success", f"Resource pada lokasi berhasil dihapus.")
                    self.updateInventaris(resource_id)
        except ValueError:
            messagebox.showwarning("Fail", "Quantity yang didistribusikan tidak valid!")
            
        deallocateWindow.destroy()
        
    # PopUp form Distribute Resource
    def formDistributeInventory(self, inventaris_id, resource_id, location, quantity):    
        distributeWindow = tk.Toplevel(self.root)
        distributeWindow.title("Distribute Resource")
        distributeWindow.config(bg='#2F0160')
        distributeWindow.geometry("510x265")
        
        inputFieldBG = tk.PhotoImage(file="img/inputField.png")

        headerPage = tk.Label(distributeWindow, 
                          text=f"Distribute Resource from {location}", 
                          font=("Arial", 16, "bold"),
                          bg='#2F0160', fg='white')
        headerPage.pack(pady=(10, 2), anchor="w", padx=15)
        
        descPage = tk.Label(distributeWindow, text="Silakan Distribusi Resource pada lokasi yang ingin dituju beserta quantity nya", font=("Arial", 10), bg='#2F0160', fg='white')
        descPage.pack(pady=(2, 12), anchor="w", padx=15)

        ToLocationFrame = tk.Frame(distributeWindow, bg='#2F0160')
        ToLocationFrame.pack(anchor="w", padx=15, pady=(5, 5))

        ToLocationLabel = tk.Label(ToLocationFrame, text="Lokasi Tujuan Resource:", bg='#2F0160', fg='white', font=("Arial", 12))
        ToLocationLabel.pack(side="left")

        ToLocationCanvas = tk.Canvas(ToLocationFrame, width=230, height=32, bg='#2F0160', highlightthickness=0)
        ToLocationCanvas.pack(side="left", padx=(10, 0))
        ToLocationCanvas.create_image(0, 0, image=inputFieldBG, anchor="nw")
        
        ToLocationEntry = tk.Entry(ToLocationCanvas, font=("Arial", 12), bg="#ffffff", bd=0, justify="left")
        ToLocationEntry.place(x=10, y=5, width=210, height=22)  
        
        # Alokasi Quantity
        quantityFrame = tk.Frame(distributeWindow, bg='#2F0160')
        quantityFrame.pack(anchor="w", padx=15, pady=(5, 5))

        quantityLabel = tk.Label(quantityFrame, text="Quantity untuk distribusi:", bg='#2F0160', fg='white', font=("Arial", 12))
        quantityLabel.pack(side="left")

        quantityCanvas = tk.Canvas(quantityFrame, width=233, height=32, bg='#2F0160', highlightthickness=0)
        quantityCanvas.pack(side="left", padx=(10, 0))
        quantityCanvas.create_image(3, 0, image=inputFieldBG, anchor="nw")
        
        quantityEntry = tk.Entry(quantityCanvas, font=("Arial", 12), bg="#ffffff", bd=0, justify="left")
        quantityEntry.place(x=13, y=5, width=210, height=22)  
        
        # Variabel untuk menyimpan status checkbox delete
        isDelete = tk.BooleanVar(value=False)

        checkboxButtonDistributeFrame = tk.Frame(distributeWindow, bg='#2F0160')
        checkboxButtonDistributeFrame.pack(anchor="w", padx=15, pady=(10, 10), fill="x")
        
        deleteFrame = tk.Frame(checkboxButtonDistributeFrame, bg='#2F0160')
        deleteFrame.pack(side="left", padx=15) 
        deleteFrame.pack_forget()  
        
        deleteCheckbox = tk.Checkbutton(
            deleteFrame,
            text="Delete Location",
            variable=isDelete,
            onvalue=True,
            offvalue=False,
            bg='#2F0160',
            fg='white',
            selectcolor="#2F0160",
            font=("Arial", 12),
            activebackground="#2F0160",
            activeforeground="white"
        )
        deleteCheckbox.pack(anchor="w", padx=(95,5))
        
        submitButton = tk.Button(
            checkboxButtonDistributeFrame,
            text="Distribute",
            bg="blue",
            fg="white",
            activebackground="darkblue",
            activeforeground="yellow",
            relief="flat",
            font=("Arial", 12),
            command=lambda: self.distributeInventory(inventaris_id, resource_id, location, ToLocationEntry, quantityEntry, isDelete.get(), distributeWindow)
        )
        submitButton.pack(side="right", padx=(0, 105))

        # bandingkan quantity
        def matchDistributeQuantity(*args):
            try:
                entered_quantity = int(quantityEntry.get())
                if entered_quantity == quantity:
                    deleteFrame.pack(side="left", padx=(0, 10))   
                else:
                    deleteFrame.pack_forget()  
            except ValueError:
                deleteFrame.pack_forget()  

        # Bind perubahan pada entry ke fungsi check_quantity_match
        quantityEntry.bind("<KeyRelease>", matchDistributeQuantity)
        
        distributeWindow.inputFieldBG = inputFieldBG
        
    def distributeInventory(self, inventaris_id, resource_id, location, ToLocationEntry, quantityEntry, isDelete, distributeWindow):
        """Mengupdate jumlah resource."""    
        Tolocation = ToLocationEntry.get().upper()
        
        if not Tolocation:
            messagebox.showerror("Fail", "Lokasi tidak boleh kosong")
            distributeWindow.destroy()
            return
        try:
            Tolocation = ToLocationEntry.get().upper()
            quantity = int(quantityEntry.get())
            isSuccess = self.resourceControl.distribute_to(inventaris_id, Tolocation, quantity, isDelete)
            if isSuccess == 0:
                messagebox.showerror("Fail", f"Quantity yang didistribusikan tidak valid!")
            elif isSuccess == 1:
                messagebox.showerror("Fail", f"lokasi tidak ditemukan!")
            elif isSuccess == 2:
                messagebox.showerror("Fail", f"lokasi tujuan tidak boleh sama!")
            elif isSuccess == 3:
                messagebox.showerror("Fail", f"Quantity yang didistribusikan melebihi total quantity!")
            elif isSuccess == 4:
                messagebox.showinfo("Success", f"Quantity  sejumlah {quantity} dari {location} berhasil dipindahkan ke {Tolocation}.")
                self.updateInventaris(resource_id)
            else:
                if isDelete:
                    messagebox.showinfo("Success", f"Semua quantity resource di {location} berhasil dipindahkan ke {Tolocation} dan lokasi dihapus.")
                    self.updateInventaris(resource_id)
        except ValueError:
            messagebox.showerror("Fail", "Quantity yang didistribusikan tidak valid!")
        distributeWindow.destroy()
        
    # Tampilan konten logActivity
    def showLogActivityContent(self, resource_id):
        self.logActivity_canvases = []
        
        # Bersihkan tab 
        for widget in self.tabContentFrame.winfo_children():
            widget.destroy()

        self.bgImage = PhotoImage(file="img/barInventory.png")
        self.seeReportButtonImage = PhotoImage(file="img/seereportbutton.png")
        self.reportButtonImage = PhotoImage(file="img/reportButton.png")
        
        # Ambil aktivitas log
        LogActivities = self.resourceControl.get_all_log_for_resource(resource_id)
        print(f"INI ID {resource_id}")
        print(LogActivities)
        
        # Membuat space kosong
        paddingFrame = tk.Frame(self.tabContentFrame, height=30, bg="#2F0160")
        paddingFrame.pack(fill=tk.X)
        
        if len(LogActivities)==0:
            empty_message = tk.Label(
                self.tabContentFrame,
                text="Belum ada Aktivitas terbaru",
                font=("Arial", 18, "bold"),
                bg="#2F0160",
                fg="white"
            )
            empty_message.pack(pady=20)
            return 

        for activity in LogActivities[::-1]: 
            self.createActivityRow(activity, resource_id)

            
    def createActivityRow(self, activity, resource_id):
        activityCanvas = tk.Canvas(self.tabContentFrame, width=678, height=91, bg='#2F0160', highlightthickness=0)
        activityCanvas.pack(anchor="w", padx=50, pady=(10, 10), fill="x") 
         
        activityCanvas.create_image(0, 0, anchor="nw", image=self.bgImage)
        activityCanvas.image = self.bgImage
        
        reportLabel = tk.Label(self.tabContentFrame, text=activity[2], font=("Arial", 14, "bold"), bg="#F7F7F7", fg="black")
        activityCanvas.create_window(30, 45, anchor="w", window=reportLabel) 
        
        #Button see report
        inventarisButton = tk.Button(
            self.tabContentFrame,
            image=self.seeReportButtonImage,
            command=lambda log_id = activity[0]: self.seeReport(log_id),
            bd=0,
            highlightthickness=0,
            bg="#2F0160",
            activebackground="#2F0160"
        )
        activityCanvas.create_window(530, 45, anchor="w", window=inventarisButton)
        
        #Button opsi CRUD
        reportButton = tk.Button(
            self.tabContentFrame,
            image=self.reportButtonImage,
            command=lambda log_id = activity[0]: self.reportOperation(log_id, resource_id),
            bd=0,
            highlightthickness=0,
            bg="#2F0160",
            activebackground="#2F0160"
        )
        activityCanvas.create_window(600, 45, anchor="w", window=reportButton)
        
    
    def middle(self, popup_height, popup_width):
        window = self.root
        screen_width = window.winfo_width()
        screen_height = window.winfo_height()
        position_top = window.winfo_rooty() + (screen_height // 2 - popup_height // 2)
        position_left = window.winfo_rootx() + (screen_width // 2 - popup_width // 2)

        return position_top,position_left
            
    def reportOperation(self, id, resource_id):
        window = self.root
        popup = Toplevel(window)
        popup.geometry("350x150")
        popup.config(bg="#2F0160")  
        popup.grab_set() 
        popup_width = 350
        popup_height = 120
        screen_width = window.winfo_width()
        screen_height = window.winfo_height()

        #Tengah-Tengah
        position_top = window.winfo_rooty() + (screen_height // 2 - popup_height // 2)
        position_left = window.winfo_rootx() + (screen_width // 2 - popup_width // 2)
        popup.geometry(f'{popup_width}x{popup_height}+{position_left}+{position_top}')

        title_label = Label(popup, text="Menu Report", font=("Arial", 14, "bold"), bg="#2F0160", fg="white")
        title_label.pack(pady=10)  

        def create_action():
            popup.destroy()
            already_exist = self.resourceControl.check_exist_report(id)
            if already_exist:
                messagebox.showinfo("Eror", "Laporan sudah pernah dibuat.")
            else:
                self.open_form(resource_id, id, action="create")

        def update_action():
            popup.destroy()
            already_exist = self.resourceControl.check_exist_report(id)
            if not already_exist:
                messagebox.showinfo("Eror", "Laporan belum pernah dibuat, tidak ada yang bisa diupdate.")
            else:
                self.open_form(resource_id, id, action="update")

        def delete_action():
            already_exist = self.resourceControl.check_exist_report(id)
            if not already_exist:
                messagebox.showinfo("Failed", "Gagal menghapus laporan karena laporan belum pernah dibuat")
            else:
                berhasil = self.resourceControl.delete_report(id)
                if (berhasil):
                    messagebox.showinfo("Success", f"Laporan dengan ID {id} berhasil dihapus.")
                else:
                    messagebox.showinfo("Fail", f"Laporan gagal dihapus")    
            popup.destroy()

        def cancel_action():
            print("Cancel action")
            popup.destroy()

        button_frame = Frame(popup, bg="#2F0160") 
        button_frame.pack(side="bottom", fill="x", pady=20)

        # Tombol Create, Update, Delete, dan Cancel
        Button(button_frame, text="Create", command=create_action, bg="#28a745", fg="white").pack(side="left", fill="x", expand=True, padx=5)
        Button(button_frame, text="Update", command=update_action, bg="#2196F3", fg="white").pack(side="left", fill="x", expand=True, padx=5)
        Button(button_frame, text="Delete", command=delete_action, bg="#db2778", fg="white").pack(side="left", fill="x", expand=True, padx=5)
        Button(button_frame, text="Cancel", command=cancel_action, bg="black", fg="white").pack(side="left", fill="x", expand=True, padx=5)
        
    #PopUp UI untuk CRUD Report
    def open_form(self, resource_id, id, action):
        window = self.root
        form_popup = Toplevel(window)
        popup_width = 400
        popup_height = 300
        
        position_top, position_left= self.middle(popup_height,popup_width)
        form_popup.geometry(f"{popup_width}x{popup_height}+{position_left}+{position_top}")
        form_popup.config(bg="#2F0160")
        form_popup.grab_set()
        form_popup.title(f"{action.capitalize()} Report for ID: {id}")

        # Label dan input field untuk form
        label_input = Label(form_popup, text=f"Enter detail to {action} Report:", bg="#2F0160", fg="white", font=("Arial", 12))
        label_input.pack(pady=10)

        # Input Paragraf
        input_field = Text(form_popup, width=50, height=10, font=("Arial", 12), bd=3, relief="solid")
        input_field.pack(pady=5, padx=10)  

        # Fungsi Create and Update
        def submit_create_action(id):
            user_input = input_field.get("1.0", "end-1c")
            if not user_input:
                messagebox.showwarning("Input Error", "Data tidak boleh kosong.")
                return
            berhasil = self.resourceControl.create_report(resource_id, id, user_input)
            if berhasil:
                messagebox.showinfo("Success", "Laporan berhasil dibuat.")
            else:
                messagebox.showerror("Failed", "Gagal membuat laporan.")
            form_popup.destroy()  

        def submit_update_action(id):
            user_input = input_field.get("1.0", "end-1c") 
            if not user_input:
                messagebox.showwarning("Input Error", "Data tidak boleh kosong.")
                return
            berhasil = self.resourceControl.update_report(id, user_input)
            if berhasil:
                messagebox.showinfo("Success", "Laporan berhasil diperbarui.")
            else:
                messagebox.showerror("Failed", "Gagal memperbarui laporan.")
            form_popup.destroy()  

            # Tombol Submit 
        if action == "create":
            Button(form_popup, text="Submit Create", command=lambda: submit_create_action(id), bg="white", fg="#2F0160", font=("Arial", 12)).pack(pady=10)
        elif action == "update":
            Button(form_popup, text="Submit Update", command=lambda: submit_update_action(id), bg="white", fg="#2F0160", font=("Arial", 12)).pack(pady=10)

    def seeReport(self,id):
        report = self.resourceControl.get_report_detail_id(id)

        if report:  # Cek ada data/tidak
            popup = tk.Toplevel()
            popup.title("Report Log")
            popup.config(bg="#2F0160")
            popup.grab_set()
            popup.focus_set()

            # Membuat Popup Berada Ditengah
            position_top, position_left = self.middle(300, 100)
            popup.geometry(f"300x300+{position_left-90}+{position_top+100}") 
            
            frame = tk.Frame(popup)
            frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            frame.pack_propagate(False)  

            # Frame tampil laporan
            text_box = tk.Text(frame, wrap="word", font=("Arial", 12), height=10, width=45, 
                            bg="#2F0160", fg="white", bd=0, relief="flat")  
            text_box.insert(tk.END, report) 
            text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=text_box.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            text_box.config(yscrollcommand=scrollbar.set)

            # Membuat scroll hanya untuk pop up
            def on_mouse_wheel(event):
                """Tangani event scroll untuk text_box"""
                text_box.yview_scroll(int(-1 * (event.delta / 120)), "units")
                return "break"  

            text_box.bind("<MouseWheel>", on_mouse_wheel)  
            text_box.bind("<Button-4>", lambda e: text_box.yview_scroll(-1, "units"))  
            text_box.bind("<Button-5>", lambda e: text_box.yview_scroll(1, "units"))  

        else:
            popup = tk.Toplevel()
            popup.geometry("375x100")
            popup.title("Report")
            position_top, position_left = self.middle(300, 100)
            popup.geometry(f"300x100+{position_left-90}+{position_top+100}") 
            popup.grab_set()
            popup.config(bg="#2F0160")
            
            label = tk.Label(popup, text="Maaf, belum ada Laporan untuk Log ini", wraplength=300, bg="#2F0160", fg="white", font=("Arial", 12))
            label.pack(pady=10)
 
        close_button = tk.Button(popup, text="Close", command=popup.destroy, bg="#2F0160", fg="white")
        close_button.pack(side=tk.BOTTOM, pady=10) 
            

    def showTab(self, content_function):
        """Membersihkan konten tab sebelumnya dan menampilkan konten baru"""
        # Bersihkan semua konten tab sebelumnya
        for widget in self.tabContentFrame.winfo_children():
            widget.destroy()

        content_function()
        

    def goToSecondPage(self, resource):
        self.firstPage.pack_forget()  
        self.setupSecondPage(resource) 
        
    def goToFirstPage(self):
        self.secondPage.pack_forget()  
        self.firstPage.pack(fill="both", expand=True)  