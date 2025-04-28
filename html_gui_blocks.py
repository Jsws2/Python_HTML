import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import webbrowser

#HTML 코드 저장 리스트
html_list = []

#대분류 - 세부항목 매핑
tags = {
    "텍스트": ["h1", "h2", "h3", "h4", "h5", "p", "pre"],
    "링크": ["a"],
    "이미지": ["img"],
    "구조": ["div", "ul", "ol", "li"],
    "특수문자": ["&lt;", "&gt;", "&amp;", "&quot;"]
}

#세부항목 드롭다운 업데이트 함수
def update_suboptions(*args):
    selected_main = main_var.get()
    sub_options = tags.get(selected_main, [])
    sub_var.set("")
    sub_menu['menu'].delete(0, 'end')
    for option in sub_options:
        sub_menu['menu'].add_command(label=option, command=tk._setit(sub_var, option))

#태그 추가 함수
def add_tag():
    selected = sub_var.get()

    if not selected:
        messagebox.showwarning("경고", "세부 항목을 선택하세요")
        return
    
    # 특수문자 처리
    if selected.startswith("&"):
        html = selected
        html_list.append(html)
    
    elif selected in ["p", "pre"]:
        content = simpledialog.askstring("문단 입력", "문단 내용을 입력하세요:")
        if content:
            html = f"<{selected}>{content}</{selected}>"
            html_list.append(html)

    elif selected == "a":
        href = simpledialog.askstring("링크 주소 입력", "링크 주소를 입력하세요:")
        text = simpledialog.askstring("링크 텍스트 입력", "링크에 표시할 텍스트를 입력하세요")
        if href and text:
            html = f'<a href="{href}">{text}</a>'
            html_list.append(html)

    elif selected == "img":
        src = simpledialog.askstring("이미지 주소 입력", "이미지 URL을 입력하세요:")
        alt = simpledialog.askstring("대체 텍스트 입력", "이미지 설명을 입력하세요:")
        if src:
            html = f'<img src="{src}" alt="{alt if alt else''}">'
            html_list.append(html)
    
    elif selected.startswith("h"):
        content = simpledialog.askstring("제목 입력", f"{selected} 태그 안에 들어갈 제목을 입력하세요")
        if content:
            html = f"<{selected}>{content}</{selected}>"
            html_list.append(html)

    elif selected in ["div", "li"]:
        content = simpledialog.askstring("내용 입력", f"{selected} 태그 안에 들어갈 내용을 입력하세요 (li 항목은 한 줄 입력):")
        if content:
            html = f"<{selected}>{content}</{selected}>"
        else:
            html = f"<{selected}></{selected}>"
        html_list.append(html)

    elif selected in ["ul", "ol"]:
        try:
            count = simpledialog.askinteger("항목 개수 입력", "몇 개의 항목을 추가할까요?")
            if count and count > 0:
                items = []
                for i in range(1, count + 1):
                    item = simpledialog.askstring(f"항목{i} 입력", f"{i}번째 항목 내용을 입력하세요:")
                    if item:
                        items.append(f"<li>{item}</li>")
                html = f"<{selected}>\n" + "\n".join(items) + f"\n</{selected}>"
                html_list.append(html)
        except Exception as e:
            messagebox.showerror("오류", str(e))
    update_preview()

#미리보기 업데이트 함수
def update_preview():
    preview_box.delete("1.0", tk.END)
    for line in html_list:
        preview_box.insert(tk.END, line + "\n")
    live_preview()

# 파일 저장 함수
def save_to_file():
    try:
        filename = simpledialog.askstring("파일명 입력", "저장할 파일 이름을 입력하세요 (/html은 자동 추가)")
        if not filename:
            return
        
        if not filename.endswith(".html"):
            filename += ".html"

        with open("output.html", "w", encoding="utf-8") as f:
            f.write("<!DOCTYPE html>\n")
            f.write("<html lang=\"ko\">\n")
            f.write("<head>\n")
            f.write("   <meta charset=\"UTF-8\">\n")
            f.write("   <title>HTML 블록 코딩 결과</title>\n")
            f.write("</head>\n")
            f.write("<body>\n")

            for line in html_list:
                f.write(line + "\n")
            f.write("</body>\n")
            f.write("</html>\n")
            
        messagebox.showinfo("저장 완료", "output.html 파일로 저장되었습니다!")
        os.system("open output.html")  # macOS 
    except Exception as e:
        messagebox.showerror("에러 발생", str(e))

# 함수 지우기
def delete_block():
    try:
        index = simpledialog.askinteger("블록 삭제", "삭제할 블록 번호를 입력하세요 (1부터 시작합니다)")
        if index is None:
            return
        if 1 <= index <= len(html_list):
            html_list.pop(index - 1)
            update_preview()
        else:
            messagebox.showwarning("오류", "유효하지 않은 번호입니다.")
    except Exception as e:
        messagebox.showerror("오류", str(e))

# 실시간 코드(수정 중)
def live_preview():
    try:
        with open("temp_preview.html", "w", encoding="utf-8") as f:
            f.write("<!DOCTYPE html>\n")
            f.write("<html lang=\"ko\">\n")
            f.write("<head>\n")
            f.write("   <meta charset=\"UTF-8\">\n")
            f.write("   <title>HTML 미리보기</title>\n")
            f.write("</head>\n")
            f.write("<body>\n")

            for line in html_list:
                f.write(line + "\n")
            f.write("</body>\n")
            f.write("</html>\n")
        path = os.path.abspath("temp_preview.html")
        webbrowser.open(f"file://{path}", new = 0)
    except Exception as e:
        messagebox.showerror("오류", str(e))


#전체 리셋 함수
def reset_all():
    html_list.clear()
    update_preview()
    main_var.set("")
    sub_var.set("")

#GUI 세팅
root = tk.Tk()
root.title("HTML 블록 코딩 툴")

#드롭다운

#분류
main_var = tk.StringVar()
main_var.trace("w", update_suboptions)
main_menu = tk.OptionMenu(root, main_var, *tags.keys())
main_menu.config(width=20)
main_menu.pack(pady=10)

#세부 항목
sub_var = tk.StringVar()
sub_menu = tk.OptionMenu(root, sub_var, "")
sub_menu.config(width=20)
sub_menu.pack(pady=5)

#추가 버튼
add_btn = tk.Button(root, text="태그 추가", command=add_tag)
add_btn.pack(pady=5)
delete_btn = tk.Button(root, text="블록 삭제", command=delete_block)
delete_btn.pack(pady=5)

#미리보기
preview_label = tk.Label(root, text="현재 생성된 HTML:")
preview_label.pack()
preview_box = tk.Text(root, height=15, width=60)
preview_box.pack()

save_btn = tk.Button(root, text="파일로 저장 (output.html)", command=save_to_file)
save_btn.pack(pady=5)

reset_btn = tk.Button(root, text="새로 만들기", command=reset_all)
reset_btn.pack(pady=5)

root.mainloop()
