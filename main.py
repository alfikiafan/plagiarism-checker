# main.py

from view.app_view import PlagiarismApp

def main():
    """
    Fungsi utama untuk menjalankan aplikasi Pengecek Plagiasi.
    """
    app = PlagiarismApp()
    app.mainloop()

if __name__ == "__main__":
    main()
