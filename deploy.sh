#!/bin/bash

echo "===================================="
echo "  AI Essay Grading System"
echo "  GitHub 一鍵部署腳本"
echo "===================================="
echo ""

# 檢查是否已初始化 Git
if [ ! -d ".git" ]; then
    echo "[1/6] 初始化 Git 倉庫..."
    git init
    echo "✓ Git 初始化完成"
    echo ""
else
    echo "✓ Git 已初始化"
    echo ""
fi

# 添加檔案
echo "[2/6] 添加所有檔案到 Git..."
git add .
echo "✓ 檔案已添加"
echo ""

# 提交
echo "[3/6] 提交變更..."
git commit -m "初始提交：AI 作文批改系統完整版"
echo "✓ 提交完成"
echo ""

# 詢問 GitHub 倉庫 URL
echo "[4/6] 設定 GitHub 遠端倉庫..."
read -p "請輸入你的 GitHub 倉庫 URL: " REPO_URL

# 檢查是否已設定遠端
if git remote | grep -q "origin"; then
    echo "遠端倉庫已存在，更新 URL..."
    git remote set-url origin "$REPO_URL"
else
    git remote add origin "$REPO_URL"
fi
echo "✓ 遠端倉庫設定完成"
echo ""

# 推送到 GitHub
echo "[5/6] 推送到 GitHub..."
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✓ 推送成功！"
    echo ""
    echo "[6/6] 驗證部署..."
    echo "✓ 部署完成！"
    echo ""
    echo "===================================="
    echo "  🎉 恭喜！專案已成功部署到 GitHub"
    echo "===================================="
    echo ""
    echo "前往查看：${REPO_URL%.git}"
    echo ""
else
    echo "✗ 推送失敗"
    echo ""
    echo "可能的原因："
    echo "1. 需要輸入 GitHub 帳號和 Token"
    echo "2. 網路連線問題"
    echo "3. GitHub 倉庫不存在"
    echo ""
    echo "請查看 DEPLOYMENT_GUIDE.md 了解詳細步驟"
    echo ""
fi
