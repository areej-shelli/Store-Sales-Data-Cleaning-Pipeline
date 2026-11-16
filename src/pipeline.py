import pandas as pd
import numpy as np
import sqlite3 as sq

# تجهيز عينة مبيعات خام تحتوي على فجوات زمنية وقيم شاذة
raw_data = {
    'date': ['2026-03-01', '2026-03-03', '2026-03-04', '2026-03-06', '2026-03-07'], # ملاحظة: يوم 2 و 5 مارس غير متوفرين
    'sales': [120, 150, 130, 99999, 140] # 99999 خطأ إدخال (Outlier)
}

df_raw = pd.DataFrame(raw_data)
print("--- Raw Data ---")
print(df_raw)
print("\n" + "="*50 + "\n")

# 1. تحويل عمود التاريخ إلى datetime
df_raw['date'] = pd.to_datetime(df_raw['date'])

# 2. فلترة القيم الشاذة باستخدام IQR
Q1 = df_raw['sales'].quantile(0.25)
Q3 = df_raw['sales'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# استبعاد القيم الشاذة وتفريغها
df_clean = df_raw[(df_raw['sales'] >= lower_bound) & (df_raw['sales'] <= upper_bound)].copy()

# 3. معالجة الفجوات الزمنية وملء الأيام الناقصة بأصفار
df_clean = df_clean.set_index('date').asfreq('D', fill_value=0).reset_index()

print("--- Cleaned & Reindexed Data ---")
print(df_clean)
print("\n" + "="*50 + "\n")

# 4. حفظ البيانات المنظفة في SQLite
conn = sq.connect("store_sales.db")
df_clean.to_sql('sales_daily', conn, if_exists='replace', index=False)

# 5. حساب المتوسط المتحرك (3-Day Rolling Average) باستخدام SQL Window Functions
sql_query = """
SELECT 
    date,
    sales,
    AVG(sales) OVER (
        ORDER BY date 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS rolling_avg_3d
FROM sales_daily;
"""

df_final = pd.read_sql(sql_query, conn)

print("--- Final Results with Rolling Average ---")
print(df_final)

conn.close()
