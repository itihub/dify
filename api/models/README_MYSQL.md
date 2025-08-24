# MySQL 数据库支持

本项目已添加对 MySQL 数据库的支持，同时保持与 PostgreSQL 的兼容性。

## 主要修改

### 1. 数据库兼容性模块 (`db_compat.py`)
- `get_uuid_default()`: 根据数据库类型返回适当的 UUID 默认值
- `get_array_column()`: MySQL 使用 JSON，PostgreSQL 使用 ARRAY
- `get_current_timestamp()`: 数据库特定的时间戳函数
- `get_boolean_default()`: 数据库特定的布尔默认值
- `get_varchar_default()`: 数据库特定的字符串默认值

### 2. 引擎配置 (`engine.py`)
- 添加数据库类型检测功能
- 统一的索引命名约定

### 3. 模型文件更新
- `account.py`: 已完全更新支持 MySQL
- `model.py`: 已部分更新，替换了关键的 PostgreSQL 特定函数

### 4. MySQL 配置 (`configs/mysql_config.py`)
- MySQL 连接配置
- 连接字符串生成

## 使用方法

### 环境变量配置
```bash
# 使用 MySQL
DB_HOST=mysql
DB_PORT=3306
DB_USERNAME=dify
DB_PASSWORD=difyai123456
DB_DATABASE=dify

# 使用 PostgreSQL (默认)
DB_HOST=postgres
DB_PORT=5432
DB_USERNAME=postgres
DB_PASSWORD=difyai123456
DB_DATABASE=dify
```

### Docker Compose 使用
```bash
# 启动 PostgreSQL (默认)
docker-compose up

# 启动 MySQL
docker-compose --profile mysql up

# 同时启动两个数据库
docker-compose --profile postgres --profile mysql up
```

## 注意事项

1. **数组字段**: MySQL 中的数组字段使用 JSON 类型存储
2. **UUID 生成**: MySQL 使用 `UUID()` 函数，PostgreSQL 使用 `uuid_generate_v4()`
3. **字符集**: MySQL 配置使用 `utf8mb4` 字符集
4. **时间戳**: 不同数据库的时间戳函数略有差异

## 待完成的工作

- 完成所有模型文件的更新 (dataset.py, workflow.py, 等)
- 添加数据库迁移脚本
- 更新应用配置以支持动态数据库选择
- 添加单元测试验证兼容性