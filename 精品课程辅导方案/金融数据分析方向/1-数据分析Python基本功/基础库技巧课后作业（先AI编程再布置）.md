# 📚 课后作业：Python 标准库在数据分析中的应用

## Part 1：`math`

1. **数据标准化**
    给定一组数 `[12.5, 15.3, 17.8, 14.2, 19.6]`，请用 `math` 模块完成如下任务：

   - 计算平均值与标准差（标准差公式自己实现，不用 `numpy`）。
   - 将每个数值做 **Z-Score 标准化**。

   *提示：`math.sqrt`, `math.pow` 可以帮助你。*



------

## Part 2：`pickle`

1. **结果缓存**
    假设你有一个数据分析结果字典：

   ```
   result = {"mean": 15.6, "std": 2.3, "n": 100}
   ```

   - 将其保存为 `result.pkl`
   - 再从 `result.pkl` 中读取并打印结果

   *提示：用 `pickle.dump` 和 `pickle.load`。*

------

## Part 3：`datetime`

1. **时间序列窗口**
    写一个程序：

   - 获取今天日期
   - 生成过去 7 天的日期列表（格式：`YYYY-MM-DD`）
   - 打印结果

   *提示：`datetime.now` + `timedelta`。*