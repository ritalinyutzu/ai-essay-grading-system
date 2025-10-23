# 🚀 GitHub 部署完整指南

本指南將手把手教你如何將 AI 作文批改系統部署到 GitHub。

---

## 📋 前置準備

### 1. 確認已安裝 Git

打開終端機（PowerShell / Terminal），執行：

```bash
git --version
```

**如果沒有安裝：**
- Windows: 下載 [Git for Windows](https://git-scm.com/download/win)
- macOS: `brew install git`
- Linux: `sudo apt-get install git`

### 2. GitHub 帳號

- 沒有帳號？前往 [GitHub](https://github.com) 註冊
- 記住你的使用者名稱

### 3. 設定 Git 個人資訊

```bash
git config --global user.name "你的名字"
git config --global user.email "你的Email"
```

---

## 🎯 部署步驟

### 步驟 1：下載專案檔案

**選項 A：從 Claude 下載**

如果你是從 Claude 產生的檔案，請：
1. 下載所有檔案
2. 放到同一個資料夾（例如：`C:\Projects\ai-essay-grading-system`）

**選項 B：從本地建立**

如果檔案已經在本地：
```bash
cd 你的專案路徑
```

---

### 步驟 2：在 GitHub 建立新倉庫

#### 2.1 登入 GitHub

前往 https://github.com 並登入

#### 2.2 建立新倉庫

1. 點擊右上角的 `+` → `New repository`
2. 填寫資訊：
   - **Repository name**: `ai-essay-grading-system`
   - **Description**: `AI 作文自動批改系統 - 基於 ICR 和 NLP`
   - **Public/Private**: 選擇 Public（公開）
   - **不要勾選** "Initialize this repository with a README"（因為我們已經有了）
3. 點擊 `Create repository`

#### 2.3 記下 Git URL

建立後，你會看到類似這樣的 URL：
```
https://github.com/你的使用者名稱/ai-essay-grading-system.git
```

**複製這個 URL！待會會用到。**

---

### 步驟 3：初始化 Git 倉庫（本地）

打開終端機，進入專案資料夾：

```bash
# Windows
cd C:\Projects\ai-essay-grading-system

# macOS/Linux
cd ~/Projects/ai-essay-grading-system
```

初始化 Git：

```bash
git init
```

你應該會看到：
```
Initialized empty Git repository in ...
```

---

### 步驟 4：添加檔案到 Git

```bash
# 查看所有檔案
git status

# 添加所有檔案
git add .

# 確認已添加
git status
```

你應該會看到綠色的文字，表示檔案已準備好提交。

---

### 步驟 5：提交變更

```bash
git commit -m "初始提交：AI 作文批改系統完整版"
```

你應該會看到類似：
```
[main (root-commit) xxxxxxx] 初始提交：AI 作文批改系統完整版
 15 files changed, 2500 insertions(+)
 create mode 100644 README.md
 create mode 100644 essay_grading_system.py
 ...
```

---

### 步驟 6：連接到 GitHub

將本地倉庫連接到 GitHub：

```bash
git remote add origin https://github.com/你的使用者名稱/ai-essay-grading-system.git
```

**重要：** 把上面的 URL 替換成你在步驟 2.3 複製的 URL！

---

### 步驟 7：推送到 GitHub

```bash
# 推送主分支
git branch -M main
git push -u origin main
```

**第一次推送會要求輸入 GitHub 帳號密碼：**

- **Username**: 你的 GitHub 使用者名稱
- **Password**: 
  - **不是你的密碼！** 
  - 而是 **Personal Access Token**（個人訪問令牌）

---

### 步驟 8：產生 Personal Access Token（如果需要）

如果你還沒有 Token：

1. 前往 GitHub → Settings（頭像下拉選單）
2. 左側選單最下方：Developer settings
3. Personal access tokens → Tokens (classic)
4. Generate new token (classic)
5. 填寫：
   - **Note**: `AI Essay Grading System`
   - **Expiration**: 90 days（或更長）
   - **Select scopes**: 勾選 `repo`（整個區塊）
6. 點擊 `Generate token`
7. **複製 Token**（只會顯示一次！）

格式類似：`ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

### 步驟 9：使用 Token 推送

再次執行推送，這次輸入 Token：

```bash
git push -u origin main
```

- Username: `你的使用者名稱`
- Password: **貼上你的 Token**

**成功！** 你應該會看到：
```
Enumerating objects: 20, done.
Counting objects: 100% (20/20), done.
...
To https://github.com/你的使用者名稱/ai-essay-grading-system.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

## ✅ 驗證部署

### 檢查 GitHub

1. 前往 `https://github.com/你的使用者名稱/ai-essay-grading-system`
2. 你應該會看到所有檔案！
3. README.md 會自動顯示在首頁

---

## 🔄 後續更新

當你修改檔案後，想要推送更新：

```bash
# 1. 查看修改
git status

# 2. 添加修改的檔案
git add .

# 3. 提交
git commit -m "描述你做了什麼修改"

# 4. 推送
git push
```

**常用的 commit 訊息範例：**
```bash
git commit -m "新增：評分演算法優化"
git commit -m "修復：ICR 辨識 bug"
git commit -m "更新：README 文件"
git commit -m "改進：提升準確率到 92%"
```

---

## 🎨 美化 GitHub 專案

### 1. 添加 Topics（標籤）

在 GitHub 專案頁面：
1. 點擊右側的 ⚙️ Settings
2. 找到 Topics
3. 添加：`machine-learning`, `nlp`, `ocr`, `education`, `python`, `ai`

### 2. 添加描述

在專案首頁，點擊 "Add description"：
```
AI 作文自動批改系統 - 基於 ICR 文字辨識和 NLP 評分，支援 Confusion Matrix、F1 Score 等評估指標
```

### 3. 添加網站（可選）

如果你有 Demo 網站或文件網站，可以在 Settings → Website 添加

---

## 🐛 常見問題排除

### 問題 1：push 時說 "rejected"

**原因：** 遠端有新的變更，需要先拉取

**解決：**
```bash
git pull origin main --rebase
git push
```

---

### 問題 2：忘記 Token

**解決：** 重新產生新的 Token（步驟 8）

---

### 問題 3：檔案太大無法推送

**原因：** Git 限制單一檔案 100 MB

**解決：**
1. 檢查哪些檔案太大：
   ```bash
   find . -size +50M
   ```

2. 添加到 .gitignore：
   ```bash
   echo "檔案名稱" >> .gitignore
   ```

3. 重新提交：
   ```bash
   git rm --cached 檔案名稱
   git add .gitignore
   git commit -m "移除大型檔案"
   git push
   ```

---

### 問題 4：想刪除某個檔案

```bash
# 從 Git 刪除（但保留本地檔案）
git rm --cached 檔案名稱

# 從 Git 和本地都刪除
git rm 檔案名稱

# 提交刪除
git commit -m "刪除檔案"
git push
```

---

### 問題 5：想重新命名檔案

```bash
git mv 舊檔名 新檔名
git commit -m "重新命名檔案"
git push
```

---

## 📚 Git 常用指令速查表

```bash
# 查看狀態
git status

# 查看歷史
git log

# 查看差異
git diff

# 查看遠端倉庫
git remote -v

# 拉取最新變更
git pull

# 推送到遠端
git push

# 查看分支
git branch

# 建立新分支
git checkout -b 新分支名稱

# 切換分支
git checkout 分支名稱

# 合併分支
git merge 分支名稱
```

---

## 🎓 進階技巧

### 1. 使用 GitHub Actions（自動化測試）

建立 `.github/workflows/test.yml`：

```yaml
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
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python test_installation.py
```

### 2. 添加 Badge（徽章）

在 README.md 最上方添加：

```markdown
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/你的使用者名稱/ai-essay-grading-system.svg)](https://github.com/你的使用者名稱/ai-essay-grading-system/stargazers)
```

### 3. 啟用 GitHub Pages（建立文件網站）

1. 在 Settings → Pages
2. Source 選擇 `main` branch
3. 前往 `https://你的使用者名稱.github.io/ai-essay-grading-system`

---

## 📞 需要幫助？

如果遇到問題：

1. **查看 GitHub 文件：** https://docs.github.com
2. **Google 搜尋：** "git 問題描述"
3. **Stack Overflow：** https://stackoverflow.com
4. **提交 Issue：** 在你的 GitHub 專案中點擊 "Issues"

---

## 🎉 恭喜！

你已經成功將專案部署到 GitHub！

**下一步：**
- 分享專案連結給朋友
- 在 LinkedIn 上展示
- 投遞履歷時附上 GitHub 連結
- 繼續開發新功能

---

## 📝 快速部署指令總覽

```bash
# 完整流程（複製貼上）

# 1. 進入專案目錄
cd 你的專案路徑

# 2. 初始化 Git
git init

# 3. 添加所有檔案
git add .

# 4. 提交
git commit -m "初始提交：AI 作文批改系統"

# 5. 連接到 GitHub（替換成你的 URL）
git remote add origin https://github.com/你的使用者名稱/ai-essay-grading-system.git

# 6. 推送
git branch -M main
git push -u origin main
```

---

**Made with ❤️ by Rita Lin**

有問題隨時回來查看這份指南！ 🚀
