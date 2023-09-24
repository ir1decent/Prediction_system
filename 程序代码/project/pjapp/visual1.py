import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata
import time
import os



def Visualize(file_path,output_folder,file_name):
    data = pd.read_csv(file_path,sep='[,\s+]',engine='python')

    columns = data.columns.tolist()
    x_col = columns[0]
    y_col = columns[1]
    z_col = columns[2]
    # 提取经度、纬度和人口数据
    longitude = data[x_col]
    latitude = data[y_col]
    z = data[z_col]

    # 创建网格点
    grid_x, grid_y = np.mgrid[min(longitude):max(longitude):100j, min(latitude):max(latitude):100j]

    # 扁平化经度、纬度和人口数据
    longitude_flat = longitude.to_numpy()
    latitude_flat = latitude.to_numpy()
    z_flat = z.to_numpy()

    # 插值计算人口密度
    grid_z = griddata((longitude_flat, latitude_flat), z_flat, (grid_x, grid_y), method='linear')

    # 绘制等高线图
    plt.contourf(grid_x, grid_y, grid_z, levels=20, cmap='viridis')
    plt.colorbar(label='Z')
    plt.scatter(longitude, latitude, c=z, cmap='viridis', edgecolors='k')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('My Visualization')
    #plt.show()
    file_name=file_name.split('.')[0]
    # 设置可视化图片的文件名，加上唯一ID避免文件名冲突
    visualization_file = f'{file_name}.png'
    # 将可视化图片存储在指定路径下的文件夹
    visualization_path = os.path.join(output_folder, visualization_file)
    plt.savefig(visualization_path)
    # 将可视化图片存储在指定路径下的文件夹
    visualization_path = os.path.join(output_folder, visualization_file)
    plt.savefig(visualization_path)
'''
# 定义文件路径和输出文件夹路径
file_path = '路径/到/你的/Excel文件.xlsx'
output_folder = '路径/到/你的/输出文件夹'
#生成一个时间戳，作为图片的名字
unique_id = str(int(time.time()))
Visualize(file_path,out_folder,unique_id)
'''
# file_path = '试一下.csv'
# output_folder = '预测图'
# unique_id = str(int(time.time()))
# file_name = '123预测'
# Visualize(file_path,output_folder,unique_id,file_name)