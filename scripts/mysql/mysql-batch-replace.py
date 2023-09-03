#请先安装依赖pip install mysql-connector-python
#修改下面db_config内的mysql服务器相关配置
#修改被替换的字符串：search_string内容
#修改替换后的字符串：replace_string内容

import mysql.connector

# 配置数据库连接
db_config = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'your_host',
    'database': 'your_database'
}

# 创建数据库连接
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# 定义要查找和替换的字符串
search_string = 'old_string'
replace_string = 'new_string'

try:
    # 获取数据库中的所有表名
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]

    # 遍历每个表并执行替换操作
    for table in tables:
        # 获取表的列信息
        cursor.execute(f"DESCRIBE {table}")
        columns = [column[0] for column in cursor.fetchall()]

        for column in columns:
            # 构建 SQL 查询语句
            query = f"UPDATE {table} SET {column} = REPLACE({column}, %s, %s)"
            
            # 执行替换操作
            cursor.execute(query, (search_string, replace_string))
            conn.commit()

    print("替换完成。")

except mysql.connector.Error as err:
    print(f"错误: {err}")

finally:
    # 关闭数据库连接
    cursor.close()
    conn.close()


