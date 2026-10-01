# Secret Council — Secret Trump × 神祕阿扁

兩個原版 Pygame 遊戲已整合至本專案。`game_trump.py` 與 `game_bian.py` 保留各自的遊戲流程及 AI；正式遊戲以獨立程序啟動，隔離對局狀態。所有程式、圖片與字型均位於本專案，不再依賴舊版資料夾。

## 啟動

需要 Python 3.10 以上。Windows 可直接雙擊 `start.bat`（需先建立 `.venv` 並安裝 `requirements.txt`）。

其他環境首次安裝及啟動：

```sh
python -m pip install -r requirements.txt
python main.py
```

主選單依序提供：

1. **Secret Trump Version** — 進入原本 SecretTrump 主程式。
2. **Tutorial for Trump** — 全英文互動教學。
3. **阿扁版** — 進入原本 SecretBian 主程式。
4. **阿扁版遊戲教學** — 全繁體中文互動教學。

主選單支援滑鼠、上下方向鍵、Enter 與空白鍵。教學使用滑鼠操作；Esc 返回選單。正式遊戲可按 Esc 或左上角按鈕返回選單（目前對局不保留）；關閉遊戲視窗也返回選單。主選單按 Esc 則退出程式。

也可直接執行 `python game_trump.py` 或 `python game_bian.py`，素材路徑不依賴工作目錄。正式遊戲維持原版以滑鼠點選箭頭、投票按鈕、政策牌及中央繼續按鈕的操作。

## 教學與規則

每個版本包含十個練習：翻牌、身分資訊、合法提名、投票、三次破局、總統棄牌、院長棄牌、權力、特殊提名、勝利條件。答錯有提示，完成操作才可前進；可回上一步或重試。總統留下的兩張牌會實際傳到院長步驟。這是獨立的固定情境練習，不影響正式對局。

原始規則已保存至 `docs/bian-rules.txt` 與 `docs/trump-rules.txt`，保留本遊戲與 Secret Hitler 不同的規則：

- 十人：六位藍營／民主黨、三位一般綠營／共和黨，以及一位扁維拉／D.T.。
- 五項藍方政策或殺死特殊角色，藍方獲勝；六項另一方政策，另一方獲勝。
- 第三、第五項綠營／共和黨政策有暗殺權；第四項有私人黨派調查權。
- 四項綠營／共和黨政策後，特殊角色獲提名為院長／chancellor 就直接獲勝，不需要投票。
- 三次破局強制頒布政策，不發動總統權力。

## 美術與程式

- `assets/entrance.png`：以內建 imagegen 產生的政治懸疑桌遊封面。生成提示詞見 `assets/ART_DIRECTION.md`。
- `visual.py`：統一字型、配色、向量式圖示與面板。執行 `python visual.py` 可重新輸出兩版本所有使用中的 PNG 美術。
- `assets/trump/`、`assets/bian/`：新版背景、陣營政策、特殊角色、調查、暗殺、死亡、箭頭及投票按鈕，共二十張 PNG。
- `assets/fonts/wqy-zenhei.ttf`：兩版共用的中文字型，僅保留一份。
- `game_trump.py`、`game_bian.py`：兩個正式遊戲入口。
- `policy_animation.py`：兩版共用的政策動畫與政策軌座標。
- `game_skin.py`：原遊戲的視覺整合、階段提示與柔和切換光框。原有政策淡入改為每秒六十格下約半秒完成，移除背景執行緒繪圖；字型會快取。
- 兩版皆修正原本停留在勝利畫面時，每次重畫都增加勝場的問題；現在每局僅計算一次。
- `tutorial.py`：雙語互動教學狀態及畫面。
- `main.py`：四選項入口與子程序管理。遊戲離開後重新建立主選單畫面。

舊版資料夾、未使用的舊圖片、舊 py2exe 設定及一次性遷移工具已移除。

## 打包 Windows EXE

在專案目錄執行 `build.bat`，會使用 `.venv` 的 Python 安裝打包依賴，再使用 `main.spec` 產生單檔 `dist/SecretCouncil.exe`。圖片、字型與兩版遊戲都已內含，使用者不需安裝 Python。請先關閉正在使用的同名 EXE 再重新打包。

也可以手動執行：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-build.txt
.\.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean main.spec
```

請使用 `python -m PyInstaller` 並明確指定 `.venv`，避免 PATH 中的 Python 3.9 舊版 `pyinstaller.exe` 被誤用。舊版的 `.notanexecutable` 標頭寫入錯誤已不適用目前採用的 PyInstaller 6.x 打包流程。若仍有寫入失敗，檢查錯誤紀錄與安全軟體隔離紀錄，確認檔案是否正被其他程序占用。

EXE 使用 `--edition Trump` 或 `--edition Bian` 啟動內含遊戲模組；不會把 EXE 當成 Python 直譯器去執行外部 `.py`。`main.spec` 關閉 UPX，並使用專案內的資源相對位置，支援單檔解壓路徑。

打包後可執行診斷（會短暫開啟視窗，自動操作兩版各一局與四個入口，並輸出 JSON 報告）：

```powershell
$check = Start-Process -FilePath .\dist\SecretCouncil.exe -ArgumentList '--self-test', 'artifacts\exe-check.json' -WindowStyle Hidden -PassThru -Wait
$check.ExitCode
Get-Content artifacts\exe-check.json
```

## 打包 macOS arm64 單檔執行檔

在 Apple Silicon Mac（M 系列）上，使用原生 arm64 的 Python 3.10 以上執行：

```sh
./build-macos-arm64.sh
```

腳本會自動建立專用的 `.venv-macos-arm64`、安裝 `requirements-build.txt`，再使用 `main-macos-arm64.spec` 產生單一檔案 `dist/SecretCouncil-arm64`。Python runtime、圖片、中文字型及兩版遊戲全部內含，交付時只需這一個檔案，不需另外安裝 Python。可在 Finder 雙擊啟動，或在終端機執行：

```sh
./dist/SecretCouncil-arm64
```

PyInstaller onefile 啟動時會將內含資源解壓至系統暫存目錄，退出後清理，首次啟動會有解壓時間。複製到其他位置後仍可直接執行；若傳送方式遺失執行權限，先執行 `chmod +x SecretCouncil-arm64`。

若要指定 Python 路徑：

```sh
PYTHON=/path/to/arm64/python3 ./build-macos-arm64.sh
```

腳本會檢查 Python 的作業系統、架構及版本；不接受 Rosetta 下的 x86_64 Python。macOS 使用 PyInstaller onefile 並明確指定 `target_arch='arm64'`，Windows 仍使用原有的單檔 EXE 設定。兩個平台需各自在對應的作業系統建置。參考 [PyInstaller 建置說明](https://pyinstaller.org/en/stable/usage.html)。

目前產物使用 PyInstaller 的 ad-hoc 簽章，尚未使用 Apple Developer ID 簽章或公證。

打包後可執行內含診斷（會短暫開啟視窗，自動操作兩版各一局與四個入口）：

```sh
./dist/SecretCouncil-arm64 --self-test artifacts/macos-arm64-check.json
cat artifacts/macos-arm64-check.json
```

若需要標準 macOS APP 套件，也保留原有建置方式：

```sh
./build-macos-arm64.sh --app
open dist/SecretCouncil.app
```

兩種模式都使用 `assets/icons/SecretCouncil.png` 的自訂圖示。建置時透過 `create-macos-icon.sh` 產生標準及 Retina 尺寸的 `.icns`；APP 模式由 `main-macos-arm64-app.spec` 嵌入圖示，單檔模式由 `set-macos-file-icon.js` 設定 Finder 圖示。主選單與兩版遊戲也會使用內含 PNG 設定執行時的 Dock 圖示。

單檔的 Finder 自訂圖示存放於 macOS 檔案中繼資料，複製或傳送時需保留 resource fork／extended attributes（例如使用 Finder 複製或 `ditto`）。部分上傳平台會移除此資訊；遊戲執行時的 Dock 圖示仍會正常顯示。

套用 Finder 自訂圖示後，一般 `codesign --verify` 可通過，但 `codesign --verify --strict` 會拒絕 resource fork／FinderInfo；若需要正式簽章與公證，請使用 `--app` 模式，將圖示存放於 APP 的 Resources。

## 驗證

```sh
python -m unittest discover -s tests -v
python tests/smoke_game.py Trump
python tests/smoke_game.py Bian
python tests/render_previews.py
python tests/smoke_startup.py
python tests/smoke_startup.py --native
```

測試使用 SDL 無視窗模式，驗證教學 gating、錯誤答案、所有棄牌組合、重試及文字排版。每個遊戲 smoke test 以模擬滑鼠完成五局並驗證 Esc 返回；不代表所有隨機 AI 局面都已窮盡。`artifacts/` 提供選單、教學及遊戲的實際 Pygame 渲染預覽。

`smoke_startup.py` 從其他工作目錄啟動入口，實際建立兩個遊戲子程序，並依序操作四個選項與返回選單。加上 `--native` 會短暫開啟真實遊戲視窗，驗證 SDL 顯示模式。
