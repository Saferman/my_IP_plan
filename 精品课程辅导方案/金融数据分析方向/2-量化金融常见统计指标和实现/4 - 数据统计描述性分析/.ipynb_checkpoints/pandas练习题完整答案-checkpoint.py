# pandas 数据统计描述性分析 - 完整答案
# 作者：AI助手
# 说明：这是对原notebook中所有练习题的完整解答

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

print("=== pandas 数据统计描述性分析练习题答案 ===\n")

# 加载数据
df = pd.read_excel("2020年中国大学排名.xlsx")
print("✅ 数据加载成功！")
print(f"数据形状: {df.shape}")
print(f"列名: {list(df.columns)}")

print("\n" + "="*60 + "\n")

# 1 - 查看数据前 10 行
print("1. 查看数据前 10 行:")
print("代码: df.head(10)")
result_1 = df.head(10)
print(result_1)
print("\n" + "-"*50 + "\n")

# 2 - 修改索引为学校名称列
print("2. 修改索引为学校名称列:")
print("代码: df = df.set_index('学校名称')")
df = df.set_index('学校名称')
print("✅ 索引修改完成")
print(f"新的索引: {df.index.name}")
print(f"前5个索引值: {list(df.index[:5])}")
print("\n" + "-"*50 + "\n")

# 3 - 查看数据量（总单元格数量）
print("3. 查看数据量（总单元格数量）:")
print("代码: df.size")
total_cells = df.size
print(f"数据框总单元格数量: {total_cells}")
print(f"行数: {df.shape[0]}, 列数: {df.shape[1]}")
print(f"验证: {df.shape[0]} × {df.shape[1]} = {df.shape[0] * df.shape[1]}")
print("\n" + "-"*50 + "\n")

# 4 - 按总分升序排列，查看倒数20名
print("4. 按总分升序排列，查看倒数20名:")
print("代码: df.sort_values('总分', ascending=True).head(20)")
bottom_20 = df.sort_values('总分', ascending=True).head(20)
print("总分最低的20所大学:")
print(bottom_20[['总分', '省市', '类型']] if '类型' in df.columns else bottom_20[['总分', '省市']])
print("\n" + "-"*50 + "\n")

# 5 - 按高端人才得分降序排序，展示前10位
print("5. 按高端人才得分降序排序，展示前10位:")
print("代码: df.sort_values('高端人才得分', ascending=False).head(10)")
if '高端人才得分' in df.columns:
    top_talent = df.sort_values('高端人才得分', ascending=False).head(10)
    print("高端人才得分最高的10所大学:")
    print(top_talent[['高端人才得分', '总分', '省市']])
else:
    print("❌ 未找到'高端人才得分'列")
print("\n" + "-"*50 + "\n")

# 6 - 查看各项得分最高的学校名称
print("6. 查看各项得分最高的学校名称:")
print("代码: 遍历数值列，找出每列的最大值对应的学校")
score_columns = [col for col in df.columns if '得分' in col or col == '总分']
print("各项得分最高的学校:")
for col in score_columns:
    if col in df.columns:
        max_school = df[col].idxmax()
        max_score = df[col].max()
        print(f"  {col}: {max_school} ({max_score}分)")
print("\n" + "-"*50 + "\n")

# 7 - 计算总分列的均值
print("7. 计算总分列的均值:")
print("代码: df['总分'].mean()")
total_score_mean = df['总分'].mean()
print(f"总分的均值: {total_score_mean:.2f}")
print("\n" + "-"*50 + "\n")

# 8 - 计算总分列的中位数
print("8. 计算总分列的中位数:")
print("代码: df['总分'].median()")
total_score_median = df['总分'].median()
print(f"总分的中位数: {total_score_median:.2f}")
print("\n" + "-"*50 + "\n")

# 9 - 计算总分列的众数
print("9. 计算总分列的众数:")
print("代码: df['总分'].mode()")
total_score_mode = df['总分'].mode()
print(f"总分的众数: {total_score_mode.values}")
print(f"众数个数: {len(total_score_mode)}")
print("\n" + "-"*50 + "\n")

# 10 - 计算指定列的统计信息
print("10. 计算总分、高端人才得分、办学层次得分的统计信息:")
print("代码: df[selected_columns].agg(['max', 'min', 'median', 'mean'])")
available_columns = [col for col in ['总分', '高端人才得分', '办学层次得分'] if col in df.columns]
if available_columns:
    stats_summary = df[available_columns].agg(['max', 'min', 'median', 'mean']).round(2)
    print("选定列的统计信息:")
    print(stats_summary)
else:
    print("❌ 未找到指定的列")
print("\n" + "-"*50 + "\n")

# 11 - 查看数值型数据的完整统计信息
print("11. 查看数值型数据的完整统计信息:")
print("代码: df.describe().round(2)")
numeric_stats = df.describe().round(2)
print("数值型数据的完整统计信息:")
print(numeric_stats)
print("\n" + "-"*50 + "\n")

# 12 - 计算各省市总分均值
print("12. 计算各省市总分均值:")
print("代码: df.groupby('省市')['总分'].mean().sort_values(ascending=False)")
if '省市' in df.columns:
    province_avg_score = df.groupby('省市')['总分'].mean().sort_values(ascending=False)
    print("各省市总分均值（降序排列）:")
    print(province_avg_score.round(2))
else:
    print("❌ 未找到'省市'列")
print("\n" + "-"*50 + "\n")

# 13 - 计算相关系数矩阵
print("13. 计算相关系数矩阵:")
print("代码: df.select_dtypes(include=[np.number]).corr().round(3)")
correlation_matrix = df.select_dtypes(include=[np.number]).corr()
print("数值型变量的相关系数矩阵:")
print(correlation_matrix.round(3))
print("\n" + "-"*50 + "\n")

# 14 - 绘制相关系数热力图
print("14. 绘制相关系数热力图:")
print("代码: sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')")
try:
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, 
                annot=True,
                cmap='coolwarm',
                center=0,
                square=True,
                fmt='.2f',
                cbar_kws={'shrink': 0.8})
    plt.title('大学排名数据相关系数热力图', fontsize=16, pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig('相关系数热力图.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✅ 热力图已生成并保存为 '相关系数热力图.png'")
except Exception as e:
    print(f"❌ 绘图出错: {e}")
print("\n" + "-"*50 + "\n")

# 15 - 计算各省市出现的次数
print("15. 计算各省市出现的次数:")
print("代码: df['省市'].value_counts()")
if '省市' in df.columns:
    province_counts = df['省市'].value_counts()
    print("各省市高校数量统计:")
    print(province_counts)
    
    # 可视化
    try:
        plt.figure(figsize=(12, 8))
        province_counts.head(15).plot(kind='bar')
        plt.title('各省市高校上榜数量（前15名）', fontsize=14)
        plt.xlabel('省市')
        plt.ylabel('高校数量')
        plt.xticks(rotation=45)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig('省市高校数量统计.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("✅ 柱状图已生成并保存为 '省市高校数量统计.png'")
    except Exception as e:
        print(f"❌ 绘图出错: {e}")
else:
    print("❌ 未找到'省市'列")
print("\n" + "-"*50 + "\n")

# 16 - 地图可视化（简化版）
print("16. 地图可视化:")
print("代码: 使用matplotlib绘制简单条形图代替地图")
if '省市' in df.columns:
    try:
        plt.figure(figsize=(15, 8))
        province_counts = df['省市'].value_counts()
        province_counts.plot(kind='bar')
        plt.title('各省市高校上榜数量分布', fontsize=16)
        plt.xlabel('省市')
        plt.ylabel('高校数量')
        plt.xticks(rotation=45)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig('省市分布图.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("✅ 分布图已生成并保存为 '省市分布图.png'")
        print("💡 如需真正的地图，请安装pyecharts: pip install pyecharts")
    except Exception as e:
        print(f"❌ 绘图出错: {e}")
print("\n" + "-"*50 + "\n")

# 17 - 绘制总分的直方图和密度估计图
print("17. 绘制总分的直方图和密度估计图:")
print("代码: plt.hist() 和 df['总分'].plot(kind='density')")
try:
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # 直方图
    axes[0].hist(df['总分'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    axes[0].set_title('总分分布直方图', fontsize=14)
    axes[0].set_xlabel('总分')
    axes[0].set_ylabel('频数')
    axes[0].grid(alpha=0.3)
    
    # 添加统计线
    mean_score = df['总分'].mean()
    median_score = df['总分'].median()
    axes[0].axvline(mean_score, color='red', linestyle='--', label=f'均值: {mean_score:.1f}')
    axes[0].axvline(median_score, color='green', linestyle='--', label=f'中位数: {median_score:.1f}')
    axes[0].legend()
    
    # 密度估计图
    df['总分'].plot(kind='density', ax=axes[1], color='orange', linewidth=2)
    axes[1].set_title('总分密度估计图', fontsize=14)
    axes[1].set_xlabel('总分')
    axes[1].set_ylabel('密度')
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('总分分布图.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 输出描述性统计
    print("✅ 分布图已生成并保存为 '总分分布图.png'")
    print("\n总分的描述性统计:")
    print(f"均值: {df['总分'].mean():.2f}")
    print(f"中位数: {df['总分'].median():.2f}")
    print(f"标准差: {df['总分'].std():.2f}")
    print(f"偏度: {df['总分'].skew():.2f}")
    print(f"峰度: {df['总分'].kurtosis():.2f}")
    
except Exception as e:
    print(f"❌ 绘图出错: {e}")

print("\n" + "="*60)
print("🎉 所有练习题答案已完成！")
print("📊 生成的图片文件:")
print("  - 相关系数热力图.png")
print("  - 省市高校数量统计.png") 
print("  - 省市分布图.png")
print("  - 总分分布图.png")
print("="*60)

# 额外分析：深入洞察
print("\n📈 额外分析 - 深入洞察:")

# 不同类型大学的分析
if '类型' in df.columns:
    print("\n1. 不同类型大学的总分分布:")
    type_stats = df.groupby('类型')['总分'].agg(['count', 'mean', 'std', 'min', 'max']).round(2)
    print(type_stats)
    
    # 箱线图
    try:
        plt.figure(figsize=(12, 8))
        df.boxplot(column='总分', by='类型', ax=plt.gca())
        plt.title('不同类型大学总分分布箱线图')
        plt.suptitle('')  # 移除自动生成的标题
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('类型分布箱线图.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("✅ 箱线图已保存为 '类型分布箱线图.png'")
    except Exception as e:
        print(f"❌ 箱线图绘制出错: {e}")

# Top 10 vs Bottom 10 对比
print("\n2. Top 10 vs Bottom 10 对比:")
top_10 = df.nlargest(10, '总分')
bottom_10 = df.nsmallest(10, '总分')

print("\nTop 10 大学:")
display_cols = ['总分', '省市']
if '类型' in df.columns:
    display_cols.append('类型')
print(top_10[display_cols].round(2))

print("\nBottom 10 大学:")
print(bottom_10[display_cols].round(2))

print("\n🎯 分析完成！这些答案涵盖了pandas数据统计描述性分析的核心技能。")
