import requests
from openpyxl import Workbook
from openpyxl.worksheet.dimensions import ColumnDimension, RowDimension
from openpyxl.styles import Alignment
from datetime import datetime

# 设置请求的URL和POST数据
url = 'https://...'  # 替换为目标URL

cookie = "?????????"

data = {
    'examId': '?????????',
    'uuid': '?????????'
}

headers = {
    'Cookie': cookie
}

# 发送POST请求
response = requests.post(url, data=data, headers=headers, verify=False)

if response.status_code == 200:
    try:
        json_data = response.json()  # 解析JSON响应
        
        # 创建一个新的Excel工作簿
        wb = Workbook()
        ws = wb.active
        
        # 写入表头，包括新增的序号列
        ws.append(['序号', '题目', '答案', '题型'])
        
        for i, item in enumerate(json_data, start=1):
            if 'text_key' in item:
                text_key_data = item['text_key']
                content = text_key_data['content']
                options = [text_key_data['optionA'], text_key_data['optionB'],
                           text_key_data['optionC'], text_key_data['optionD'],
                           text_key_data['optionE']]
                
                # 过滤掉为null的选项，并在每个选项结尾换行
                options_string = '\n'.join(f'{chr(30+i)}、{options[i]}' for i in range(5) if options[i] is not None)
                
                # 根据题目序号判断题型
                question_type = '单选题' if i <= 10 else '多选题'
                
                # 将数据写入Excel的不同行，包括新增的序号列
                ws.append([i, f'{content}\n{options_string}', '', question_type])
                
            else:
                print('未找到text_key字段内容')
        
        # 设置列宽
        column_dimension = ColumnDimension(ws, 'A')
        column_dimension.width = 5  # 调整序号列的宽度
        ws.column_dimensions['A'] = column_dimension
        
        column_dimension = ColumnDimension(ws, 'B')
        column_dimension.width = 90
        ws.column_dimensions['B'] = column_dimension

        column_dimension = ColumnDimension(ws, 'C')
        column_dimension.width = 20
        ws.column_dimensions['C'] = column_dimension

        column_dimension = ColumnDimension(ws, 'D')
        column_dimension.width = 18
        ws.column_dimensions['D'] = column_dimension

        # 自动换行和自适应行高，从第二行开始
        for row in ws.iter_rows(min_row=2):  # 从第二行开始
            for cell in row:
                cell.alignment = Alignment(wrapText=True)  # 启用自动换行

        # 获取当前日期和时间
        current_datetime = datetime.now().strftime('%Y%m%d%H%M%S')
        
        # 生成输出文件名
        output_filename = f'练习题收集_{current_datetime}.xlsx'
        
        # 保存Excel文件
        wb.save(output_filename)
        print(f'数据已写入{output_filename}文件')

        return True, output_filename
        
    except ValueError:
        print('无法解析JSON响应')
        return False, ""
else:
    print('请求失败，状态码:', response.status_code)
    return False, ""



