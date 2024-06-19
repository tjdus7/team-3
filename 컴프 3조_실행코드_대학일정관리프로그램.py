import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from ttkthemes import ThemedStyle 
import pickle

class UniversityScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("대학 일정 관리 프로그램")  # 윈도우 창 제목 설정
        
        self.schedule = {'시험': [], '과제': []}  # 일정을 저장할 딕셔너리
        
        self.load_schedule()  # 프로그램이 시작될 때 저장된 스케줄을 불러옴
        
        self.create_widgets()  # GUI 위젯 생성
        self.display_schedule()  # 저장된 스케줄을 표시
    
    def create_widgets(self):
        # 제목 레이블 생성
        self.title_label = ttk.Label(self.root, text="대학일정프로그램", font=('Arial', 20, 'bold'))
        self.title_label.pack(side='top', pady=10)
        
        # 트리뷰 생성 (일정을 표시하기 위한 테이블)
        self.tree = ttk.Treeview(self.root, columns=('Type', 'Date', 'Lecture', 'Professor', 'Memo', 'Status'), show='headings')
        self.tree.heading('Type', text='유형')
        self.tree.heading('Date', text='날짜')
        self.tree.heading('Lecture', text='강의명')
        self.tree.heading('Professor', text='교수님')
        self.tree.heading('Memo', text='메모')
        self.tree.heading('Status', text='진행 상황')
        self.tree.pack(side='left', fill='both', expand=True)
        self.tree.bind("<ButtonRelease-1>", self.select_schedule)  # 트리뷰 클릭 시 이벤트 바인딩
        
        # 날짜 선택 라벨 및 캘린더 생성
        self.calendar_label = ttk.Label(self.root, text='날짜 선택:')
        self.calendar_label.pack(side='top', padx=10, pady=5)
        self.calendar = Calendar(self.root, selectmode='day', date_pattern='yyyy-mm-dd')
        self.calendar.pack(side='top', padx=10, pady=5)
        self.calendar.config(font=('Arial', 12))  # 캘린더 폰트 크기 조절
        
        # 강의명, 교수명, 메모, 진행 상황 입력 위젯 생성
        self.lecture_label = ttk.Label(self.root, text='강의명:')
        self.lecture_label.pack(side='top', padx=10, pady=5)
        self.lecture_entry = ttk.Entry(self.root)
        self.lecture_entry.pack(side='top', padx=10, pady=5)
        
        self.professor_label = ttk.Label(self.root, text='교수님:')
        self.professor_label.pack(side='top', padx=10, pady=5)
        self.professor_entry = ttk.Entry(self.root)
        self.professor_entry.pack(side='top', padx=10, pady=5)
        
        self.memo_label = ttk.Label(self.root, text='메모:')
        self.memo_label.pack(side='top', padx=10, pady=5)
        self.memo_entry = ttk.Entry(self.root)
        self.memo_entry.pack(side='top', padx=10, pady=5)
        
        self.status_label = ttk.Label(self.root, text='진행 상황:')
        self.status_label.pack(side='top', padx=10, pady=5)
        
        # 진행 상황 라디오 버튼 생성
        self.status_var = tk.StringVar(value='진행중')
        self.status_radio_inprogress = ttk.Radiobutton(self.root, text='진행중', variable=self.status_var, value='진행중')
        self.status_radio_inprogress.pack(side='top', padx=10, pady=5)
        self.status_radio_completed = ttk.Radiobutton(self.root, text='완료', variable=self.status_var, value='완료')
        self.status_radio_completed.pack(side='top', padx=10, pady=5)
        self.status_radio_incomplete = ttk.Radiobutton(self.root, text='미완료', variable=self.status_var, value='미완료')
        self.status_radio_incomplete.pack(side='top', padx=10, pady=5)
        
        # 일정 유형 라디오 버튼 생성
        self.type_var = tk.StringVar(value='시험')
        self.type_radio_exam = ttk.Radiobutton(self.root, text='시험', variable=self.type_var, value='시험')
        self.type_radio_exam.pack(side='top', padx=10, pady=5)
        self.type_radio_assignment = ttk.Radiobutton(self.root, text='과제', variable=self.type_var, value='과제')
        self.type_radio_assignment.pack(side='top', padx=10, pady=5)
        
        # 일정 추가, 삭제, 저장 버튼 생성
        button_frame = ttk.Frame(self.root)
        button_frame.pack(side='top', padx=10, pady=5)
        
        self.add_button = ttk.Button(button_frame, text='일정 추가', command=self.add_schedule)
        self.add_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.remove_button = ttk.Button(button_frame, text='일정 삭제', command=self.remove_schedule)
        self.remove_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.save_button = ttk.Button(self.root, text='저장', command=self.save_schedule)
        self.save_button.pack(side='bottom', padx=10, pady=5)
        
        # 다른 테마 적용
        style = ThemedStyle(self.root)
        style.set_theme("breeze") # breeze 테마 적용
    
    def select_schedule(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = selected_item[0]
            self.selected_schedule_index = self.tree.index(item)
            schedule_type = self.tree.item(item)['values'][0]
            schedule = self.schedule[schedule_type][self.selected_schedule_index]
            self.lecture_entry.delete(0, 'end')
            self.lecture_entry.insert(0, schedule.get('강의명', ''))
            self.professor_entry.delete(0, 'end')
            self.professor_entry.insert(0, schedule.get('교수님', ''))
            self.memo_entry.delete(0, 'end')
            self.memo_entry.insert(0, schedule.get('메모', ''))
            self.status_var.set(schedule.get('진행상황', ''))
    
    def display_schedule(self):
        for schedule_type, schedules in self.schedule.items():
            for schedule in schedules:
                self.tree.insert('', 'end', values=(schedule_type, schedule['날짜'], schedule.get('강의명', ''), 
                                                    schedule.get('교수님', ''), schedule.get('메모', ''), schedule.get('진행상황', '')))
    
    def add_schedule(self):
        date = self.calendar.get_date()
        lecture = self.lecture_entry.get()
        professor = self.professor_entry.get()
        memo = self.memo_entry.get()
        status = self.status_var.get()
        schedule_type = self.type_var.get()
        
        if date and professor and memo and status:
            self.schedule[schedule_type].append({'날짜': date, '강의명': lecture, '교수님': professor, '메모': memo, '진행상황': status})
            self.tree.insert('', 'end', values=(schedule_type, date, lecture, professor, memo, status))
            self.clear_entries()
        else:
            messagebox.showwarning("경고", "모든 필드를 입력하세요.")
    
    def remove_schedule(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = selected_item[0]
            self.tree.delete(item)
            schedule_type = self.tree.item(item)['values'][0]
            index = self.tree.index(item)
            del self.schedule[schedule_type][index]
    
    def clear_entries(self):
        self.calendar.set_date('')
        self.lecture_entry.delete(0, 'end')
        self.professor_entry.delete(0, 'end')
        self.memo_entry.delete(0, 'end')
    
    def save_schedule(self):
        with open('schedule.pkl', 'wb') as f:
            pickle.dump(self.schedule, f)
    
    def load_schedule(self):
        try:
            with open('schedule.pkl', 'rb') as f:
                self.schedule = pickle.load(f)
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = UniversityScheduler(root)
    root.mainloop()