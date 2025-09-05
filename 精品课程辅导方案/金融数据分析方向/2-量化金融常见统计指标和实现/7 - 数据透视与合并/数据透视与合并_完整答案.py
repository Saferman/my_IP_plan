# 数据透视与合并 - 完整答案
# 作者：AI助手
# 说明：这是对数据透视与合并notebook中所有练习题的完整解答

import pandas as pd
import numpy as np

print("=== 数据透视与合并练习题完整答案 ===\n")

# 1 - 加载数据
print("1. 加载数据")
print("代码: df = pd.read_csv('某超市销售数据.csv', thousands=',')")

try:
    df = pd.read_csv("某超市销售数据.csv", thousands=',')
    print("✅ 数据加载成功！")
    print(f"数据形状: {df.shape}")
    print(f"列名: {list(df.columns)}")
    print("\n数据前5行:")
    print(df.head())
    print("\n" + "="*60 + "\n")
except FileNotFoundError:
    print("❌ 找不到数据文件，请确保 '某超市销售数据.csv' 在当前目录")
    exit()

# 2 - 数据透视｜默认 - 制作各省「平均销售额」的数据透视表
print("2. 数据透视｜默认 - 各省平均销售额")
print("代码: df.pivot_table(values='销售额', index='省/自治区')")

pivot_2 = df.pivot_table(values='销售额', index='省/自治区')
print("各省平均销售额:")
print(pivot_2.round(2))
print("\n" + "-"*50 + "\n")

# 3 - 数据透视｜指定方法 - 制作各省「销售总额」的数据透视表
print("3. 数据透视｜指定方法 - 各省销售总额")
print("代码: df.pivot_table(values='销售额', index='省/自治区', aggfunc='sum')")

pivot_3 = df.pivot_table(values='销售额', index='省/自治区', aggfunc='sum')
print("各省销售总额:")
print(pivot_3.round(2))
print("\n" + "-"*50 + "\n")

# 4 - 数据透视｜多方法 - 制作各省「销售总额」与「平均销售额」的数据透视表
print("4. 数据透视｜多方法 - 各省销售总额与平均销售额")
print("代码: df.pivot_table(values='销售额', index='省/自治区', aggfunc=['sum', 'mean'])")

pivot_4 = df.pivot_table(values='销售额', index='省/自治区', aggfunc=['sum', 'mean'])
print("各省销售总额与平均销售额:")
print(pivot_4.round(2))
print("\n" + "-"*50 + "\n")

# 5 - 数据透视｜多指标 - 制作各省市「销售总额」与「利润总额」的数据透视表
print("5. 数据透视｜多指标 - 各省销售总额与利润总额")
print("代码: df.pivot_table(values=['销售额', '利润'], index='省/自治区', aggfunc='sum')")

pivot_5 = df.pivot_table(values=['销售额', '利润'], index='省/自治区', aggfunc='sum')
print("各省销售总额与利润总额:")
print(pivot_5.round(2))
print("\n" + "-"*50 + "\n")

# 6 - 数据透视｜多索引 - 制作「各省市」与「不同类别」产品「销售总额」的数据透视表
print("6. 数据透视｜多索引 - 各省市与不同类别产品销售总额")
print("代码: df.pivot_table(values='销售额', index=['省/自治区', '类别'], aggfunc='sum')")

pivot_6 = df.pivot_table(values='销售额', index=['省/自治区', '类别'], aggfunc='sum')
print("各省市与不同类别产品销售总额:")
print(pivot_6.round(2))
print("\n" + "-"*50 + "\n")

# 7 - 数据透视｜多层 - 制作各省市「不同类别」产品的「销售总额」透视表
print("7. 数据透视｜多层 - 各省市不同类别产品销售总额（列透视）")
print("代码: df.pivot_table(values='销售额', index='省/自治区', columns='类别', aggfunc='sum')")

pivot_7 = df.pivot_table(values='销售额', index='省/自治区', columns='类别', aggfunc='sum')
print("各省市不同类别产品销售总额:")
print(pivot_7.round(2))
print("\n" + "-"*50 + "\n")

# 8 - 数据透视｜综合 - 制作「各省市」、「不同类别」产品「销售量与销售额」的「均值与总和」的数据透视表，并在最后追加一行『合计』
print("8. 数据透视｜综合 - 复杂透视表")
print("代码: df.pivot_table(values=['数量', '销售额'], index='省/自治区', columns='类别', aggfunc=['mean', 'sum'], margins=True)")

pivot_8 = df.pivot_table(values=['数量', '销售额'], 
                        index='省/自治区', 
                        columns='类别', 
                        aggfunc=['mean', 'sum'], 
                        margins=True)
print("各省市、不同类别产品销售量与销售额的均值与总和:")
print(pivot_8.round(2))
print("\n" + "-"*50 + "\n")

# 9 - 数据透视｜筛选 - 在上一题的基础上，查询「类别」等于「办公用品」的详情
print("9. 数据透视｜筛选 - 查询办公用品类别")
print("代码: pivot_8.loc[:, (slice(None), '办公用品')]")

try:
    # 筛选办公用品类别的数据
    office_supplies = pivot_8.loc[:, (slice(None), '办公用品')]
    print("办公用品类别详情:")
    print(office_supplies.round(2))
except KeyError:
    print("注意：列名可能不完全匹配，让我们查看实际的列名")
    print("实际列名:", pivot_8.columns.tolist())
    # 尝试其他可能的列名
    for col in pivot_8.columns:
        if '办公用品' in str(col):
            print(f"找到匹配列: {col}")
print("\n" + "-"*50 + "\n")

# 10 - 数据透视｜逆透视 - 将第5题的透视表进行逆透视
print("10. 数据透视｜逆透视 - 将宽表转换为长表")
print("代码: pivot_5.reset_index().melt(id_vars='省/自治区', var_name='指标', value_name='数值')")

# 重新创建第5题的透视表用于逆透视
pivot_5_for_melt = df.pivot_table(values=['销售额', '利润'], index='省/自治区', aggfunc='sum')
pivot_5_reset = pivot_5_for_melt.reset_index()

# 进行逆透视
melted_data = pivot_5_reset.melt(id_vars='省/自治区', var_name='指标', value_name='数值')
print("逆透视结果:")
print(melted_data.head(10))
print(f"逆透视后数据形状: {melted_data.shape}")
print("\n" + "-"*50 + "\n")

# 额外分析：数据合并示例
print("=== 数据合并示例 ===")

# 创建示例数据用于合并演示
print("创建示例数据进行合并演示:")

# 数据1：省份信息
province_info = pd.DataFrame({
    '省/自治区': ['北京', '上海', '广东', '江苏', '浙江'],
    '地区': ['华北', '华东', '华南', '华东', '华东'],
    '经济水平': ['发达', '发达', '发达', '发达', '发达']
})

# 数据2：从原数据中提取的省份销售汇总
province_sales = df.groupby('省/自治区').agg({
    '销售额': 'sum',
    '利润': 'sum',
    '数量': 'sum'
}).reset_index()

print("\n省份信息表:")
print(province_info)
print("\n省份销售汇总表:")
print(province_sales.head())

# 使用merge进行合并
print("\n使用merge进行内连接:")
merged_data = pd.merge(province_info, province_sales, on='省/自治区', how='inner')
print(merged_data)

print("\n使用concat进行垂直合并示例:")
# 创建两个相同结构的数据框
df1 = df[df['省/自治区'] == '北京'].head(3)
df2 = df[df['省/自治区'] == '上海'].head(3)

concat_result = pd.concat([df1, df2], ignore_index=True)
print("合并后的数据:")
print(concat_result[['省/自治区', '类别', '销售额', '利润']])

print("\n" + "="*60)
print("🎉 所有练习题答案已完成！")
print("\n📊 主要知识点总结:")
print("1. pivot_table() - 数据透视表创建")
print("2. aggfunc参数 - 聚合函数设置（sum, mean, count等）")
print("3. index和columns - 行索引和列索引设置")
print("4. values参数 - 要聚合的数值列")
print("5. margins参数 - 添加合计行/列")
print("6. melt() - 逆透视，宽表转长表")
print("7. merge() - 数据合并")
print("8. concat() - 数据连接")
print("="*60)
