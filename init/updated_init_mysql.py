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
            try:
                cursor.execute(statement)
                print(f"Executed: {statement[:60]}...")
            except mysql.connector.Error as err:
                print(f"⚠️ Error executing statement: {err}")
                print(f"↳ Statement: {statement[:100]}...")
        conn.commit()
        cursor.close()
        print("✅ SQL file executed successfully!")

    except Exception as e:
        print(f"❌ Error reading or executing SQL file: {e}")

def show_db_stats(conn):
    """显示数据库统计信息"""
    try:
        cursor = conn.cursor()
        stats_queries = {
            "Total users": "SELECT COUNT(*) FROM user_profiles",
            "Total jobs": "SELECT COUNT(*) FROM job_postings",
            "Total resumes": "SELECT COUNT(*) FROM resumes",
            "Total applications": "SELECT COUNT(*) FROM job_applications"
        }

        print("\n📊 Database Stats:")
        for label, query in stats_queries.items():
            cursor.execute(query)
            result = cursor.fetchone()
            print(f"{label}: {result[0]}")
        cursor.close()
    except Exception as e:
        print(f"⚠️ Error fetching database stats: {e}")

def main():
    """主函数"""
    print("🚀 Starting MySQL database initialization...")

    config_no_db = MYSQL_CONFIG.copy()
    del config_no_db['database']

    try:
        # 连接 MySQL，不指定数据库
        conn = mysql.connector.connect(**config_no_db)
        print("✅ Connected to MySQL server")

        # 创建数据库
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_CONFIG['database']}")
        cursor.execute(f"USE {MYSQL_CONFIG['database']}")
        cursor.close()
        print(f"✅ Database `{MYSQL_CONFIG['database']}` is ready")

        conn.close()

        # 重新连接到目标数据库
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        print(f"✅ Connected to database `{MYSQL_CONFIG['database']}`")

        # 执行初始化 SQL 文件
        sql_file_path = os.path.join(os.path.dirname(__file__), 'init_mysql.sql')
        execute_sql_file(conn, sql_file_path)

        # 显示统计信息
        show_db_stats(conn)

        conn.close()
        print("🎉 MySQL database initialization completed successfully!")

    except mysql.connector.Error as err:
        print(f"❌ MySQL error: {err}")

if __name__ == "__main__":
    main()

