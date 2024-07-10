import pandas as pd
import folium

# 读取CSV文件
file_path = 'xiuchuan.csv'

# 尝试不同的编码读取文件
ais_data = None
encodings = ['utf-8', 'ISO-8859-1', 'latin1', 'GBK']

for encoding in encodings:
    try:
        ais_data = pd.read_csv(file_path, encoding=encoding)
        print(f"成功使用编码 {encoding} 读取文件")
        break
    except Exception as e:
        print(f"使用编码 {encoding} 读取文件失败: {e}")

if ais_data is None:
    print("所有尝试的编码都无法读取文件，请检查文件编码或文件内容。")
    exit()

# 打印前几行数据
print(ais_data.head())

# 确认经纬度列存在
if 'lat' not in ais_data.columns or 'lon' not in ais_data.columns:
    print("数据中缺少 'lat' 或 'lon' 列。")
    exit()

# 检查空值和数据类型
print(f"空值检查：\n{ais_data[['lat', 'lon']].isnull().sum()}")
print(f"数据类型检查：\n{ais_data[['lat', 'lon']].dtypes}")

# 清洗数据
ais_data = ais_data.dropna(subset=['lat', 'lon'])  # 删除包含空值的行
ais_data = ais_data[(ais_data['lat'].apply(lambda x: isinstance(x, (int, float)))) &
                    (ais_data['lon'].apply(lambda x: isinstance(x, (int, float))))]  # 确保经纬度为数字

# 将经纬度转换为浮点数
ais_data['lat'] = ais_data['lat'].astype(float)
ais_data['lon'] = ais_data['lon'].astype(float)

# 打印清洗后的数据
print(f"清洗后数据:\n{ais_data[['lat', 'lon']].head()}")

# 创建地图中心点
map_center = [ais_data['lat'].mean(), ais_data['lon'].mean()]
print(f"地图中心位置: {map_center}")

# 创建地图对象
map_ais = folium.Map(location=map_center, zoom_start=12)

# 添加标记
row_count = 0
for idx, row in ais_data.iterrows():
    lat = row['lat']
    lon = row['lon']

    # 检查每一行的数据
    if pd.notnull(lat) and pd.notnull(lon):
        try:
            folium.CircleMarker(
                location=[lat, lon],
                radius=1,
                color='red',
                fill=True,
                fill_color='red',
                fill_opacity=0.9
            ).add_to(map_ais)

            print(f"添加标记: 第 {idx} 行, lat={lat}, lon={lon}")
            row_count += 1
        except ValueError as e:
            print(f"数据格式错误：第 {idx} 行，lat={lat}, lon={lon}，错误信息：{e}")
    else:
        print(f"跳过空值：第 {idx} 行，lat={lat}, lon={lon}")

print(f"总共处理了 {row_count} 行")

# 保存地图
map_ais.save('ais_map.html')
print("地图已保存为 'ais_map.html'，请在浏览器中打开查看。")
