from PIL import Image
import os
import json
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkcalendar import DateEntry

class ResizePicGUI:
    def __init__(self, root, config_file=None):
        self.root = root
        self.root.title("画像リサイズツール")
        self.root.geometry("500x300")
        self.root.resizable(False, False)
        
        # 設定ファイルのパス
        self.config_file = config_file if config_file is not None else "config.json"
        
        # 設定を読み込み
        self.config = self.load_config()
        
        # GUI要素の作成
        self.create_widgets()
        
    def load_config(self):
        """設定ファイルを読み込む"""
        default_config = {
            "folder_path": os.path.expanduser("~")  # デフォルトはホームディレクトリ
        }
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                return {**default_config, **config}
            else:
                return default_config
        except Exception:
            return default_config
    
    def save_config(self):
        """設定ファイルに保存する"""
        try:
            config = {
                "folder_path": self.folder_var.get()
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception:
            pass  # 保存に失敗しても処理は継続
    
    def create_widgets(self):
        """GUI要素を作成"""
        # メインフレーム
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # タイトル
        title_label = ttk.Label(main_frame, text="画像リサイズツール 設定", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # フォルダ選択部分
        folder_label = ttk.Label(main_frame, text="開くフォルダのアドレス:")
        folder_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        folder_frame = ttk.Frame(main_frame)
        folder_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        folder_frame.columnconfigure(0, weight=1)
        
        self.folder_var = tk.StringVar(value=self.config.get("folder_path", ""))
        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_var, width=50)
        self.folder_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        select_button = ttk.Button(folder_frame, text="選択", command=self.select_folder)
        select_button.grid(row=0, column=1)
        
        # 日付選択部分
        date_label = ttk.Label(main_frame, text="日付:")
        date_label.grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        
        # カレンダーウィジェットを使用
        try:
            self.date_entry = DateEntry(main_frame, width=12, background='darkblue',
                                      foreground='white', borderwidth=2, 
                                      date_pattern='yyyy-mm-dd')
            self.date_entry.grid(row=4, column=0, sticky=tk.W, pady=(0, 30))
        except ImportError:
            # tkcalendarがない場合は、通常のEntryを使用
            date_frame = ttk.Frame(main_frame)
            date_frame.grid(row=4, column=0, sticky=tk.W, pady=(0, 30))
            
            today = datetime.now()
            self.date_var = tk.StringVar(value=today.strftime('%Y-%m-%d'))
            self.date_entry = ttk.Entry(date_frame, textvariable=self.date_var, width=15)
            self.date_entry.grid(row=0, column=0)
            
            date_help = ttk.Label(date_frame, text="(yyyy-mm-dd形式)", font=("Arial", 8))
            date_help.grid(row=0, column=1, padx=(5, 0))
        
        # ボタン部分
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=(20, 0))
        
        ok_button = ttk.Button(button_frame, text="OK", command=self.execute_resize, width=12)
        ok_button.grid(row=0, column=0, padx=(0, 10))
        
        cancel_button = ttk.Button(button_frame, text="終了", command=self.close_app, width=12)
        cancel_button.grid(row=0, column=1, padx=(10, 0))
        
    def select_folder(self):
        """フォルダ選択ダイアログを開く"""
        folder_path = filedialog.askdirectory(
            initialdir=self.folder_var.get() if self.folder_var.get() else os.path.expanduser("~"),
            title="フォルダを選択してください"
        )
        if folder_path:
            self.folder_var.set(folder_path)
    
    def get_date(self):
        """日付を取得する"""
        try:
            if hasattr(self.date_entry, 'get_date'):
                # DateEntryの場合
                return self.date_entry.get_date()
            else:
                # 通常のEntryの場合
                date_str = self.date_var.get()
                return datetime.strptime(date_str, '%Y-%m-%d').date()
        except Exception:
            return None
    
    def execute_resize(self):
        """リサイズ処理を実行"""
        # 入力値の検証
        folder_path = self.folder_var.get().strip()
        if not folder_path:
            messagebox.showerror("エラー", "フォルダを選択してください。")
            return
        
        if not os.path.exists(folder_path):
            messagebox.showerror("エラー", "指定されたフォルダが存在しません。")
            return
        
        date_obj = self.get_date()
        if date_obj is None:
            messagebox.showerror("エラー", "正しい日付形式で入力してください。")
            return
        
        # 設定を保存
        self.save_config()
        
        # 画像ファイルを選択
        filepaths = filedialog.askopenfilenames(
            initialdir=folder_path,
            title="リサイズする画像を選択",
            filetypes=[
                ("画像ファイル", "*.jpg *.jpeg *.png *.bmp *.tiff *.gif"),
                ("JPEGファイル", "*.jpg *.jpeg"),
                ("PNGファイル", "*.png"),
                ("すべてのファイル", "*.*")
            ]
        )
        
        if not filepaths:
            return
        
        # リサイズ処理を実行
        try:
            self.resize_images(filepaths, date_obj)
            messagebox.showinfo("完了", f"処理が完了しました。\n{len(filepaths)}枚の画像をリサイズしました。")
            self.close_app()
        except Exception as e:
            messagebox.showerror("エラー", f"処理中にエラーが発生しました:\n{str(e)}")
    
    def resize_images(self, filepaths, date_obj):
        """画像をリサイズする"""
        for i, filepath in enumerate(filepaths):
            try:
                # 画像ファイルを開く
                with Image.open(filepath) as image:
                    # 画像のサイズを取得
                    width, height = image.size
                    
                    # リサイズするサイズを計算
                    if width > height:
                        new_width = 600
                        new_height = int(height * (new_width / width))
                    else:
                        new_height = 500
                        new_width = int(width * (new_height / height))
                    
                    # 画像をリサイズ
                    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # ファイル名を作成
                    save_dir = os.path.dirname(filepath)
                    file_extension = os.path.splitext(filepath)[1]
                    filename = f"{date_obj.strftime('%Y%m%d')}_00_pic_{i:04d}{file_extension}"
                    save_path = os.path.join(save_dir, filename)
                    
                    # リサイズされた画像を保存
                    resized_image.save(save_path, quality=95)
            
            except Exception as e:
                raise Exception(f"ファイル '{os.path.basename(filepath)}' の処理中にエラーが発生しました: {str(e)}")
    
    def close_app(self):
        """アプリケーションを終了"""
        self.root.destroy()

def main():
    root = tk.Tk()
    app = ResizePicGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()