#!/bin/bash

# 测试脚本：验证超级管理员功能

BASE_URL="http://127.0.0.1:8000"

echo "========================================"
echo "测试 1: 默认管理员登录"
echo "========================================"
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}')
echo "$LOGIN_RESPONSE" | python3 -m json.tool

DEFAULT_TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
echo -e "\n获取到 token: ${DEFAULT_TOKEN:0:50}...\n"

echo "========================================"
echo "测试 2: 执行初始设置，创建新管理员"
echo "========================================"
SETUP_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/setup" \
  -H "Authorization: Bearer $DEFAULT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username":"superadmin","email":"super@example.com","password":"super123","full_name":"Super Admin"}')
echo "$SETUP_RESPONSE" | python3 -m json.tool

NEW_TOKEN=$(echo "$SETUP_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
echo -e "\n获取到新 token: ${NEW_TOKEN:0:50}...\n"

echo "========================================"
echo "测试 3: 验证新管理员是否是超级管理员"
echo "========================================"
ME_RESPONSE=$(curl -s -X GET "$BASE_URL/api/auth/me" \
  -H "Authorization: Bearer $NEW_TOKEN")
echo "$ME_RESPONSE" | python3 -m json.tool

IS_SUPERUSER=$(echo "$ME_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['is_superuser'])")
echo -e "\n>>> is_superuser = $IS_SUPERUSER"

if [ "$IS_SUPERUSER" = "True" ]; then
    echo "✅ 成功！新管理员是超级管理员"
else
    echo "❌ 失败！新管理员不是超级管理员"
    exit 1
fi

echo -e "\n========================================"
echo "测试 4: 超级管理员创建普通用户"
echo "========================================"
NORMAL_USER=$(curl -s -X POST "$BASE_URL/api/auth/register" \
  -H "Authorization: Bearer $NEW_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username":"normaluser","email":"normal@example.com","password":"pass123","is_superuser":false}')
echo "$NORMAL_USER" | python3 -m json.tool

NORMAL_IS_SUPER=$(echo "$NORMAL_USER" | python3 -c "import sys, json; print(json.load(sys.stdin)['is_superuser'])")
echo -e "\n>>> normaluser is_superuser = $NORMAL_IS_SUPER"

if [ "$NORMAL_IS_SUPER" = "False" ]; then
    echo "✅ 成功！创建了普通用户"
else
    echo "❌ 失败！创建的应该是普通用户"
    exit 1
fi

echo -e "\n========================================"
echo "测试 5: 超级管理员创建另一个超级管理员"
echo "========================================"
ANOTHER_ADMIN=$(curl -s -X POST "$BASE_URL/api/auth/register" \
  -H "Authorization: Bearer $NEW_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin2","email":"admin2@example.com","password":"pass123","is_superuser":true}')
echo "$ANOTHER_ADMIN" | python3 -m json.tool

ADMIN2_IS_SUPER=$(echo "$ANOTHER_ADMIN" | python3 -c "import sys, json; print(json.load(sys.stdin)['is_superuser'])")
echo -e "\n>>> admin2 is_superuser = $ADMIN2_IS_SUPER"

if [ "$ADMIN2_IS_SUPER" = "True" ]; then
    echo "✅ 成功！创建了另一个超级管理员"
else
    echo "❌ 失败！应该创建超级管理员"
    exit 1
fi

echo -e "\n========================================"
echo "✅ 所有测试通过！超级管理员功能正常工作"
echo "========================================"
echo -e "\n总结："
echo "1. 默认管理员可以登录"
echo "2. 初始设置创建的账号是超级管理员"
echo "3. 超级管理员可以创建普通用户"
echo "4. 超级管理员可以创建其他超级管理员"
