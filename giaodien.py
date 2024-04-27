from tkinter import *
from tkinter.ttk import Combobox, Treeview
from datetime import datetime
import flappyBird as flb
import subprocess

def calculate_age(birth_year):
    current_year = datetime.now().year
    return current_year - birth_year

def send():
    global next_stt

    hoten_value = entry2.get()
    gioitinh_value = gender_var.get()
    ngaysinh_value = f"{day_var.get()}/{month_var.get()}/{year_var.get()}"

    try:
        ngaysinh_value = datetime.strptime(ngaysinh_value, '%d/%m/%Y')
    except ValueError:
        ngaysinh_value = datetime.now()

    tuoi_value = calculate_age(ngaysinh_value.year)

    saved_data.append({'STT': next_stt, 'Họ tên': hoten_value, 'Giới tính': gioitinh_value, 'Ngày sinh': ngaysinh_value.strftime('%d/%m/%Y'), 'Tuổi': tuoi_value})

    tree.insert('', 'end', values=(next_stt, hoten_value, gioitinh_value, ngaysinh_value.strftime('%d/%m/%Y'), tuoi_value))

    subprocess.Popen(['python', 'flappyBird.py'])

    next_stt += 1

def tree_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda: tree_sort_column(tv, col, not reverse))

a = Tk()
a.title('FlappyBird')
a.geometry('800x400')  # Tăng kích thước cửa sổ
a['bg'] = '#87CEEB'  # Đặt màu nền cho cửa sổ (màu xanh dương nhẹ)
a.attributes('-topmost', True)

saved_data = []
next_stt = 1

# Tạo và định dạng các label và entry
label_style = ('Times New Roman', 14, 'bold')
entry_style = ('Times New Roman', 14)
button_style = ('Times New Roman', 14, 'bold')

name2 = Label(a, font=label_style, text=' Họ tên:', bg='#87CEEB', fg='#003366')  
name2.place(x=10, y=30)

entry2 = Entry(a, width=40, font=entry_style)
entry2.place(x=150, y=30)

name3 = Label(a, font=label_style, text=' Giới tính:', bg='#87CEEB', fg='#003366')
name3.place(x=10, y=70)

gender_options = ['Nam', 'Nữ', 'Khác']
gender_var = StringVar(value=gender_options[0])
gender_combo = Combobox(a, values=gender_options, textvariable=gender_var, state='readonly', width=15, font=entry_style)
gender_combo.place(x=150, y=70)

name4 = Label(a, font=label_style, text=' Ngày sinh:', bg='#87CEEB', fg='#003366')
name4.place(x=10, y=110)

day_options = [str(i) for i in range(1, 32)]
day_var = StringVar(value=day_options[0])
day_combo = Combobox(a, values=day_options, textvariable=day_var, state='readonly', width=5, font=entry_style)
day_combo.place(x=150, y=110)

month_options = [str(i) for i in range(1, 13)]
month_var = StringVar(value=month_options[0])
month_combo = Combobox(a, values=month_options, textvariable=month_var, state='readonly', width=5, font=entry_style)
month_combo.place(x=220, y=110)

year_options = [str(i) for i in range(1900, datetime.now().year + 1)]
year_var = StringVar(value=year_options[0])
year_combo = Combobox(a, values=year_options, textvariable=year_var, state='readonly', width=7, font=entry_style)
year_combo.place(x=300, y=110)

# Tạo và định dạng Treeview
tree = Treeview(a, columns=('STT', 'Họ tên', 'Giới tính', 'Ngày sinh', 'Tuổi'), show='headings', selectmode='browse', height=5)
tree.heading('STT', text='STT', anchor='center', command=lambda: tree_sort_column(tree, 'STT', False))
tree.heading('Họ tên', text='Họ tên', anchor='center', command=lambda: tree_sort_column(tree, 'Họ tên', False))
tree.heading('Giới tính', text='Giới tính', anchor='center', command=lambda: tree_sort_column(tree, 'Giới tính', False))
tree.heading('Ngày sinh', text='Ngày sinh', anchor='center', command=lambda: tree_sort_column(tree, 'Ngày sinh', False))
tree.heading('Tuổi', text='Tuổi', anchor='center', command=lambda: tree_sort_column(tree, 'Tuổi', False))
tree.column('STT', width=30, anchor='center')
tree.column('Họ tên', width=180, anchor='center')
tree.column('Giới tính', width=70, anchor='center')
tree.column('Ngày sinh', width=90, anchor='center')
tree.column('Tuổi', width=50, anchor='center')
tree.place(x=10, y=190, width=760, height=200)

# Tạo và định dạng nút Gửi
but = Button(a, text='Gửi', width=10, height=1, font=button_style, command=send, bg='#003366', fg='#87CEEB')  
but.place(x=550, y=50)

a.mainloop()
