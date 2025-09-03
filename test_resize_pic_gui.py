import unittest
import os
import tempfile
import shutil
import json
from datetime import datetime, date
from unittest.mock import patch, MagicMock
import tkinter as tk
from PIL import Image

# テスト対象のモジュールをインポート
from resize_pic_gui import ResizePicGUI


class TestResizePicGUI(unittest.TestCase):
    """ResizePicGUIのテストクラス"""
    
    def setUp(self):
        """各テストの前に実行される初期化処理"""
        self.root = tk.Tk()
        self.root.withdraw()  # GUIを非表示にしてテスト実行
        
        # テスト用の一時ディレクトリを作成
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "test_config.json")
        
        # テスト用の画像ファイルを作成
        self.test_images = []
        for i in range(3):
            image_path = os.path.join(self.test_dir, f"test_image_{i}.jpg")
            # 100x100のテスト画像を作成
            test_image = Image.new('RGB', (100, 100), color=(255, 0, 0))
            test_image.save(image_path)
            self.test_images.append(image_path)
        
        # より大きい画像（横長）
        large_image_path = os.path.join(self.test_dir, "large_image.jpg")
        large_image = Image.new('RGB', (1000, 600), color=(0, 255, 0))
        large_image.save(large_image_path)
        self.test_images.append(large_image_path)
        
        # より大きい画像（縦長）
        tall_image_path = os.path.join(self.test_dir, "tall_image.jpg")
        tall_image = Image.new('RGB', (400, 800), color=(0, 0, 255))
        tall_image.save(tall_image_path)
        self.test_images.append(tall_image_path)
    
    def tearDown(self):
        """各テストの後に実行されるクリーンアップ処理"""
        self.root.destroy()
        # テスト用ディレクトリを削除
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def create_app_with_config(self, config_data=None):
        """設定ファイル付きでアプリを作成"""
        if config_data:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f)
        
        # config_fileパラメータを渡してアプリを作成
        app = ResizePicGUI(self.root, config_file=self.config_file)
        return app
    
    def test_load_config_default(self):
        """デフォルト設定の読み込みテスト"""
        app = self.create_app_with_config()
        self.assertIn('folder_path', app.config)
        self.assertEqual(app.config['folder_path'], os.path.expanduser("~"))
    
    def test_load_config_existing(self):
        """既存設定ファイルの読み込みテスト"""
        test_config = {"folder_path": "/test/path"}
        app = self.create_app_with_config(test_config)
        self.assertEqual(app.config['folder_path'], "/test/path")
    
    def test_save_config(self):
        """設定保存テスト"""
        app = self.create_app_with_config()
        app.folder_var.set("/new/test/path")
        app.save_config()
        
        # 設定が正しく保存されているかチェック
        with open(self.config_file, 'r', encoding='utf-8') as f:
            saved_config = json.load(f)
        self.assertEqual(saved_config['folder_path'], "/new/test/path")
    
    def test_get_date_valid(self):
        """有効な日付取得テスト"""
        app = self.create_app_with_config()
        
        # DateEntryがない場合のテスト（通常のEntry）
        if hasattr(app.date_entry, 'get_date'):
            # DateEntryの場合
            result_date = app.get_date()
            self.assertIsInstance(result_date, date)
        else:
            # 通常のEntryの場合
            app.date_var.set('2023-12-25')
            result_date = app.get_date()
            expected_date = datetime.strptime('2023-12-25', '%Y-%m-%d').date()
            self.assertEqual(result_date, expected_date)
    
    def test_get_date_invalid(self):
        """無効な日付取得テスト"""
        app = self.create_app_with_config()
        
        if not hasattr(app.date_entry, 'get_date'):
            app.date_var.set('invalid-date')
            result_date = app.get_date()
            self.assertIsNone(result_date)
    
    @patch('tkinter.filedialog.askdirectory')
    def test_select_folder(self, mock_askdirectory):
        """フォルダ選択テスト"""
        mock_askdirectory.return_value = "/selected/folder"
        
        app = self.create_app_with_config()
        app.select_folder()
        
        self.assertEqual(app.folder_var.get(), "/selected/folder")
        mock_askdirectory.assert_called_once()
    
    def test_resize_images_horizontal(self):
        """横長画像のリサイズテスト"""
        app = self.create_app_with_config()
        test_date = date(2023, 12, 25)
        
        # 横長の大きい画像をテスト
        horizontal_image = [img for img in self.test_images if "large_image" in img][0]
        
        app.resize_images([horizontal_image], test_date)
        
        # リサイズされた画像が作成されているかチェック
        expected_filename = "20231225_00_pic_0000.jpg"
        expected_path = os.path.join(self.test_dir, expected_filename)
        self.assertTrue(os.path.exists(expected_path))
        
        # リサイズされた画像のサイズをチェック
        with Image.open(expected_path) as resized_img:
            width, height = resized_img.size
            self.assertEqual(width, 600)  # 横長なので幅が600に設定される
            self.assertEqual(height, 360)  # アスペクト比を維持
    
    def test_resize_images_vertical(self):
        """縦長画像のリサイズテスト"""
        app = self.create_app_with_config()
        test_date = date(2023, 12, 25)
        
        # 縦長の大きい画像をテスト
        vertical_image = [img for img in self.test_images if "tall_image" in img][0]
        
        app.resize_images([vertical_image], test_date)
        
        # リサイズされた画像が作成されているかチェック
        expected_filename = "20231225_00_pic_0000.jpg"
        expected_path = os.path.join(self.test_dir, expected_filename)
        self.assertTrue(os.path.exists(expected_path))
        
        # リサイズされた画像のサイズをチェック
        with Image.open(expected_path) as resized_img:
            width, height = resized_img.size
            self.assertEqual(height, 500)  # 縦長なので高さが500に設定される
            self.assertEqual(width, 250)   # アスペクト比を維持
    
    def test_resize_images_multiple(self):
        """複数画像のリサイズテスト"""
        app = self.create_app_with_config()
        test_date = date(2023, 12, 25)
        
        # 最初の3つの小さい画像をテスト
        small_images = self.test_images[:3]
        
        app.resize_images(small_images, test_date)
        
        # 3つのリサイズされた画像が作成されているかチェック
        for i in range(3):
            expected_filename = f"20231225_00_pic_{i:04d}.jpg"
            expected_path = os.path.join(self.test_dir, expected_filename)
            self.assertTrue(os.path.exists(expected_path), 
                          f"Expected file {expected_filename} was not created")
    
    def test_resize_images_error_handling(self):
        """画像リサイズエラーハンドリングテスト"""
        app = self.create_app_with_config()
        test_date = date(2023, 12, 25)
        
        # 存在しないファイルパス
        non_existent_file = os.path.join(self.test_dir, "non_existent.jpg")
        
        with self.assertRaises(Exception) as context:
            app.resize_images([non_existent_file], test_date)
        
        self.assertIn("処理中にエラーが発生しました", str(context.exception))
    
    @patch('tkinter.messagebox.showerror')
    def test_execute_resize_no_folder(self, mock_showerror):
        """フォルダ未選択時のエラーテスト"""
        app = self.create_app_with_config()
        app.folder_var.set("")  # 空のフォルダパス
        
        app.execute_resize()
        
        mock_showerror.assert_called_with("エラー", "フォルダを選択してください。")
    
    @patch('tkinter.messagebox.showerror')
    def test_execute_resize_invalid_folder(self, mock_showerror):
        """無効なフォルダパスのエラーテスト"""
        app = self.create_app_with_config()
        app.folder_var.set("/non/existent/folder")
        
        app.execute_resize()
        
        mock_showerror.assert_called_with("エラー", "指定されたフォルダが存在しません。")
    
    @patch('tkinter.filedialog.askopenfilenames')
    @patch('tkinter.messagebox.showinfo')
    def test_execute_resize_success(self, mock_showinfo, mock_askopenfilenames):
        """正常なリサイズ実行テスト"""
        mock_askopenfilenames.return_value = self.test_images[:2]
        
        app = self.create_app_with_config()
        app.folder_var.set(self.test_dir)
        
        with patch.object(app, 'close_app'):
            app.execute_resize()
        
        mock_showinfo.assert_called_once()
        call_args = mock_showinfo.call_args[0]
        self.assertEqual(call_args[0], "完了")
        self.assertIn("2枚の画像をリサイズしました", call_args[1])


class TestIntegration(unittest.TestCase):
    """統合テスト"""
    
    def setUp(self):
        """統合テストの初期化"""
        self.test_dir = tempfile.mkdtemp()
        self.root = tk.Tk()
        self.root.withdraw()
    
    def tearDown(self):
        """統合テストのクリーンアップ"""
        self.root.destroy()
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_full_workflow(self):
        """完全なワークフローの統合テスト"""
        # テスト用画像を作成
        test_image_path = os.path.join(self.test_dir, "integration_test.jpg")
        test_image = Image.new('RGB', (800, 600), color=(128, 128, 128))
        test_image.save(test_image_path)
        
        # 設定ファイルパスを指定
        config_file = os.path.join(self.test_dir, "integration_config.json")
        
        # config_fileパラメータを渡してアプリを作成
        app = ResizePicGUI(self.root, config_file=config_file)
        
        # 設定を行う
        app.folder_var.set(self.test_dir)
        test_date = date(2023, 12, 31)
        
        # リサイズを実行
        app.resize_images([test_image_path], test_date)
        
        # 結果を検証
        expected_filename = "20231231_00_pic_0000.jpg"
        expected_path = os.path.join(self.test_dir, expected_filename)
        
        self.assertTrue(os.path.exists(expected_path))
        
        # リサイズされた画像の検証
        with Image.open(expected_path) as resized_img:
            width, height = resized_img.size
            # 横長なので幅600にリサイズされる
            self.assertEqual(width, 600)
            self.assertEqual(height, 450)  # アスペクト比維持


def run_tests():
    """テストスイートを実行"""
    # テストローダーを作成
    loader = unittest.TestLoader()
    
    # テストスイートを作成
    test_suite = unittest.TestSuite()
    
    # 単体テストを追加
    test_suite.addTests(loader.loadTestsFromTestCase(TestResizePicGUI))
    test_suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # テストランナーを作成
    runner = unittest.TextTestRunner(verbosity=2)
    
    # テストを実行
    result = runner.run(test_suite)
    
    return result


if __name__ == '__main__':
    print("=== 画像リサイズGUIアプリケーション テスト実行 ===")
    print()
    
    try:
        result = run_tests()
        
        print()
        print("=== テスト結果サマリー ===")
        print(f"実行テスト数: {result.testsRun}")
        print(f"失敗: {len(result.failures)}")
        print(f"エラー: {len(result.errors)}")
        
        if result.failures:
            print("\n失敗したテスト:")
            for test, traceback in result.failures:
                error_msg = traceback.split('AssertionError:')[-1].strip() if 'AssertionError:' in traceback else traceback.split('\n')[-2]
                print(f"- {test}: {error_msg}")
        
        if result.errors:
            print("\nエラーが発生したテスト:")
            for test, traceback in result.errors:
                error_msg = traceback.split('Exception:')[-1].strip() if 'Exception:' in traceback else traceback.split('\n')[-2]
                print(f"- {test}: {error_msg}")
        
        if result.wasSuccessful():
            print("\n✅ すべてのテストが成功しました！")
        else:
            print("\n❌ 一部のテストが失敗しました。")
            
    except ImportError as e:
        print(f"❌ インポートエラー: {e}")
        print("resize_pic_gui.pyが同じディレクトリにあることを確認してください。")
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")
        print("必要なライブラリ（pillow, tkcalendar）がインストールされていることを確認してください。")