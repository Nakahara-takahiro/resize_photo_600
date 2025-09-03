# 画像リサイズGUIアプリケーション テスト実施方法

## 概要
このドキュメントでは、`resize_pic_gui.py`のテストコード`test_resize_pic_gui.py`の実施方法について説明します。

## 前提条件

### 必要なライブラリ
テストを実行する前に、以下のライブラリがインストールされていることを確認してください：

```bash
pip install pillow tkcalendar
```

### ファイル構成
以下のファイルが同じディレクトリにあることを確認してください：
- `resize_pic_gui.py` (メインアプリケーション)
- `test_resize_pic_gui.py` (テストコード)

## テスト実施方法

### 1. 推奨: 標準的なテスト実行

最新のPython環境に対応した実行方法：

```bash
python -m unittest discover -s . -p "test_*.py" -v
```

または、より簡潔に：

```bash
python -m unittest test_resize_pic_gui -v
```

### 2. カスタムテストランナーでの実行

カスタマイズされた出力で実行する場合：

```bash
python test_resize_pic_gui.py
```

### 3. 特定のテストクラスのみ実行

```bash
python -m unittest test_resize_pic_gui.TestResizePicGUI -v
```

### 4. 特定のテストメソッドのみ実行

```bash
python -m unittest test_resize_pic_gui.TestResizePicGUI.test_resize_images_horizontal -v
```

### 5. Python 3.13対応の注意事項

Python 3.13以降では、`unittest.makeSuite`が削除されているため、テストコードは`unittest.TestLoader`を使用するように更新されています。古いPythonバージョンとの互換性も保持されています。

## テスト内容

### 単体テスト (TestResizePicGUI)

| テストメソッド | テスト内容 |
|---|---|
| `test_load_config_default` | デフォルト設定の読み込み |
| `test_load_config_existing` | 既存設定ファイルの読み込み |
| `test_save_config` | 設定ファイルの保存機能 |
| `test_get_date_valid` | 有効な日付の取得 |
| `test_get_date_invalid` | 無効な日付のエラーハンドリング |
| `test_select_folder` | フォルダ選択機能 |
| `test_resize_images_horizontal` | 横長画像のリサイズ |
| `test_resize_images_vertical` | 縦長画像のリサイズ |
| `test_resize_images_multiple` | 複数画像の一括リサイズ |
| `test_resize_images_error_handling` | リサイズエラーの処理 |
| `test_execute_resize_no_folder` | フォルダ未選択エラー |
| `test_execute_resize_invalid_folder` | 無効フォルダエラー |
| `test_execute_resize_success` | 正常なリサイズ実行 |

### 統合テスト (TestIntegration)

| テストメソッド | テスト内容 |
|---|---|
| `test_full_workflow` | 完全なワークフローの動作確認 |

## テスト実行時の注意事項

### 1. GUI環境について
- テストは自動的にGUI要素を非表示にして実行されます
- ヘッドレス環境（GUI非対応環境）では実行できない可能性があります

### 2. 一時ファイルについて
- テスト実行中に一時ディレクトリと一時ファイルが作成されます
- テスト終了後に自動的に削除されます

### 3. テスト実行時間
- 全テストの実行には通常10-30秒程度かかります
- 画像ファイルの作成と処理が含まれるため、ディスクI/Oが発生します

## 期待される結果

### 成功時の出力例
```
=== 画像リサイズGUIアプリケーション テスト実行 ===

test_execute_resize_invalid_folder (test_resize_pic_gui.TestResizePicGUI) ... ok
test_execute_resize_no_folder (test_resize_pic_gui.TestResizePicGUI) ... ok
test_execute_resize_success (test_resize_pic_gui.TestResizePicGUI) ... ok
test_get_date_invalid (test_resize_pic_gui.TestResizePicGUI) ... ok
test_get_date_valid (test_resize_pic_gui.TestResizePicGUI) ... ok
test_load_config_default (test_resize_pic_gui.TestResizePicGUI) ... ok
test_load_config_existing (test_resize_pic_gui.TestResizePicGUI) ... ok
test_resize_images_error_handling (test_resize_pic_gui.TestResizePicGUI) ... ok
test_resize_images_horizontal (test_resize_pic_gui.TestResizePicGUI) ... ok
test_resize_images_multiple (test_resize_pic_gui.TestResizePicGUI) ... ok
test_resize_images_vertical (test_resize_pic_gui.TestResizePicGUI) ... ok
test_save_config (test_resize_pic_gui.TestResizePicGUI) ... ok
test_select_folder (test_resize_pic_gui.TestResizePicGUI) ... ok
test_full_workflow (test_resize_pic_gui.TestIntegration) ... ok

----------------------------------------------------------------------
Ran 14 tests in 2.345s

OK

=== テスト結果サマリー ===
実行テスト数: 14
失敗: 0
エラー: 0

✅ すべてのテストが成功しました！
```

## トラブルシューティング

### よくある問題と解決方法

#### 1. ImportErrorが発生する場合
```
ImportError: No module named 'resize_pic_gui'
```

**解決方法**: `resize_pic_gui.py`が同じディレクトリにあることを確認

#### 2. Pillowライブラリのエラー
```
ModuleNotFoundError: No module named 'PIL'
```

**解決方法**: 
```bash
pip install pillow
```

#### 3. tkinterのエラー（Linux環境）
```
ModuleNotFoundError: No module named 'tkinter'
```

**解決方法** (Ubuntu/Debian):
```bash
sudo apt-get install python3-tk
```

#### 4. tkcalendarのエラー
```
ModuleNotFoundError: No module named 'tkcalendar'
```

**解決方法**: 
```bash
pip install tkcalendar
```

この場合、アプリケーションは通常のテキスト入力にフォールバックします。

## 継続的インテグレーション (CI)

GitHubActionsなどのCI環境で実行する場合の設定例：

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    
    - name: Install system dependencies
      run: |
        sudo apt-get update
        sudo apt-get install python3-tk xvfb
    
    - name: Install Python dependencies
      run: |
        pip install pillow tkcalendar
    
    - name: Run tests
      run: |
        xvfb-run -a python test_resize_pic_gui.py
```

## テスト結果の解釈

- **✅ OK**: テストが成功
- **❌ FAIL**: アサーションが失敗（期待値と実際の値が異なる）
- **💥 ERROR**: テスト実行中に例外が発生

失敗やエラーが発生した場合は、詳細なトレースバック情報が表示されるので、それを基に問題を特定してください。