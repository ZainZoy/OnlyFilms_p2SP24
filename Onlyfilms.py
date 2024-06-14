from Movie import *
from DesginPatter import *
from tkinter import *
from tkinter import messagebox, font, filedialog, ttk
from PIL._tkinter_finder import tk
from PIL import ImageTk, Image
from tkVideoPlayer import TkinterVideo


class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1920x1080")
        self.root.title("OF🥵")

        self.user_manager = UserManager()

        self.entry1 = None
        self.entry2 = None
        self.entry3 = None
        self.continue_button = None
        self.message_label = None
        self.role_var = None

        self.font_config = font.Font(family="Helvetica", size=16)

        background_image = Image.open("logo.jpg")
        background_image = background_image.resize(size=(1920, 1080))
        self.background_photo = ImageTk.PhotoImage(background_image)

        self.entry_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def exit_app(self):
        self.root.destroy()

    def entry_screen(self):
        self.clear_screen()

        background_label = Label(self.root, image=self.background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        label = Label(self.root, text="Welcome to OnlyFilms", pady=30, fg="white", bg="#0C5057", font=self.font_config)
        label.pack(anchor="n")

        label1 = Label(self.root, text="Click here to sign up", fg="white", bg="#0C5057", pady=5, font=self.font_config)
        button = Button(self.root, text="Sign Up", command=self.signup, width=20, font=self.font_config)
        label1.pack()
        button.pack()

        label2 = Label(self.root, text="Click here to sign in", fg="white", bg="#0C5057", pady=10,
                       font=self.font_config)
        button1 = Button(self.root, text="Sign In", width=20, font=self.font_config, command=self.login)
        label2.pack()
        button1.pack()

        exit_button = Button(self.root, text="Exit", width=20, command=self.exit_app, font=self.font_config)
        exit_button.place(relx=0.5, rely=0.8, anchor="center")

    def toggle_password_visibility(self, entry, button):
        if entry.cget('show') == '*':
            entry.config(show='')
            button.config(text='Hide Password')

        else:
            entry.config(show='*')
            button.config(text='Show Password')

    def check_fields(self, *args):
        if self.entry1.get() and self.entry2.get() and self.entry3.get():
            self.continue_button.pack()

        else:
            self.continue_button.pack_forget()

    def save_info(self):
        username = self.entry1.get()
        password = self.entry2.get()
        confirm_password = self.entry3.get()
        role = self.role_var.get()

        if self.user_manager.username_exists(username):
            messagebox.showerror("Error", "Username already taken!")
            return

        if password == confirm_password:
            user = User(username, password, role)
            self.user_manager.add_user(user)

            with open("user_info.txt", "a") as file:
                file.write(f"Username: {username}, Password: {password}, Role: {role}\n")
            self.message_label.config(text="Sign-up successful!", fg="green")

            self.entry1.delete(0, END)
            self.entry2.delete(0, END)
            self.entry3.delete(0, END)

            self.role_var.set("viewing user")

        else:
            messagebox.showerror("Error", "Passwords do not match!")

    def signup(self):
        self.clear_screen()

        background_label = Label(self.root, image=self.background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        back_button = Button(self.root, text="Back", fg="white", bg="#0C5057", command=self.entry_screen,
                             font=self.font_config)
        back_button.pack(anchor="nw")
        label = Label(self.root, text="Sign up Window", fg="white", bg="#0C5057", font=self.font_config)
        label.pack(anchor="n")

        label1 = Label(self.root, text="Username", fg="white", bg="#0C5057", font=self.font_config)
        label1.pack()
        self.entry1 = Entry(self.root, font=self.font_config)
        self.entry1.pack()
        self.entry1.bind("<KeyRelease>", self.check_fields)

        label2 = Label(self.root, text="Password", fg="white", bg="#0C5057", font=self.font_config)
        label2.pack()
        self.entry2 = Entry(self.root, show="*", font=self.font_config)
        self.entry2.pack()
        self.entry2.bind("<KeyRelease>", self.check_fields)

        label3 = Label(self.root, text="Confirm Password", fg="white", bg="#0C5057", font=self.font_config)
        label3.pack()
        self.entry3 = Entry(self.root, show="*", font=self.font_config)
        self.entry3.pack()
        self.entry3.bind("<KeyRelease>", self.check_fields)

        toggle_password_button = Button(self.root, text="Show Password",
                                        command=lambda: self.toggle_password_visibility(self.entry2,
                                                                                        toggle_password_button),
                                        font=self.font_config)
        toggle_password_button.place(relx=0.65, rely=0.2)

        toggle_confirm_password_button = Button(self.root, text="Show Password",
                                                command=lambda: self.toggle_password_visibility(self.entry3,
                                                                                                toggle_confirm_password_button),
                                                font=self.font_config)
        toggle_confirm_password_button.place(relx=0.65, rely=0.28)

        self.continue_button = Button(self.root, text="Continue", command=self.save_info, font=self.font_config)
        self.continue_button.pack_forget()

        self.message_label = Label(self.root, text="", fg="white", bg="#0C5057", font=self.font_config)
        self.message_label.pack(pady=10)

        exit_button = Button(self.root, text="Exit", width=20, command=self.exit_app, font=self.font_config)
        exit_button.place(relx=0.5, rely=0.9, anchor="center")

        self.role_var = StringVar(value="viewing user")
        admin_checkbox = Checkbutton(self.root, text="Admin", width=11, variable=self.role_var, onvalue="admin",
                                     offvalue="viewing user", font=self.font_config)
        admin_checkbox.place(relx=0.65, rely=.12)

    def check_credentials(self):
        self.username = self.entry1.get()
        self.password = self.entry2.get()
        role = self.role_var.get()

        if not self.username or not self.password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        for user in self.user_manager.users:

            if user.username == self.username:

                if user.password == self.password:

                    if user.role == role:
                        messagebox.showinfo("Success", f"Login successful as {role}!")
                        self.entry1.delete(0, END)
                        self.entry2.delete(0, END)
                        self.role_var.set("viewing user")
                        self.open_dashboard(role)
                        return
                    
                    else:
                        messagebox.showerror("Error", "Role mismatch.")
                        return
                    
                else:
                    messagebox.showerror("Error", "Invalid password.")
                    return
        messagebox.showerror("Error", "Invalid username or password.")

    def login(self):
        self.clear_screen()

        background_label = Label(self.root, image=self.background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        back_button = Button(self.root, text="Back", fg="white", bg="#0C5057", command=self.entry_screen,
                             font=self.font_config)
        back_button.pack(anchor="nw")
        label = Label(self.root, text="Sign In Window", fg="white", bg="#0C5057", font=self.font_config)
        label.pack(anchor="n")

        label1 = Label(self.root, text="Username", fg="white", bg="#0C5057", font=self.font_config)
        label1.pack()
        self.entry1 = Entry(self.root, font=self.font_config)
        self.entry1.pack()

        label2 = Label(self.root, text="Password", fg="white", bg="#0C5057", font=self.font_config)
        label2.pack()
        self.entry2 = Entry(self.root, show="*", font=self.font_config)
        self.entry2.pack()

        toggle_password_button = Button(self.root, text="Show Password",
                                        command=lambda: self.toggle_password_visibility(self.entry2,
                                                                                        toggle_password_button),
                                        font=self.font_config)
        toggle_password_button.place(relx=0.65, rely=0.2)

        login_button = Button(self.root, text="Login", command=self.check_credentials, font=self.font_config)
        login_button.pack(pady=10)

        exit_button = Button(self.root, text="Exit", width=20, command=self.exit_app, font=self.font_config)
        exit_button.place(relx=0.5, rely=0.9, anchor="center")

        self.role_var = StringVar(value="viewing user")
        admin_checkbox = Checkbutton(self.root, text="Admin", width=11, variable=self.role_var, onvalue="admin",
                                     offvalue="viewing user", font=self.font_config)
        admin_checkbox.place(relx=0.65, rely=.13)

    def open_dashboard(self, role):
        self.clear_screen()

        background_label = Label(self.root, image=self.background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        if role == "admin":
            custom_font = font.Font(family="Helvetica", size=25)
            label = Label(self.root, text=f"Admin Dashboard ({self.username})", fg="white", bg="#0C5057",
                          font=custom_font)
            label.pack(anchor="n")
            button1 = Button(self.root, text="Add Movie", width=20, font=self.font_config,
                             command=self.add_movie_screen)
            button1.pack(pady=10, padx=20, anchor="w")
            button2 = Button(self.root, text="Remove Movie", width=20, font=self.font_config,
                             command=self.remove_movie_screen)
            button2.pack(pady=10, padx=20, anchor="w")
            button3 = Button(self.root, text="View Library", width=20, font=self.font_config, command = self.view_all_movies_screen_admin)
            button3.pack(pady=10, padx=20, anchor="w")

        else:
            custom_font = font.Font(family="Helvetica", size=25)
            label = Label(self.root, text=f"User Dashboard ({self.username})", fg="white", bg="#0C5057",
                          font=custom_font)
            label.pack(anchor="n")
            button1 = Button(self.root, text="View All Movies", width=20, font=self.font_config,
                             command=self.view_all_movies_screen)
            button1.pack(pady=10, padx=20, anchor="w")
            button2 = Button(self.root, text="Watch History", command=self.display_watchhistory, width=20,
                             font=self.font_config)
            button2.pack(pady=10, padx=20, anchor="w")
            button4 = Button(self.root, text="Favourites", command=self.display_Favourites, width=20,
                             font=self.font_config)
            button4.pack(pady=10, padx=20, anchor="w")

        exit_button = Button(self.root, text="Logout", width=20, command=self.entry_screen, font=self.font_config)
        exit_button.pack(pady=20, padx=20, anchor="w")

    def add_movie_screen(self):
        self.clear_screen()

        background_label = Label(self.root, image=self.background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        custom_font = font.Font(family="Helvetica", size=25)
        label = Label(self.root, text="Add Movie", fg="white", bg="#0C5057", font=custom_font)
        label.pack(anchor="n", pady=10, padx=20)

        label1 = Label(self.root, text="Movie Name", fg="white", bg="#0C5057", font=self.font_config)
        label1.pack(pady=10, padx=20, anchor="w")
        self.entry_movie_name = Entry(self.root, font=self.font_config)
        self.entry_movie_name.pack(pady=10, padx=20, anchor="w")

        label2 = Label(self.root, text="Description", fg="white", bg="#0C5057", font=self.font_config)
        label2.pack(pady=10, padx=20, anchor="w")
        self.entry_description = Entry(self.root, font=self.font_config)
        self.entry_description.pack(pady=10, padx=20, anchor="w")

        label3 = Label(self.root, text="Duration", fg="white", bg="#0C5057", font=self.font_config)
        label3.pack(pady=10, padx=20, anchor="w")
        self.entry_duration = Entry(self.root, font=self.font_config)
        self.entry_duration.pack(pady=10, padx=20, anchor="w")

        label4 = Label(self.root, text="Genre", fg="white", bg="#0C5057", font=self.font_config)
        label4.pack(pady=10, padx=20, anchor="w")
        self.genre_var = StringVar()
        genres = ["Horror", "Comedy", "Action", "Romance","Sports", "Sci-Fi", "Documentary", "Nature"]
        self.combobox_genre = ttk.Combobox(self.root, textvariable=self.genre_var, values=genres, font=self.font_config)
        self.combobox_genre.pack(pady=10, padx=20, anchor="w")

        label5 = Label(self.root, text="Select Movie File", fg="white", bg="#0C5057", font=self.font_config)
        label5.pack(pady=10, padx=20, anchor="w")
        self.movie_file_path = StringVar()
        select_movie_button = Button(self.root, text="Select Movie", command=self.select_movie_file,
                                     font=self.font_config)
        select_movie_button.pack(pady=10, padx=20, anchor="w")

        self.selected_file_label = Label(self.root, text="", fg="white", bg="#0C5057", font=self.font_config)
        self.selected_file_label.pack(pady=10, padx=20, anchor="w")

        save_button = Button(self.root, text="Save", command=self.save_movie, font=self.font_config)
        save_button.pack(pady=10, padx=20, anchor="w")

        exit_button = Button(self.root, text="Cancel", command=self.open_dashboard_admin, font=self.font_config)
        exit_button.pack(pady=10, padx=20, anchor="w")

    def select_movie_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.mkv *.avi")])
        if file_path:
            self.movie_file_path.set(file_path)
            self.selected_file_label.config(text=f"Selected File: {file_path}")

    def save_movie(self):
        movie_name = self.entry_movie_name.get()
        description = self.entry_description.get()
        duration = self.entry_duration.get()
        genre = self.genre_var.get()
        movie_file = self.movie_file_path.get()
        create_movie = Movie(movie_name, description, duration, genre, movie_file)

        if not movie_name or not description or not duration or not genre or not movie_file:
            messagebox.showerror("Error", "Please fill all fields and select a movie file.")
            return

        try:
            with open("movies.txt", "r") as file:
                movies = file.readlines()

                for movie in movies:

                    if f"Movie Name: {movie_name}," in movie:
                        messagebox.showerror("Error", "Movie already exists!")
                        return 
                    
        except FileNotFoundError:
            pass

        with open("movies.txt", "a") as file:
            file.write(f"Movie Name: {create_movie.movie_name}, Description: {create_movie.description}, Duration: {create_movie.duration}, Genre: {create_movie.genre}, File Path: {create_movie.movie_file}\n")

        messagebox.showinfo("Success", "Movie added successfully!")

        self.entry_movie_name.delete(0, END)
        self.entry_description.delete(0, END)
        self.entry_duration.delete(0, END)
        self.combobox_genre.set("")
        self.selected_file_label.config(text="")
        self.movie_file_path.set("")

    def remove_movie_screen(self):
        self.clear_screen()

        background_label = Label(self.root, image=self.background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        custom_font = font.Font(family="Helvetica", size=25)
        label = Label(self.root, text="Remove Movie", fg="white", bg="#0C5057", font=custom_font)
        label.pack(anchor="n", pady=10, padx=20)

        label1 = Label(self.root, text="Movie Name", fg="white", bg="#0C5057", font=self.font_config)
        label1.pack(pady=10, padx=20, anchor="w")
        self.entry_movie_name_remove = Entry(self.root, font=self.font_config)
        self.entry_movie_name_remove.pack(pady=10, padx=20, anchor="w")

        remove_button = Button(self.root, text="Remove", command=self.remove_movie, font=self.font_config)
        remove_button.pack(pady=10, padx=20, anchor="w")

        exit_button = Button(self.root, text="Cancel", command=self.open_dashboard_admin, font=self.font_config)
        exit_button.pack(pady=10, padx=20, anchor="w")

    def remove_movie(self):
        movie_name = self.entry_movie_name_remove.get()

        if not movie_name:
            messagebox.showerror("Error", "Please enter the movie name.")
            return

        with open("movies.txt", "r") as file:
            lines = file.readlines()

        with open("movies.txt", "w") as file:
            found = False
            for line in lines:

                if movie_name not in line:
                    file.write(line)

                else:
                    found = True

        if found:
            messagebox.showinfo("Success", f"Movie '{movie_name}' removed successfully!")

        else:
            messagebox.showerror("Error", f"Movie '{movie_name}' not found.")

    def open_dashboard_admin(self):
        self.clear_screen()
        self.open_dashboard("admin")

    def view_all_movies_screen(self):
        new_window = Toplevel(self.root)
        new_window.geometry("800x600")
        new_window.title("View All Movies")

        background_label = Label(new_window, image=self.background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        back_button = Button(new_window, text="Back", fg="white", bg="#0C5057", command=new_window.destroy,
                             font=self.font_config)
        back_button.pack(anchor="nw")

        label = Label(new_window, text="All Movies", fg="white", bg="#0C5057", font=self.font_config)
        label.pack(anchor="n")

        movies_frame = Frame(new_window, bg="#0C5057")
        movies_frame.pack(fill=BOTH, expand=True)

        movies_canvas = Canvas(movies_frame, bg="#0C5057")
        scrollbar = Scrollbar(movies_frame, orient=VERTICAL, command=movies_canvas.yview)
        scrollable_frame = Frame(movies_canvas, bg="#0C5057")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: movies_canvas.configure(
                scrollregion=movies_canvas.bbox("all")
            )
        )

        movies_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        movies_canvas.configure(yscrollcommand=scrollbar.set)

        with open("movies.txt", "r") as file:
            for line in file:
                parts = line.strip().split(", ")

                if len(parts) == 5:
                    movie_name, description, duration, genre, file_path = parts

                    if file_path.startswith("File Path: "):
                        file_path = file_path[len("File Path: "):]

                    movie_frame = Frame(scrollable_frame, bg="#0C5057", bd=2, relief=SOLID)
                    movie_frame.pack(fill=X, padx=10, pady=5)

                    movie_label = Label(movie_frame, text=f"{movie_name}\n{duration}\n{description}\n{genre}",
                                        fg="white", bg="#0C5057", justify=LEFT, font=self.font_config)
                    movie_label.pack(side=LEFT, padx=10)

                    Favourites_button = Button(movie_frame, text="Add to Favourites",
                                               command=lambda mn=movie_name: self.add_to_Favourites(mn),
                                               font=self.font_config)
                    Favourites_button.pack(side=LEFT, padx=5)

                    play_button = Button(movie_frame, text="Play", command=lambda fp=file_path: self.play_movie(fp),
                                         font=self.font_config)
                    play_button.pack(side=LEFT, padx=5)

        movies_canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

    def view_all_movies_screen_admin(self):
        new_window = Toplevel(self.root)
        new_window.geometry("800x600")
        new_window.title("View All Movies")

        background_label = Label(new_window, image=self.background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        back_button = Button(new_window, text="Back", fg="white", bg="#0C5057", command=new_window.destroy,
                             font=self.font_config)
        back_button.pack(anchor="nw")

        label = Label(new_window, text="All Movies", fg="white", bg="#0C5057", font=self.font_config)
        label.pack(anchor="n")

        movies_frame = Frame(new_window, bg="#0C5057")
        movies_frame.pack(fill=BOTH, expand=True)

        movies_canvas = Canvas(movies_frame, bg="#0C5057")
        scrollbar = Scrollbar(movies_frame, orient=VERTICAL, command=movies_canvas.yview)
        scrollable_frame = Frame(movies_canvas, bg="#0C5057")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: movies_canvas.configure(
                scrollregion=movies_canvas.bbox("all")
            )
        )

        movies_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        movies_canvas.configure(yscrollcommand=scrollbar.set)

        with open("movies.txt", "r") as file:
            for line in file:
                parts = line.strip().split(", ")

                if len(parts) == 5:
                    movie_name, description, duration, genre, file_path = parts

                    if file_path.startswith("File Path: "):
                        file_path = file_path[len("File Path: "):]

                    movie_frame = Frame(scrollable_frame, bg="#0C5057", bd=2, relief=SOLID)
                    movie_frame.pack(fill=X, padx=10, pady=5)

                    movie_label = Label(movie_frame, text=f"{movie_name}\n{duration}\n{description}\n{genre}",
                                        fg="white", bg="#0C5057", justify=LEFT, font=self.font_config)
                    movie_label.pack(side=LEFT, padx=10)

        movies_canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

    def add_to_Favourites(self, movie_name):
        is_already_in_Favourites = False

        with open("Favourites.txt", "r") as file:
            for line in file:

                if line.strip() == movie_name: 
                    is_already_in_Favourites = True

                    break 

        if is_already_in_Favourites:
            messagebox.showinfo("Information", f"{movie_name} is already in your Favourites!")

        else:
            with open("Favourites.txt", "a") as file:
                file.write(movie_name + "\n")
            messagebox.showinfo("Success", "Movie added to Favourites!")


    def delete_history(self, refresh_callback):
        with open("watch_history.txt", "w") as file:
            file.write("")

        print("Watch history cleared")
        refresh_callback()

    def display_watchhistory(self):
        def refresh_window():
            for widget in new_window.winfo_children():
                widget.destroy()

            self.display_watchhistory()

        new_window = Toplevel(self.root)
        new_window.geometry("800x600")
        new_window.title("Watch History")

        background_label = Label(new_window, image=self.background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        back_button = Button(new_window, text="Back", fg="white", bg="#0C5057", command=new_window.destroy,
                             font=self.font_config)
        back_button.pack(anchor="nw")

        label = Label(new_window, text="Watch History", fg="white", bg="#0C5057", font=self.font_config)
        label.pack(anchor="n")

        movies_frame = Frame(new_window, bg="#0C5057")
        movies_frame.pack(fill=BOTH, expand=True)

        movies_canvas = Canvas(movies_frame, bg="#0C5057")
        scrollbar = Scrollbar(movies_frame, orient=VERTICAL, command=movies_canvas.yview)
        scrollable_frame = Frame(movies_canvas, bg="#0C5057")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: movies_canvas.configure(
                scrollregion=movies_canvas.bbox("all")
            )
        )

        movies_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        movies_canvas.configure(yscrollcommand=scrollbar.set)

        movie_names = []
        with open("watch_history.txt", "r") as file:
            for line in file:
                movie_names.append(line.strip())

        if movie_names:
            for movie_name in movie_names:
                movie_frame = Frame(scrollable_frame, bg="#0C5057", bd=2, relief=SOLID)
                movie_frame.pack(fill=X, padx=10, pady=5)

                movie_label = Label(movie_frame, text=movie_name, fg="white", bg="#0C5057",
                                    justify=LEFT, font=self.font_config)
                movie_label.pack(side=LEFT, padx=10)

        else:
            no_movies_label = Label(scrollable_frame, text="No movies found in watch history.",
                                    fg="white", bg="#0C5057", font=self.font_config)
            no_movies_label.pack(padx=10, pady=10)

        movies_canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        delete_button = Button(new_window, text="Delete History", fg="white", bg="#0C5057",
                               command=lambda: self.delete_history(refresh_window), font=self.font_config)
        delete_button.pack(anchor="ne", padx=10, pady=10)


    def display_Favourites(self):
        new_window = Toplevel(self.root)
        new_window.geometry("600x400")
        new_window.title("Favourites")

        background_label = Label(new_window, image=self.background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        back_button = Button(new_window, text="Back", fg="white", bg="#0C5057", command=new_window.destroy,
                             font=self.font_config)
        back_button.pack(anchor="nw")

        label = Label(new_window, text="Favourites", fg="white", bg="#0C5057", font=self.font_config)
        label.pack(anchor="n")

        movies_frame = Frame(new_window, bg="#0C5057")
        movies_frame.pack(fill=BOTH, expand=True)

        movies_canvas = Canvas(movies_frame, bg="#0C5057")
        scrollbar = Scrollbar(movies_frame, orient=VERTICAL, command=movies_canvas.yview)
        scrollable_frame = Frame(movies_canvas, bg="#0C5057")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: movies_canvas.configure(
                scrollregion=movies_canvas.bbox("all")
            )
        )

        movies_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        movies_canvas.configure(yscrollcommand=scrollbar.set)

        movie_names = []
        with open("Favourites.txt", "r") as file:
            for line in file:
                movie_names.append(line.strip())

        if movie_names:
            for movie_name in movie_names:
                movie_frame = Frame(scrollable_frame, bg="#0C5057", bd=2, relief=SOLID)
                movie_frame.pack(fill=X, padx=10, pady=5)

                movie_label = Label(movie_frame, text=movie_name, fg="white", bg="#0C5057",
                                    justify=LEFT, font=self.font_config)
                movie_label.pack(side=LEFT, padx=10)

        else:
            no_movies_label = Label(scrollable_frame, text="No movies in Favourites yet.",
                                    fg="white", bg="#0C5057", font=self.font_config)
            no_movies_label.pack(padx=10, pady=10)

        movies_canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

    def play_movie(self, file_path):
        if not file_path:
            print("No movie file path provided.")
            return

        self.clear_screen()

        self.video_player = TkinterVideo(master=self.root, scaled=True)
        self.video_player.load(file_path)
        self.video_player.pack(expand=True, fill="both")
        self.video_player.play()

        movie_name = self.get_movie_name_from_file(file_path)

        with open("watch_history.txt", "a") as file:
            file.write(f"{movie_name}\n")

        back_button = Button(self.root, text="Back", fg="white", bg="#0C5057", command=self.entry_screen,
                             font=self.font_config)
        back_button.pack(anchor="nw")

        pause_button = Button(self.root, text="Pause", width=7, command=self.video_player.pause, font=self.font_config)
        pause_button.place(relx=0.48, rely=0.96, anchor="s")

        play_button = Button(self.root, text="Play", width=7, command=self.video_player.play, font=self.font_config)
        play_button.place(relx=0.55, rely=0.96, anchor="s")

        skip_backward_button = Button(self.root, text="start", width=7, command=self.skip_backward,
                                      font=self.font_config)
        skip_backward_button.place(relx=0.35, rely=0.96, anchor="s")

        skip_forward_button = Button(self.root, text="end", width=7, command=self.skip_forward, font=self.font_config)
        skip_forward_button.place(relx=0.65, rely=0.96, anchor="s")

        # self.time_label = tk.Label(self.root, text="00:00 / 00:00", font=self.font_config)
        # self.time_label.place(relx=0.5, rely=0.9, anchor="s")
        #
        # self.time_slider = ttk.Scale(self.root, from_=0, to=1, orient="horizontal", command=self.on_slider_move)
        # self.time_slider.place(relx=0.5, rely=0.88, anchor="s", relwidth=0.8)

    def get_movie_name_from_file(self, file_path):
        with open("movies.txt", "r") as file:
            for line in file:
                parts = line.strip().split(", ")

                if len(parts) == 5 and parts[-1].startswith("File Path: "): 
                    movie_file_path = parts[-1][len("File Path: "):].strip()

                    if movie_file_path == file_path:
                        return parts[0]
                    
        return "Movie Name Unavailable"

    def skip_backward(self):
        current_time = self.video_player.current_duration()
        new_time = max(0, int(current_time) - 5000)
        self.video_player.seek(new_time)
        self.update_scale()

    def skip_forward(self, value=10000): 
        try:
            current_time = self.video_player.current_duration()
            print(f"Current time: {current_time}") 
            new_time = min(self.video_player.video_info()['duration'], current_time + value)
            print(f"New time: {new_time}") 
            self.video_player.seek(new_time)
            self.update_scale()

        except Exception as e:
            print(f"Error in skip_forward: {e}")

    # def update_time(self):
    #     if self.video_player:
    #         self.update_scale()
    #         self.root.after(500, self.update_time)

    # def on_slider_move(self, val):
    #     self.video_player.seek(int(float(val)))
    #     self.update_scale()

root = Tk()
app = App(root)
root.mainloop()

