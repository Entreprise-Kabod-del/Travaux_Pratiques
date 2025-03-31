import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
import shutil
from time import ctime
from tkinter import simpledialog

# Création de la fenêtre principale
fenetre_principale = tk.Tk()
fenetre_principale.title("Explorateur de Fichiers")
fenetre_principale.geometry("850x600")

# Chargement des icônes
# Chemin vers les icônes PNG
chemin_icone_dossier = "folder_icon.png"  # Remplacez par le chemin de votre icône de dossier
chemin_icone_fichier = "file_icon.png"    # Remplacez par le chemin de votre icône de fichier

# Chargement des icônes avec PIL et redimensionnement
icone_dossier = ImageTk.PhotoImage(Image.open("C:/Users/Public/folder.png").resize((16, 16)))  # Dossier
icone_fichier = ImageTk.PhotoImage(Image.open("C:/Users/Public/file_icon.png").resize((16, 16)))  # Fichier

# Liste des favoris
favoris = []

# Liste des répertoires récemment ouverts
repertoires_recents = []
MAX_RECENTS = 5  # Nombre maximal de répertoires récents à garder


# Frame principale
frame = tk.Frame(fenetre_principale, border=2, relief="solid")
frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Frame pour les options de navigation à gauche
frame_1 = tk.Frame(frame, width=200, border=2, relief="solid")
frame_1.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

# Frame principale de l'affichage des fichiers
frame_2 = tk.Frame(frame, border=2, relief="solid")
frame_2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

#Barre de navigation
frame_3 = tk.Frame(frame_2, border=2, relief="solid") 
frame_3.pack(fill=tk.X, padx=5, pady=5)

chemin_var = tk.StringVar(value=os.getcwd()) 
entry_chemin = tk.Entry(frame_3, textvariable=chemin_var, width=80) 
entry_chemin.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

btn_go = tk.Button(frame_3, text="Lancer", command=lambda: afficher_fichiers(chemin_var.get())) 
btn_go.pack(side=tk.LEFT, padx=5)

# Barre d'actualisation
def actualiser():
    afficher_fichiers(chemin_var.get())
btn_actualiser = tk.Button(frame_3, text="Actualiser", command=lambda: afficher_fichiers(chemin_var.get())) 
btn_actualiser.pack(side=tk.LEFT, padx=5)

btn_nouveau_dossier = tk.Button(frame_3, text="Nouveau Dossier", command=lambda: creer_nouveau_dossier(chemin_var.get())) 
btn_nouveau_dossier.pack(side=tk.LEFT, padx=5)

# Frame pour le filtrage des fichiers
frame_filtrage = tk.Frame(frame_3)  # Placer sous le chemin actuel
frame_filtrage.pack(fill=tk.X, padx=5, pady=5)

# Liste des extensions de fichiers que tu veux proposer
extensions = ["Tous les fichiers", ".txt", ".jpg", ".png", ".pdf", ".csv", ".docx", ".mp3", ".mp4"]

# Créer un Menu déroulant pour choisir l'extension
filtre_extension_var = tk.StringVar()
filtre_extension_var.set("Tous les fichiers")  # Valeur par défaut
filtre_menu = tk.OptionMenu(frame_filtrage, filtre_extension_var, *extensions)
filtre_menu.pack(side=tk.LEFT, padx=5)

# Bouton pour appliquer le filtre
btn_filtrer = tk.Button(frame_filtrage, text="Filtrer", command=lambda: afficher_fichiers(chemin_var.get(), filtre_extension_var.get()))
btn_filtrer.pack(side=tk.LEFT, padx=5)


# Fonction pour afficher les fichiers du dossier
def afficher_fichiers(chemin, extension_filter="Tous les fichiers"):
    chemin_var.set(chemin)  # Mettre à jour le chemin
    tree.delete(*tree.get_children())  # Réinitialiser l'affichage des fichiers

    try:
        for fichier in os.listdir(chemin):
            chemin_complet = os.path.join(chemin, fichier)
            
            # Appliquer le filtre d'extension si nécessaire
            if extension_filter != "Tous les fichiers" and not fichier.lower().endswith(extension_filter.lower()):
                continue  # Ignore ce fichier s'il ne correspond pas à l'extension
            
            # Calculer la taille et la date de création
            if os.path.isdir(chemin_complet):
                taille = taille_dossier(chemin_complet)
            else:
                taille = os.path.getsize(chemin_complet)
            
            date_creation = ctime(os.path.getctime(chemin_complet))  # Obtenir la date de création

            # Insérer l'élément dans la Treeview
            tree.insert("", "end", values=(fichier, f"{taille} octets", "Dossier" if os.path.isdir(chemin_complet) else "Fichier", date_creation), tags=(chemin_complet,))
    
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'afficher les fichiers : {str(e)}")


# Fonction pour calculer la taille d'un dossier
def taille_dossier(chemin):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(chemin):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

# Fonction pour ouvrir un dossier
def ouvrir_dossier(chemin):
    afficher_fichiers(chemin)

# Fonction pour ouvrir le répertoire des récents
def ouvrir_recents(): 
    chemin = os.path.expanduser("~")  # Ouvre le dossier utilisateur 
    afficher_fichiers(chemin)

def ouvrir_recents():
    tree.delete(*tree.get_children())  # Réinitialiser l'affichage des fichiers
    if repertoires_recents:
        for chemin in repertoires_recents:
            nom = os.path.basename(chemin)
            tree.insert("", "end", values=(nom, "-", "Récents", "-"), tags=(chemin,))
    else:
        messagebox.showinfo("Récents", "Aucun répertoire récent.")
  

# Fonction pour ouvrir les favoris
def ouvrir_favoris():
    global favoris
    tree.delete(*tree.get_children())
    for chemin in favoris:
        nom = os.path.basename(chemin)
        tree.insert("", "end", values=(nom, "-", "Favori", "-"), tags=(chemin,))

def ouvrir_tags():
    chemin_tags = os.path.expanduser("~/.tags")  # Le chemin du répertoire des tags
    
    if not os.path.exists(chemin_tags):  # Créer le répertoire si nécessaire
        os.makedirs(chemin_tags)
    
    afficher_fichiers(chemin_tags)  # Afficher le contenu du répertoire des tags        


# Fonction pour ouvrir "Computer", répertorier les disques de l'ordinateur
def ouvrir_computer(): 
    if os.name == "nt":  # Windows
        disques = [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:\\")]
    else:  # Linux/Mac
        disques = ["/"]  # Sur Linux/Mac, le répertoire racine "/"
    
    tree.delete(*tree.get_children())  # Réinitialiser l'affichage des fichiers
    for disque in disques:  # Ajouter chaque disque dans le Treeview
        tree.insert("", "end", values=(disque, "-", "Disque", "-"), tags=(disque,))

# Fonction pour afficher le contenu d'un disque sélectionné
def afficher_contenu_disque(chemin):
    afficher_fichiers(chemin)  # Affiche les fichiers du répertoire racine du disque


# Fonction pour ouvrir les tags
def ajouter_tag():
    item = tree.selection()  # Récupérer l'élément sélectionné
    if item:
        chemin = tree.item(item, "tags")[0]  # Récupérer le chemin complet
        tag = simpledialog.askstring("Ajouter un tag", "Entrez le nom du tag :")
        
        if tag:
            tag_chemin = os.path.join(chemin_tags, tag)
            
            # Ajouter le chemin du fichier au fichier du tag
            try:
                with open(tag_chemin, 'a') as f:
                    f.write(chemin + '\n')
                messagebox.showinfo("Tag ajouté", f"Le fichier a été ajouté au tag {tag}.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'ajouter le tag : {str(e)}")



# Fonction pour ajouter un fichier/dossier aux favoris
def ajouter_favoris():
    item = tree.selection()
    chemin = tree.item(item, "tags")[0]  # Récupérer le chemin complet
    if chemin not in favoris:
        favoris.append(chemin)
        messagebox.showinfo("Favoris", f"{os.path.basename(chemin)} a été ajouté aux favoris.")
    else:
        messagebox.showinfo("Favoris", f"{os.path.basename(chemin)} est déjà dans les favoris.")

# Création des boutons dans frame_1
btn_recents = tk.Button(frame_1, text="Récents", command=ouvrir_recents)
btn_recents.pack(fill=tk.X, padx=5, pady=5)

btn_favoris = tk.Button(frame_1, text="Favoris", command=ouvrir_favoris)
btn_favoris.pack(fill=tk.X, padx=5, pady=5)

btn_computer = tk.Button(frame_1, text="Computer", command=ouvrir_computer)
btn_computer.pack(fill=tk.X, padx=5, pady=5)

btn_tags = tk.Button(frame_1, text="Tags", command=ouvrir_tags)
btn_tags.pack(fill=tk.X, padx=5, pady=5)


# Fonction pour supprimer un fichier/dossier
def supprimer_fichier():
    item = tree.selection()
    chemin = tree.item(item, "tags")[0]  # Récupérer le chemin complet
    if os.path.isdir(chemin):
        try:
            shutil.rmtree(chemin)  # Supprimer le dossier
            messagebox.showinfo("Suppression", f"Dossier {os.path.basename(chemin)} supprimé.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de supprimer ce dossier : {str(e)}")
    else:
        try:
            os.remove(chemin)  # Supprimer le fichier
            messagebox.showinfo("Suppression", f"Fichier {os.path.basename(chemin)} supprimé.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de supprimer ce fichier : {str(e)}")
    afficher_fichiers(chemin_var.get())

# Fonction pour renommer un fichier/dossier
def renommer_fichier():
    item = tree.selection()
    chemin = tree.item(item, "tags")[0]  # Récupérer le chemin complet
    nouveau_nom = simpledialog.askstring("Renommer", "Entrez le nouveau nom:")
    if nouveau_nom:
        try:
            nouveau_chemin = os.path.join(os.path.dirname(chemin), nouveau_nom)
            os.rename(chemin, nouveau_chemin)
            messagebox.showinfo("Renommage", f"{os.path.basename(chemin)} a été renommé en {nouveau_nom}.")
            afficher_fichiers(chemin_var.get())
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de renommer ce fichier/dossier : {str(e)}")


#Fonction pour créer un nouveau dossier
def creer_nouveau_dossier(chemin_courant): 
    nom_dossier = simpledialog.askstring("Nouveau dossier", "Entrez le nom du dossier :") 
    if nom_dossier: 
        nouveau_dossier = os.path.join(chemin_courant, nom_dossier) 
        try: 
            os.makedirs(nouveau_dossier) 
            messagebox.showinfo("Nouveau dossier", f"Dossier {nom_dossier} créé avec succès.") 
            afficher_fichiers(chemin_courant) 
        except Exception as e: 
            messagebox.showerror("Erreur", f"Impossible de créer ce dossier : {str(e)}")

#Fonction pour afficher le menu contextuel

def afficher_menu_contextuel(event): 
    selection = tree.identify_row(event.y) 
    if selection: 
        tree.selection_set(selection) 
        menu_contextuel.tk_popup(event.x_root, event.y_root)

# Fonction pour afficher le menu contextuel
def menu_contextuel(event): 
    item = tree.selection()  # Récupérer l'élément sélectionné
    if item:
        chemin = tree.item(item, "tags")[0]  # Récupérer le chemin complet
        menu = tk.Menu(fenetre_principale, tearoff=0)
        
        # Ajouter l'option "Ouvrir" au menu contextuel
        menu.add_command(label="Ouvrir", command=lambda: ouvrir_item(chemin))  # Ouvre l'élément sélectionné
        
        # Autres options de menu (Supprimer, Renommer, Ajouter aux favoris)
        menu.add_command(label="Supprimer", command=supprimer_fichier)
        menu.add_command(label="Renommer", command=renommer_fichier)
        menu.add_command(label="Ajouter aux favoris", command=ajouter_favoris)
        
        menu.post(event.x_root, event.y_root)

# Fonction qui ouvre l'élément sélectionné (dossier ou fichier)
def ouvrir_item(chemin):
    if os.path.isdir(chemin):  # Si c'est un dossier
        afficher_fichiers(chemin)  # Affiche le contenu du dossier
    else:  # Si c'est un fichier
        try:
            os.startfile(chemin)  # Ouvre le fichier par défaut
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir ce fichier: {str(e)}")



# Fonction pour gérer l'ouverture par double-clic
def ouvrir_par_double_clic(event):
    item = tree.selection()  # Obtenir l'élément sélectionné
    if item:  # Si un élément est sélectionné
        chemin = tree.item(item, "tags")[0]  # Récupérer le chemin complet
        if os.path.isdir(chemin):  # Si c'est un dossier
            ouvrir_dossier(chemin)
        else:  # Si c'est un fichier
            os.startfile(chemin)  # Ouvre le fichier par défaut
            
# Fonction pour gérer l'ouverture par double-clic        
def ouvrir_par_double_clic(event):
    item = tree.selection()  # Obtenir l'élément sélectionné
    if item:  # Si un élément est sélectionné
        chemin = tree.item(item, "tags")[0]  # Récupérer le chemin complet
        if os.path.isdir(chemin):  # Si c'est un dossier (ou un disque dans ce cas)
            afficher_fichiers(chemin)  # Afficher le contenu du dossier
        else:  # Si c'est un fichier
            try:
                os.startfile(chemin)  # Ouvre le fichier par défaut
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'ouvrir ce fichier: {str(e)}")



# Arborescence des fichiers
colonnes = ("Nom", "Taille", "Type", "Date de Création")  # Nouvelle colonne pour la date
tree = ttk.Treeview(frame_2, columns=colonnes, show='headings')
for col in colonnes:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.pack(fill=tk.BOTH, expand=True)

# Associer l'événement clic droit (Button-3) à la Treeview 
tree.bind("<Button-3>", menu_contextuel)

# Ajouter l'événement pour double-cliquer dans la Treeview
tree.bind("<Double-1>", ouvrir_par_double_clic)


# Charger et afficher les fichiers du répertoire courant
afficher_fichiers(os.getcwd())

fenetre_principale.mainloop()
