#!/bin/bash

# CloudNAS 共享功能测试脚本

BASE_URL="http://localhost:8000/api/v1"
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc3ODIzNTI5Nn0.NqDpl188r01MzXNrxa8twYz0uNo15RVHlsET6nDA_QU"

echo "=== CloudNAS 共享功能测试 ==="
echo ""

# 测试 NFS 列表
echo "1. 测试 NFS 共享列表"
curl -s -H "Authorization: Bearer $TOKEN" "$BASE_URL/shares/nfs/list" | jq . || echo "FAILED"
echo ""

# 测试 CIFS 列表
echo "2. 测试 CIFS 共享列表"
curl -s -H "Authorization: Bearer $TOKEN" "$BASE_URL/shares/cifs/list" | jq . || echo "FAILED"
echo ""

# 创建 NFS 共享
echo "3. 创建新的 NFS 共享"
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"path": "/tmp/cloudnas_storage/NFSTest", "clients": ["192.168.1.0/24"], "options": "rw,sync"}' \
  "$BASE_URL/shares/nfs/create" | jq . || echo "FAILED"
echo ""

# 创建 CIFS 共享
echo "4. 创建新的 CIFS 共享"
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "CifsTest", "path": "/tmp/cloudnas_storage/CifsTest", "comment": "Test CIFS share", "public": true, "writable": true}' \
  "$BASE_URL/shares/cifs/create" | jq . || echo "FAILED"
echo ""

# 验证创建后 NFS 列表
echo "5. 验证 NFS 共享列表（应包含新创建的共享）"
curl -s -H "Authorization: Bearer $TOKEN" "$BASE_URL/shares/nfs/list" | jq . || echo "FAILED"
echo ""

# 验证创建后 CIFS 列表
echo "6. 验证 CIFS 共享列表（应包含新创建的共享）"
curl -s -H "Authorization: Bearer $TOKEN" "$BASE_URL/shares/cifs/list" | jq . || echo "FAILED"
echo ""

# 测试通用共享列表
echo "7. 测试通用共享列表（NFS + CIFS）"
curl -s -H "Authorization: Bearer $TOKEN" "$BASE_URL/shares/list" | jq . || echo "FAILED"
echo ""

echo "=== 测试完成 ==="
