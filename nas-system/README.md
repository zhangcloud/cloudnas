# CloudNAS

这是一个模拟群晖 NAS 系统的前端与后端工程结构。

## 目录说明

- `backend/`: FastAPI 后端服务，包含认证、文件管理、存储、备份与系统接口。
- `frontend/`: Vue 3 + Vite 前端界面，包含登录、文件总管、存储管理与控制面板。
- `docker/`: 后端与前端 Dockerfile，以及 `docker-compose.yml`。
- `scripts/install.sh`: 本地安装脚本。
- `.env.example`: 后端配置示例。

## 模块状态

| 模块 | 功能 | 状态 | 文件位置 |
| --- | --- | --- | --- |
| 用户认证 | JWT 登录 / 注册 | ✅ | `backend/app/api/v1/auth.py` |
| 用户管理 | 用户列表 / 创建 / 删除 | ✅ | `backend/app/api/v1/users.py` |
| 文件管理 | 浏览 / 上传 / 下载 / 删除 / ACL | ✅ | `backend/app/api/v1/files.py` |
| 共享管理 | 共享文件夹 / NFS / CIFS 创建 / 删除 | ✅ | `backend/app/api/v1/shares.py` |
| 存储管理 | ZFS 存储池 / 磁盘管理 (真实 ZFS 调用) | ✅ | `backend/app/api/v1/storage.py` |
| SAN 管理 | iSCSI / FC 协议支持 | ✅ | `backend/app/api/v1/san.py` |
| 网络管理 | IP/DNS/服务状态 | ✅ | `backend/app/api/v1/network.py` |
| 任务调度 | 定时任务管理 | ✅ | `backend/app/api/v1/tasks.py` |
| 系统监控 | CPU / 内存 / 磁盘监控 | ✅ | `backend/app/api/v1/system.py` |
| 日志审计 | 系统日志查看 | ✅ | `backend/app/api/v1/logs.py` |
| 备份恢复 | 备份 / 恢复功能 | ✅ | `backend/app/api/v1/backup.py` |
| 快照管理 | 数据快照创建 / 恢复 | ✅ | `backend/app/api/v1/snapshots.py` |
| 应用中心 | 应用安装 / 卸载 / 插件机制 | ✅ | `backend/app/api/v1/apps.py` |
| DSM 桌面 | 窗口 / 开始菜单 / 任务栏 | ✅ | `frontend/src/layouts/DSMDesktop.vue` |
| 应用管理 | 模块化应用扩展 | ✅ | `frontend/src/components/WindowManager.vue` |
| DSM UI | 现代化卡片式深色主题 | ✅ | `frontend/src/assets/main.css` |

## SAN 存储网络功能

CloudNAS 支持通过 iSCSI 和 FC (Fibre Channel) 协议共享 ZFS 存储：

### iSCSI 支持
- 创建和管理 iSCSI targets
- 添加客户端访问控制 (ACL)
- 支持 LUN 映射到 ZFS 数据集

### FC 支持
- FC target 配置和管理
- WWN (World Wide Name) 管理
- 多端口支持

### 使用方法
1. 在 SAN 管理页面创建 iSCSI 或 FC targets
## 文件夹共享功能

CloudNAS 支持三种共享方式：

### 1. 基本共享 (通用)
- 支持简单的共享文件夹创建和删除
- 统一的 API: `POST /api/v1/shares/create`, `DELETE /api/v1/shares/delete`

### 2. NFS 共享 (Network File System)
- Linux/Unix 系统原生支持
- 支持客户端访问列表和挂载选项配置
- API 端点:
  - `GET /api/v1/shares/nfs/list` - 列出所有 NFS 共享
  - `POST /api/v1/shares/nfs/create` - 创建新 NFS 共享
  - `DELETE /api/v1/shares/nfs/delete` - 删除 NFS 共享

```json
{
  "path": "/tmp/cloudnas_storage/Public",
  "clients": ["192.168.1.0/24"],
  "options": "rw,sync,no_subtree_check"
}
```

### 3. CIFS 共享 (Common Internet File System / SMB)
- Windows 系统原生支持
- 支持公共/私有和读写权限设置
- API 端点:
  - `GET /api/v1/shares/cifs/list` - 列出所有 CIFS 共享
  - `POST /api/v1/shares/cifs/create` - 创建新 CIFS 共享
  - `DELETE /api/v1/shares/cifs/delete` - 删除 CIFS 共享

```json
{
  "name": "SharedFolder",
  "path": "/tmp/cloudnas_storage/SharedFolder",
  "comment": "Shared folder description",
  "public": true,
  "writable": true
}
```

### 开发环境

在开发环境中，所有共享操作都在内存中进行，不需要实际的 NFS/CIFS 工具。

### 生产环境

在生产环境中 (设置 `ENVIRONMENT=production`)，CloudNAS 使用：
- **NFS**: `exportfs` 命令配置 `/etc/exports`
- **CIFS**: `net` 命令配置 Samba `/etc/samba/smb.conf`

## SAN 存储网络功能

CloudNAS 支持通过 iSCSI 和 FC (Fibre Channel) 协议共享 ZFS 存储：

### iSCSI 支持
- 创建和管理 iSCSI targets
- 添加客户端访问控制 (ACL)
- 支持 LUN 映射到 ZFS 数据集

### FC 支持
- FC target 配置和管理
- WWN (World Wide Name) 管理
- 多端口支持

### 使用方法
1. 在 SAN 管理页面创建 iSCSI 或 FC targets
2. 配置相应的 LUN 或存储映射
3. 客户端可以通过 iSCSI initiator 或 FC HBA 连接

### 依赖要求
- iSCSI: `targetcli` 工具
- FC: 相应的 FC HBA 硬件和驱动

### 本地运行

1. 安装后端依赖:
   ```bash
   cd nas-system
   bash scripts/install.sh
   ```
2. 启动后端:
   ```bash
   cd backend
   source .venv/bin/activate
   uvicorn main:app --reload
   ```
3. 启动前端:
   ```bash
   cd frontend
   npm run dev
   ```

### Docker 运行

```bash
cd nas-system
docker compose up --build
```

### 测试共享功能

运行测试脚本验证 NFS 和 CIFS 共享功能:

```bash
bash test_shares.sh
```

## 默认登录

- 用户名: `admin`
- 密码: `admin123`
