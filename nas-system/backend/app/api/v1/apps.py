from fastapi import APIRouter, Depends, Body
from app.core.security import verify_token
import os
import importlib.util

router = APIRouter()

fake_apps = [
    {"id": "app1", "name": "文件管理器", "version": "1.0.0", "status": "installed"},
    {"id": "app2", "name": "备份中心", "version": "1.0.0", "status": "installed"},
    {"id": "app3", "name": "Cloud Sync", "version": "1.0.0", "status": "available"},
]

PLUGINS_DIR = os.path.join(os.path.dirname(__file__), '../../../plugins')

@router.get("/list")
def list_apps(token: str = Depends(verify_token)):
    # Load installed plugins
    installed_plugins = []
    if os.path.exists(PLUGINS_DIR):
        for item in os.listdir(PLUGINS_DIR):
            if item.endswith('.py'):
                installed_plugins.append({
                    "id": item[:-3],
                    "name": item[:-3].replace('_', ' ').title(),
                    "version": "1.0.0",
                    "status": "installed"
                })
    return {"apps": fake_apps + installed_plugins}

@router.post("/install")
def install_app(app_id: str = Body(...), token: str = Depends(verify_token)):
    for app in fake_apps:
        if app["id"] == app_id:
            app["status"] = "installed"
            return {"message": "应用已安装", "app": app}
    # Check if it's a plugin
    plugin_path = os.path.join(PLUGINS_DIR, f"{app_id}.py")
    if os.path.exists(plugin_path):
        return {"message": "插件已存在", "app": {"id": app_id, "name": app_id, "version": "1.0.0", "status": "installed"}}
    return {"message": "应用未找到", "app_id": app_id}

@router.post("/uninstall")
def uninstall_app(app_id: str = Body(...), token: str = Depends(verify_token)):
    for app in fake_apps:
        if app["id"] == app_id:
            app["status"] = "available"
            return {"message": "应用已卸载", "app": app}
    # Check if it's a plugin
    plugin_path = os.path.join(PLUGINS_DIR, f"{app_id}.py")
    if os.path.exists(plugin_path):
        os.remove(plugin_path)
        return {"message": "插件已卸载", "app": {"id": app_id}}
    return {"message": "应用未找到", "app_id": app_id}

@router.post("/run")
def run_plugin(plugin_id: str = Body(...), token: str = Depends(verify_token)):
    plugin_path = os.path.join(PLUGINS_DIR, f"{plugin_id}.py")
    if not os.path.exists(plugin_path):
        return {"message": "插件未找到", "plugin_id": plugin_id}
    try:
        spec = importlib.util.spec_from_file_location(plugin_id, plugin_path)
        plugin = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(plugin)
        if hasattr(plugin, 'run'):
            result = plugin.run()
            return {"message": "插件执行成功", "result": result}
        else:
            return {"message": "插件无 run 函数"}
    except Exception as e:
        return {"message": f"插件执行失败: {str(e)}"}
