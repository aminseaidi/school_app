import sqlite3
import customtkinter as ctk
from tkinter import messagebox
import os
# این خط رو اضافه کن
from kivy.core.window import Window
from kivy.utils import platform

# اگر روی گوشی بود، تمام صفحه بشه
if platform == 'android':
    Window.maximize()
# --- تنظیمات ظاهری ---
ctk.set_appearance_mode("light")  
ctk.set_default_color_theme("blue") 

BG_COLOR = "#f8fafc"
HEADER_BG = "#0f172a"
CARD_COLOR = "#ffffff"
TEXT_TITLE = "#1e293b"
TEXT_BODY = "#475569"
ACCENT_COLOR = "#3b82f6"
HIGHLIGHT = "#e0f2fe"

# حذف دیتابیس قدیمی برای پاک شدن کادرهای مزاحم
if os.path.exists('school_app.db'):
    os.remove('school_app.db')

def init_db():
    conn = sqlite3.connect('school_app.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, role TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS cards 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, page_name TEXT, title TEXT, text TEXT)''')
    
    c.execute("INSERT INTO users (username, password, role) VALUES ('admin', '1234', 'admin')")
    
    defaults = [
        ('home', '🎯 ما کی هستیم', 'مدرسه دولتی پسرانه آریو مصلی‌نژاد در ارومیه'),
        ('home', '💻 طراح برنامه', 'محمد امین سعیدی و امیرعباس قاسمی\nآیدی ایتا: @amin_hr\nآیدی روبیکا: @AMINHANDALA'),
        ('home', '📚 روش ما', 'ترکیبی از آموزش منظم و فعالیت‌های دانش‌آموزی در فضایی دوستانه.'),
        ('about', '🏫 تاریخچه مدرسه', 'مدرسه ما با سال‌ها تجربه در زمینه آموزش در خدمت شماست.'),
        ('about', '🎯 اهداف ما', 'تربیت نسلی پویا، خلاق و متعهد برای ساختن آینده‌ای روشن‌تر.'),
        ('about', '🌟 افتخارات', 'کسب رتبه‌های برتر استانی در المپیادهای علمی و ورزشی.'),
        ('staff', '👨‍🏫 جناب آقای سلاطین', 'مدیر مدرسه'),
        ('staff', '👨‍💼 جناب آقای الوانی', 'معاون آموزشی'),
        ('staff', '👨‍🏫 کادر آموزشی', 'دبیران مجرب و دلسوز مدرسه'),
        ('act', '🏆 المپیاد ورزشی', 'رقابت سالم بین کلاس‌ها.'),
        ('act', '📰 نشریه دانش‌آموزی', 'قلم و ایده دانش‌آموزان در قالب نشریه.'),
        ('act', '🎭 گروه هنری و تئاتر', 'اجرای نمایش‌های زیبا در مناسبت‌های مختلف.'),
        ('act', '🔬 انجمن علمی', 'برگزاری کارگاه‌های رباتیک و علوم آزمایشگاهی.'),
        ('news', '🎉 روز دانش‌آموز', 'روز دانش‌آموز، روز تجلیل از آینده‌سازان است.'),
        ('news', '📢 اطلاعیه ثبت‌نام', 'ثبت‌نام کلاس‌های تابستانی آغاز شد.'),
        ('contact', '📞 تماس با ما', 'شماره تماس: ۰۴۴-۳۸۶۸۷۶۸۶'),
        ('contact', '📍 آدرس', 'ارومیه، محله بازار باش، میدان جانبازان')
    ]
    for page, t, txt in defaults:
        c.execute("INSERT INTO cards (page_name, title, text) VALUES (?, ?, ?)", (page, t, txt))
            
    conn.commit()
    conn.close()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("مدرسه آریو مصلی‌نژاد")
        self.geometry("550x850") 
        self.configure(fg_color=BG_COLOR)
        
        self.current_user_role = None
        self.current_page = "home"
        
        init_db()
        
        self.header_frame = ctk.CTkFrame(self, fg_color=HEADER_BG, corner_radius=0, height=180)
        self.header_frame.pack(fill="x", side="top")
        self.header_frame.pack_propagate(False)
        
        self.main_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scroll.pack(fill="both", expand=True, padx=0, pady=0)

        self.build_header_content()
        self.show_page("home") 

    def build_header_content(self):
        for w in self.header_frame.winfo_children():
            w.destroy()
            
        ctk.CTkLabel(self.header_frame, text="مدرسه آریو مصلی‌نژاد", font=("Vazirmatn", 26, "bold"), text_color="#ffffff").pack(pady=(25, 0))
        ctk.CTkLabel(self.header_frame, text="ارومیه • دولتی", font=("Vazirmatn", 13), text_color="#94a3b8").pack()
        
        nav_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        nav_frame.pack(fill="x", padx=10, pady=(15, 10))
        pages = [("home", "خانه"), ("about", "درباره ما"), ("staff", "کادر"), ("act", "فعالیت‌ها"), ("news", "اخبار"), ("contact", "تماس")]
        
        for i, (p_name, p_text) in enumerate(pages):
            btn = ctk.CTkButton(nav_frame, text=p_text, width=60, height=32, font=("Vazirmatn", 13), 
                                fg_color=ACCENT_COLOR if self.current_page == p_name else "#334155", 
                                text_color="#ffffff", hover_color=ACCENT_COLOR,
                                corner_radius=8, command=lambda p=p_name: self.show_page(p))
            btn.grid(row=i//3, column=i%3, padx=4, pady=4, sticky="ew")
        
        nav_frame.grid_columnconfigure(0, weight=1)
        nav_frame.grid_columnconfigure(1, weight=1)
        nav_frame.grid_columnconfigure(2, weight=1)

    def show_page(self, page_name):
        self.current_page = page_name
        self.build_header_content()
        
        for widget in self.main_scroll.winfo_children():
            widget.destroy()

        titles = {"home": "جایی که درس، ایده و حال خوب کنار هم می‌نشینند.", 
                  "about": "درباره مدرسه", "staff": "کادر مدرسه", 
                  "act": "فعالیت‌های آموزشی", "news": "اخبار مدرسه", "contact": "تماس با ما"}
        
        title_frame = ctk.CTkFrame(self.main_scroll, fg_color=HIGHLIGHT, corner_radius=20)
        title_frame.pack(fill="x", pady=15, padx=15)
        
        lbl = ctk.CTkLabel(title_frame, text=titles[page_name], font=("Vazirmatn", 20, "bold"), text_color=TEXT_TITLE, wraplength=400, justify="center")
        lbl.pack(pady=20, padx=20)

        conn = sqlite3.connect('school_app.db')
        c = conn.cursor()
        c.execute("SELECT id, title, text FROM cards WHERE page_name=?", (page_name,))
        items = c.fetchall()
        conn.close()

        for card_id, t, txt in items:
            card = ctk.CTkFrame(self.main_scroll, fg_color=CARD_COLOR, corner_radius=15, border_width=1, border_color="#e2e8f0")
            card.pack(fill="x", pady=10, padx=20)
            
            ctk.CTkLabel(card, text=t, font=("Vazirmatn", 18, "bold"), text_color=TEXT_TITLE, anchor="e").pack(pady=(15, 5), padx=20, fill="x")
            ctk.CTkLabel(card, text=txt, font=("Vazirmatn", 15), text_color=TEXT_BODY, anchor="e", justify="right", wraplength=400).pack(pady=(0, 15), padx=20, fill="x")
            
            # دکمه حذف فقط برای ادمین
            if self.current_user_role == 'admin':
                ctk.CTkButton(card, text="🗑️ حذف کادر", font=("Vazirmatn", 12), fg_color="#ef4444", height=30, width=100, 
                              command=lambda cid=card_id, p=page_name: self.delete_card(cid, p)).pack(pady=(0, 15))

        auth_btn = ctk.CTkButton(self.main_scroll, text="خروج از حساب" if self.current_user_role else "ورود / ثبت‌نام", 
                                 font=("Vazirmatn", 16, "bold"), height=50, corner_radius=12,
                                 fg_color="#ef4444" if self.current_user_role else ACCENT_COLOR,
                                 hover_color="#dc2626" if self.current_user_role else "#2563eb",
                                 command=self.logout if self.current_user_role else self.show_auth)
        auth_btn.pack(fill="x", pady=30, padx=20)

        if self.current_user_role == 'admin':
            self.build_admin_form(page_name)

    def delete_card(self, card_id, page_name):
        if messagebox.askyesno("تایید", "آیا از حذف این کادر مطمئن هستید؟"):
            conn = sqlite3.connect('school_app.db')
            c = conn.cursor()
            c.execute("DELETE FROM cards WHERE id=?", (card_id,))
            conn.commit()
            conn.close()
            self.show_page(page_name)

    def build_admin_form(self, page_name):
        admin_frame = ctk.CTkFrame(self.main_scroll, fg_color="#f1f5f9", corner_radius=15, border_width=2, border_color=ACCENT_COLOR)
        admin_frame.pack(fill="x", pady=10, padx=20)
        
        ctk.CTkLabel(admin_frame, text="⚙️ پنل مدیریت (افزودن کادر جدید)", font=("Vazirmatn", 16, "bold"), text_color=ACCENT_COLOR).pack(pady=15)
        
        self.new_title = ctk.CTkEntry(admin_frame, placeholder_text="عنوان کادر جدید", font=("Vazirmatn", 15), height=45, corner_radius=10)
        self.new_title.pack(fill="x", pady=5, padx=20)
        
        self.new_text = ctk.CTkTextbox(admin_frame, font=("Vazirmatn", 15), height=100, corner_radius=10)
        self.new_text.pack(fill="x", pady=5, padx=20)
        
        ctk.CTkButton(admin_frame, text="➕ ذخیره کادر جدید", font=("Vazirmatn", 15, "bold"), fg_color="#10b981", hover_color="#059669", height=45, corner_radius=10, command=lambda: self.add_card(page_name)).pack(fill="x", pady=15, padx=20)

    def add_card(self, page_name):
        t = self.new_title.get()
        txt = self.new_text.get("0.0", "end-1c").strip()
        
        if t and txt:
            conn = sqlite3.connect('school_app.db')
            c = conn.cursor()
            c.execute("INSERT INTO cards (page_name, title, text) VALUES (?, ?, ?)", (page_name, t, txt))
            conn.commit()
            conn.close()
            messagebox.showinfo("موفقیت", "کادر جدید اضافه شد!")
            self.show_page(page_name) 
        else:
            messagebox.showwarning("هشدار", "لطفا عنوان و متن را پر کنید.")

    def show_auth(self):
        auth_win = ctk.CTkToplevel(self)
        auth_win.title("ورود / ثبت‌نام")
        auth_win.geometry("400x600") # ارتفاع بیشتر برای جایگیری بهتر
        auth_win.attributes("-topmost", True)
        auth_win.configure(fg_color=BG_COLOR)
        
        # استفاده از یک فریم برای زیبایی بیشتر
        main_frame = ctk.CTkFrame(auth_win, fg_color=CARD_COLOR, corner_radius=20)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # ------- ورود -------
        ctk.CTkLabel(main_frame, text="ورود به سیستم", font=("Vazirmatn", 20, "bold"), text_color=TEXT_TITLE).pack(pady=(20, 10))
        
        user_entry_login = ctk.CTkEntry(main_frame, placeholder_text="نام کاربری", font=("Vazirmatn", 15), height=45, corner_radius=10, fg_color="#f8fafc", text_color="black")
        user_entry_login.pack(fill="x", padx=30, pady=8)
        
        pass_entry_login = ctk.CTkEntry(main_frame, placeholder_text="رمز عبور", show="*", font=("Vazirmatn", 15), height=45, corner_radius=10, fg_color="#f8fafc", text_color="black")
        pass_entry_login.pack(fill="x", padx=30, pady=8)
        
        def do_login():
            conn = sqlite3.connect('school_app.db')
            c = conn.cursor()
            c.execute("SELECT role FROM users WHERE username=? AND password=?", (user_entry_login.get(), pass_entry_login.get()))
            res = c.fetchone()
            conn.close()
            if res:
                self.current_user_role = res[0]
                auth_win.destroy()
                self.show_page(self.current_page)
                messagebox.showinfo("خوش آمدید", f"شما به عنوان {self.current_user_role} وارد شدید.")
            else:
                messagebox.showerror("خطا", "نام کاربری یا رمز عبور اشتباه است!", parent=auth_win)

        ctk.CTkButton(main_frame, text="ورود", font=("Vazirmatn", 16, "bold"), fg_color=ACCENT_COLOR, height=45, corner_radius=10, command=do_login).pack(fill="x", padx=30, pady=(10, 20))
        
        # جداکننده
        ctk.CTkLabel(main_frame, text="— یا —", font=("Vazirmatn", 14), text_color="#94a3b8").pack(pady=5)
        
        # ------- ثبت‌نام -------
        ctk.CTkLabel(main_frame, text="ساخت حساب جدید", font=("Vazirmatn", 18, "bold"), text_color=TEXT_TITLE).pack(pady=(10, 10))
        
        user_entry_reg = ctk.CTkEntry(main_frame, placeholder_text="نام کاربری جدید", font=("Vazirmatn", 15), height=45, corner_radius=10, fg_color="#f8fafc", text_color="black")
        user_entry_reg.pack(fill="x", padx=30, pady=8)
        
        pass_entry_reg = ctk.CTkEntry(main_frame, placeholder_text="رمز عبور جدید", show="*", font=("Vazirmatn", 15), height=45, corner_radius=10, fg_color="#f8fafc", text_color="black")
        pass_entry_reg.pack(fill="x", padx=30, pady=8)
        
        def do_register():
            if not user_entry_reg.get() or not pass_entry_reg.get():
                messagebox.showwarning("هشدار", "لطفا همه فیلدها را پر کنید.", parent=auth_win)
                return
                
            conn = sqlite3.connect('school_app.db')
            c = conn.cursor()
            try:
                c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, 'user')", (user_entry_reg.get(), pass_entry_reg.get()))
                conn.commit()
                messagebox.showinfo("موفقیت", "ثبت‌نام شد! حالا وارد شوید.", parent=auth_win)
            except:
                messagebox.showerror("خطا", "این نام کاربری قبلا گرفته شده است.", parent=auth_win)
            conn.close()

        ctk.CTkButton(main_frame, text="ثبت‌نام (کاربر عادی)", font=("Vazirmatn", 16, "bold"), fg_color="#10b981", height=45, corner_radius=10, command=do_register).pack(fill="x", padx=30, pady=(10, 20))

    def logout(self):
        self.current_user_role = None
        self.show_page("home")

if __name__ == "__main__":
    app = App()
    app.mainloop()