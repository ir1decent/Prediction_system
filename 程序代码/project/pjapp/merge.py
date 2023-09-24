import pandas as pd
import os
'''
source1_file是经纬坐标文件
source2——file是属性文件
target_folder生成图片路径
file——name生成文件名
'''
def merge_csv_columns(source1_file, source2_file, target_folder, file_name):
    df1 = pd.read_csv(source1_file,skiprows=1,delimiter=' ')
    df2 = pd.read_csv(source2_file,skiprows=1)

    merged_df = pd.concat([df1, df2], axis=1)
    target_file =  f'{file_name}.csv'
    target_path = os.path.join(target_folder, target_file)
    merged_df.to_csv(target_path, index=False, sep=' ')

    #print("CSV column merge completed.")

# Example usage
# source1_file = 'test1.csv'
# source2_file = 'test2.csv'
# target_folder = '预测图'
# file_name = '试一下.csv'
#
# merge_csv_columns(source1_file, source2_file, target_folder, file_name)
