#!/bin/bash

# ================================
# Script tạo SSH key và add vào GitHub tự động
# ================================

# Hỏi email để gắn vào SSH key
read -p "Nhập email GitHub của anh: " github_email

# Hỏi token GitHub (Personal Access Token, với quyền 'admin:public_key')
read -p "Nhập Personal Access Token (PAT) của GitHub: " github_token

# Tên SSH key (mặc định id_ed25519)
key_file="$HOME/.ssh/id_ed25519"

# 1. Tạo SSH key nếu chưa có
if [ -f "$key_file" ]; then
  echo "SSH key đã tồn tại: $key_file"
else
  echo "🔑 Tạo SSH key mới..."
  ssh-keygen -t ed25519 -C "$github_email" -f "$key_file" -N ""
fi

# 2. Khởi động ssh-agent và add key
eval "$(ssh-agent -s)"
ssh-add "$key_file"

# 3. Lấy public key
pub_key=$(cat "$key_file.pub")

# 4. Gửi public key lên GitHub qua API
title="Key-$(hostname)-$(date +%Y%m%d%H%M)"
response=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: token $github_token" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/keys \
  -d "{\"title\":\"$title\",\"key\":\"$pub_key\"}")

if [ "$response" -eq 201 ]; then
  echo "✅ SSH key đã được add vào GitHub thành công!"
else
  echo "❌ Lỗi khi add SSH key lên GitHub (HTTP $response)"
  echo "Anh kiểm tra lại token GitHub nhé."
fi

# 5. Kiểm tra kết nối GitHub
echo "🔎 Test kết nối GitHub SSH..."
ssh -T git@github.com