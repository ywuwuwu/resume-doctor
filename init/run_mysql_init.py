#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Execute MySQL initialization script
"""

import mysql.connector
import os

# MySQL配置
MYSQL_CONFIG = {
    'host': 'test.2brain.ai',
    'user': 'Track_B_2',
    'password': 'mfsd123_B_2',
    'database': 'bee_beta2'
}

def execute_sql_file(conn, file_path):
    """执行SQL文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        cursor = conn.cursor()
        
        # 分割SQL语句（按分号分割）
        sql_statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        for statement in sql_statements:
            if statement:
                try:
                    cursor.execute(statement)
                    print(f"Executed: {statement[:50]}...")
                except mysql.connector.Error as err:
                    print(f"Error executing statement: {err}")
                    print(f"Statement: {statement[:100]}...")
        
        conn.commit()
        cursor.close()
        print("SQL file executed successfully!")
        
    except Exception as e:
        print(f"Error reading or executing SQL file: {e}")

def main():
    """主函数"""
    print("Starting MySQL database initialization...")
    
    # 连接到MySQL（不指定数据库，因为数据库可能不存在）
    config_without_db = MYSQL_CONFIG.copy()
    del config_without_db['database']
    
    try:
        conn = mysql.connector.connect(**config_without_db)
        print("Connected to MySQL server")
        
        # 创建数据库（如果不存在）
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_CONFIG['database']}")
        cursor.execute(f"USE {MYSQL_CONFIG['database']}")
        cursor.close()
        print(f"Database {MYSQL_CONFIG['database']} is ready")
        
        # 关闭连接并重新连接到指定数据库
        conn.close()
        
        # 重新连接到指定数据库
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        print(f"Connected to database {MYSQL_CONFIG['database']}")
        
        # 执行初始化SQL文件
        sql_file_path = os.path.join(os.path.dirname(__file__), 'init_mysql.sql')
        execute_sql_file(conn, sql_file_path)
        
        # 显示表结构
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"\nCreated tables: {[table[0] for table in tables]}")
        
        cursor.close()
        conn.close()
        
        print("MySQL database initialization completed successfully!")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    main() 
