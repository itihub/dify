# MySQL 版本支持说明

## UUID 默认值支持

### MySQL 版本差异
- **MySQL 8.0+**: 支持 `UUID()` 函数作为列的默认值
- **MySQL < 8.0**: 不支持函数调用作为默认值

### 当前实现
`get_uuid_default()` 函数已更新以支持版本检测：

```python
def get_uuid_default():
    """Get appropriate UUID default value based on database type and version"""
    scheme = os.getenv('SQLALCHEMY_DATABASE_URI_SCHEME', 'postgresql')
    if 'mysql' in scheme:
        mysql_version = _get_mysql_version()
        if mysql_version >= 8.0:
            # MySQL 8.0+ supports UUID() as default value
            return sa.text("(UUID())")
        else:
            # MySQL < 8.0 doesn't support function calls as default values
            return None  # Will be handled by application code
    else:
        # PostgreSQL uses uuid_generate_v4()
        return sa.text("uuid_generate_v4()")
```

### 配置方式
在 `.env` 文件中设置 MySQL 版本：
```bash
MYSQL_VERSION=8.0  # 或您实际使用的版本，如 5.7
```

### 处理策略
1. **MySQL 8.0+**: 使用数据库级别的 `UUID()` 默认值
2. **MySQL < 8.0**: 
   - `server_default=None`
   - 依赖 SQLAlchemy 的 `default` 参数在应用层生成 UUID
   - 或使用数据库触发器

### 兼容性
- ✅ PostgreSQL: 使用 `uuid_generate_v4()`
- ✅ MySQL 8.0+: 使用 `UUID()`
- ✅ MySQL < 8.0: 应用层 UUID 生成

这确保了在所有支持的数据库版本中都能正确处理 UUID 生成。