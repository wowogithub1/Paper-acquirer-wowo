import tkinter as tk
from tkinter import filedialog 
import shared_data
import os
from datetime import datetime

def run_gui():
 current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
 folder_name = f"task_{current_time}"

 
 window = tk.Tk()
 window.title('论文信息获取小工具')
 window.geometry("500x250")

 l = tk.Label(window,text='点击下面按钮开始')
 l.pack()

 selected_file_path = ""# 定义一个全局变量来存储所选文件路径
  # 新增参数变量和勾选框
 param_var = tk.BooleanVar()  # 创建BooleanVar对象
 param_var2 = tk.BooleanVar()  # 创建BooleanVar对象

 def open_file():
    global selected_file_path
    selected_file_path = filedialog.askopenfilename(
        title="选择 CSV 文件",
        filetypes=[("CSV Files", "*.csv")]
        )  # 打开文件选择对话框
    if selected_file_path:  # 如果选择了文件

        # 创建任务文件夹
        os.makedirs(folder_name, exist_ok=True)  # If it already exists, it will not raise an error
        # 创建子文件夹
        subfolder1_name = os.path.join(folder_name, "target")  # 构造子文件夹路径
        os.makedirs(subfolder1_name, exist_ok=True)
        subfolder2_name = os.path.join(folder_name, "references")  # 构造子文件夹路径
        os.makedirs(subfolder2_name, exist_ok=True)
        subfolder3_name = os.path.join(folder_name, "citation")  # 构造子文件夹路径
        os.makedirs(subfolder3_name, exist_ok=True)
        subfolder4_name = os.path.join(folder_name, "coReferences")  # 构造子文件夹路径
        os.makedirs(subfolder4_name, exist_ok=True)
        subfolder5_name = os.path.join(folder_name, "coCitation")  # 构造子文件夹路径
        os.makedirs(subfolder5_name, exist_ok=True)

        #传递参数给共享数据模块
        shared_data.selected_file_path = selected_file_path  # 输出选择的文件路径，您可以在这里做进一步处理
        shared_data.folder_name = folder_name
        shared_data.folder_target_path = subfolder1_name
        shared_data.folder_reference_path = subfolder2_name
        shared_data.folder_citation_path = subfolder3_name
        shared_data.folder_coReference_path = subfolder4_name
        shared_data.folder_coCitation_path = subfolder5_name

        # 打开文件夹
        os.startfile(folder_name)  # 仅在 Windows 上有效
        # 关闭窗口
        window.destroy()  

 b = tk.Button(window, text='通过csv文件中DOI获取论文信息',command=open_file)
 b.place(x=150, y=90, width=200, height=30)# 更新按钮位置

 check_button2 = tk.Checkbutton(window, text='勾选以获取共引用、共被引元数据', variable=param_var2)
 shared_data.is_get_co = param_var2 
 check_button2.pack()

 check_button = tk.Checkbutton(window, text='勾选以获取全文', variable=param_var)
 shared_data.is_get_fulltext = param_var  
 check_button.pack()



 c = tk.Button(window, text='通过检索获取论文信息',command=lambda:print('检索功能暂未实现'))
 c.place(x=150, y=150, width=200, height=30)# 更新按钮位置



 window.mainloop()

if __name__ == "__main__":
    run_gui()
   # print(shared_data.is_get_fulltext.get())