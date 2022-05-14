import tkinter as tk
from PIL import Image, ImageTk
import sqlite3 as sql3

# 베이스: 윈도우 창 #
class DemoPro(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(MainPage)
        self.geometry("600x800+450+5")
        self.resizable(False, False)
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class PersonalCard:
    # payment information #
    card_balance = 100000  # default card balance
    rewards_point = 0
    final_cost = 0


class Sharing:
    def __init__(self):
        # menu information #
        self.menu_code = {10001: "빅맥", 10002: "맥너겟", 10003: "콜라"}
        self.select_check = {10001: 0, 10002: 0, 10003: 0}
        self.menu_quantity = {10001: 0, 10002: 0, 10003: 0}
        self.menu_price = {10001: 8000, 10002: 3000, 10003: 1500}

        # used DB list #
        self.order_DB = sql3.connect("C:/Users/SEO/Downloads/portable/sqlite-tools-win32-x86-3380500/orderDB")
        self.cur = self.order_DB.cursor()

        # used image list #
        self.mv_pay_btn_img = Image.open('pic/button/mv_pay_btn.png')
        self.mv_pay_btn_img = self.mv_pay_btn_img.resize((100, 100))
        self.mv_pay_btn_img = ImageTk.PhotoImage(self.mv_pay_btn_img)
        self.cc_btn_img = Image.open('pic/button/cc_btn.png')
        self.cc_btn_img = self.cc_btn_img.resize((200, 133))
        self.cc_btn_img = ImageTk.PhotoImage(self.cc_btn_img)


class MainPage(Sharing, tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        Sharing.__init__(self)

        # used variable list #
        self.ent_open_check = 0

        # used frame list #
        self.logo_frm = tk.Frame(self, width=600, height=100, relief="solid", bd=2)
        self.logo_frm.grid(row=0, column=0, sticky="nswe")
        self.menu_btn_frm = tk.Frame(self, width=600, height=500, relief="solid", bd=2)
        self.menu_btn_frm.grid(row=1, column=0, sticky="nswe")
        '''
        self.qu_frm = tk.Frame(self, width=600, height=50, relief="solid", bd=2)
        self.qu_frm.grid(row=2, column=0, sticky="nswe")
        '''
        self.cart_frm = tk.Frame(self, width=600, height=100, relief="solid", bd=2)
        self.cart_frm.grid(row=3, column=0, sticky="nswe")
        self.entry_frm = tk.Frame(self, width=600, height=50, relief="solid", bd=2)
        self.entry_frm.grid(row=2, column=0, sticky="nswe")
        self.menu_frm = tk.Frame(self, width=600, height=50, relief="solid", bd=2)
        self.menu_frm.grid(row=4, column=0, sticky="nswe")

        # in menu frame #
        tk.Label(self.menu_frm, text="카드 잔액: %d 원" % PersonalCard.card_balance).pack()

        # in menu button frame #
        # if press menu button, entry and OK button will appear
        tk.Button(self.menu_btn_frm, text="빅맥\n8000원",
                  command=lambda: self.open_entry(10001)).place(x=0, y=0, width=200, height=133)
        tk.Button(self.menu_btn_frm, text="맥너겟\n3000원", width=200, height=100,
                  command=lambda: self.open_entry(10002)).place(x=200, y=0, width=200, height=133)
        tk.Button(self.menu_btn_frm, text="콜라\n1500원", width=200, height=100,
                  command=lambda: self.open_entry(10003)).place(x=400, y=0, width=200, height=133)

        # in entry frame #
        self.ent = tk.Entry(self.entry_frm, width=5)
        self.ent.pack(anchor="center")
        self.ent.pack_forget()
        # if press OK button, the chosen menu and its quantity will be added to cart
        self.ok_btn = tk.Button(self.entry_frm, text="OK",
                                command=lambda: self.enter_cart(self.ent.get()))
        self.ok_btn.pack(anchor="center")
        self.ok_btn.pack_forget()

        # in cart frame #
        self.cart_lbox = tk.Listbox(self.cart_frm, width=60, height=5)
        self.cart_lbox.place(x=0, y=0, width=350, height=100)
        tk.Label(self.cart_frm, text="총 결제금액").place(x=350, y=0)
        self.ttlprice_lb = tk.Label(self.cart_frm, text="￦ %d" % 0)
        self.ttlprice_lb.place(x=350, y=30)
        self.calculate_ttlprice()
        # if press "초기화" button, the cart will become empty and the orderlist will be clear
        tk.Button(self.cart_frm, text="전체취소", command=self.reset_cart).place(x=350, y=70, width=150, height=30)
        # if press "결제하기" button, the cart will become empty and go to payment select page
        tk.Button(self.cart_frm, image=self.mv_pay_btn_img,
                  command=lambda: [self.enter_orderDB(), self.reset_cart(),
                                   master.switch_frame(OrderCheckPage)]).place(x=500, y=0, width=100, height=100)

    def calculate_ttlprice(self):
        ttlprice = 0
        for code in self.menu_code.keys():
            if self.menu_quantity[code] != 0:
                ttlprice = ttlprice + self.menu_price[code] * self.menu_quantity[code]
        self.ttlprice_lb = tk.Label(self.cart_frm, text="￦ %d" % ttlprice)
        self.ttlprice_lb.place(x=350, y=30)

    def open_entry(self, code):
        # if entry is already opened
        if self.ent_open_check == 1:
            self.ent_open_check = 0
            self.select_check[code] = 0
            self.ent.delete(0, "end")
            self.ent.pack_forget()
            self.ok_btn.pack_forget()
            return
        # open entry
        self.ent_open_check = 1
        self.select_check[code] = 1
        self.ent.pack(anchor="center")
        self.ok_btn.pack(anchor="center")

    def enter_cart(self, quantity):
        for code in self.select_check.keys():
            if self.select_check[code] == 1:
                self.menu_quantity[code] = self.menu_quantity[code] + int(quantity)
                self.cart_lbox.insert(0, "메뉴: %s 수량: %d\n" % (self.menu_code[code], self.menu_quantity[code]))
                self.select_check[code] = 0

    def enter_orderDB(self):
        for code in self.menu_code.keys():
            if self.menu_quantity[code] != 0:
                mncode = code
                mnname = self.menu_code[code]
                qntity = self.menu_quantity[code]
                ttlprice = self.menu_price[code] * qntity
                sql = "INSERT INTO orderTable VALUES(?, ?, ?, ?)"
                self.cur.execute(sql, (mncode, mnname, qntity, ttlprice))
                self.order_DB.commit()

    def reset_cart(self):
        self.cart_lbox.delete(0, "end")
        for code in self.menu_quantity.keys():
            self.menu_quantity[code] = 0


class OrderCheckPage(Sharing, tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        Sharing.__init__(self)

        # used frame list #
        self.orderlist_frm = tk.Frame(self, width=600, height=637, relief="solid", bd=2)
        self.orderlist_frm.pack(fill="both", expand=True)
        self.orderlist_frm.propagate(False)
        self.announce_frm = tk.Frame(self, width=600, height=30, relief="solid", bd=2)
        self.announce_frm.pack(fill="both", expand=True)
        self.announce_frm.propagate(False)
        self.mv_btn_frm = tk.Frame(self, width=600, height=133, relief="solid", bd=2)
        self.mv_btn_frm.pack(fill="both", expand=True)
        self.mv_btn_frm.propagate(False)

        # in orderlist frame #
        self.show_orderlist()

        # in announce frame #
        tk.Label(self.announce_frm, text="결제하시겠습니까?").pack()

        # in move button frame #
        tk.Button(self.mv_btn_frm, image=self.mv_pay_btn_img,
                  command=lambda: master.switch_frame(PaymentPage)).place(x=300, y=0, width=200, height=133)
        tk.Button(self.mv_btn_frm, image=self.cc_btn_img,
                  command=lambda: master.switch_frame(MainPage)).place(x=100, y=0, width=200, height=133)

    def show_orderlist(self):
        tk.Label(self.orderlist_frm, text="주문 목록").pack()
        self.cur.execute("SELECT menuName, quantity FROM orderTable")
        rows = self.cur.fetchall()
        for menu in rows:
            tk.Label(self.orderlist_frm, text=menu).pack()


class PaymentPage(Sharing, tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        Sharing.__init__(self)

        # used frame list #
        self.chs_discnt_frm = tk.Frame(self, width=600, height=667, relief="solid", bd=1)
        self.chs_discnt_frm.pack(fill="both", expand=True)
        self.chs_discnt_frm.propagate(False)
        self.etc_frm = tk.Frame(self, width=600, height=133, relief="solid", bd=1)
        self.etc_frm.pack(fill="both", expand=True)
        self.etc_frm.propagate(False)

        # in choose discount method frame #
        self.opt1 = tk.Button(self.chs_discnt_frm, text="적립금", command=lambda: master.switch_frame(DisCountPage))
        self.opt1.place(x=0, y=0, width=300, height=333)
        self.opt2 = tk.Button(self.chs_discnt_frm, text="쿠폰", command=lambda: master.switch_frame(DisCountPage))
        self.opt2.place(x=300, y=0, width=300, height=333)
        self.opt3 = tk.Button(self.chs_discnt_frm, text="멤버십 포인트",
                              command=lambda: master.switch_frame(DisCountPage))
        self.opt3.place(x=0, y=333, width=300, height=333)
        self.opt4 = tk.Button(self.chs_discnt_frm, text="없음(그냥 결제)", width=27, height=4,
                              command=lambda: [self.pay_sequence(), master.switch_frame(ReceiptPage)])
        self.opt4.place(x=300, y=333, width=300, height=333)

        # in etc frame #
        tk.Button(self.etc_frm, text="첫 화면으로\n(결제 취소)",
                  command=lambda: [master.switch_frame(MainPage)]).place(x=200, y=666, width=200, height=133)

    def pay_sequence(self):
        self.cur.execute("SELECT finalCost FROM orderTable")
        cost_list = self.cur.fetchall()
        for cost_data in cost_list:
            PersonalCard.final_cost = PersonalCard.final_cost + cost_data[0]
        PersonalCard.card_balance = PersonalCard.card_balance - PersonalCard.final_cost
        PersonalCard.rewards_point = PersonalCard.final_cost * 0.01


class DisCountPage(Sharing, tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        Sharing.__init__(self)

        # used frame list #
        self.announce_frm = tk.Frame(self, width=600, height=667, relief="solid", bd=1)
        self.announce_frm.pack(fill="both", expand=True)
        self.announce_frm.propagate(False)
        self.btn_frm = tk.Frame(self, width=600, height=133, relief="solid", bd=1)
        self.btn_frm.pack(fill="both", expand=True)
        self.btn_frm.propagate(False)

        # in announce frame #
        self.announce1 = tk.Label(self.announce_frm, text="적립금을 사용해 할인하시겠습니까?")
        self.announce1.place(x=0, y=0, width=600, height=30)
        self.announce2 = tk.Label(self.announce_frm, text="적립금 %d point" % PersonalCard.rewards_point)
        self.announce2.place(x=0, y=30, width=600, height=30)
        self.announce3 = tk.Label(self.announce_frm, text="할인 후 결제 금액 %d" % 0)
        self.announce3.place(x=0, y=60, width=600, height=30)

        # in button frame #
        self.button1 = tk.Button(self.btn_frm, text="사용하기",
                                 command=lambda: [self.pay_sequence(), master.switch_frame(ReceiptPage)])
        self.button1.place(x=300, y=0, width=200, height=133)
        self.button2 = tk.Button(self.btn_frm, text="취소", command=lambda: master.switch_frame(PaymentPage))
        self.button2.place(x=100, y=0, width=200, height=133)

    def pay_sequence(self):
        self.cur.execute("SELECT finalCost FROM orderTable")
        cost_list = self.cur.fetchall()
        for cost_data in cost_list:
            PersonalCard.final_cost = PersonalCard.final_cost + cost_data[0]
        if PersonalCard.rewards_point < 5000: # if rewards point is over 5000, you can use it for discount
            tk.Label(self.announce_frm,
                     text="적립금이 5000점 미만이므로 사용할 수 없습니다.").place(x=0, y=90, width=600, height=30)
            PersonalCard.card_balance = PersonalCard.card_balance - PersonalCard.final_cost
            PersonalCard.rewards_point = PersonalCard.final_cost * 0.01
        else:
            PersonalCard.final_cost = PersonalCard.final_cost - PersonalCard.rewards_point
            PersonalCard.card_balance = PersonalCard.card_balance - PersonalCard.final_cost
            PersonalCard.rewards_point = 0
            PersonalCard.rewards_point = PersonalCard.final_cost * 0.01


class DisCountRewards(DisCountPage):
    pass


class DisCountCoupon(DisCountPage):
    def __init__(self, master):
        DisCountPage.__init__(self, master)

        # in announce frame #
        self.announce1 = tk.Label(self.announce_frm, text="사용할 쿠폰 선택")
        self.announce1.pack()

        # in button frame #     # 보유 여부도 외부 데이터베이스 연결해서 하는 편이 좋을까...
        self.button1 = tk.Button(self.btn_frm, text="10%% 할인 쿠폰  보유: %d" % 0)
        self.button2 = tk.Button(self.btn_frm, text="30%% 할인 쿠폰  보유: %d" % 0)
        self.button3 = tk.Button(self.btn_frm, text="50%% 할인 쿠폰  보유: %d" % 0)


class DisCountMembership(DisCountPage):
    def __init__(self, master):
        DisCountPage.__init__(self, master)
        self.announce1 = tk.Label(self.announce_frm, text="사용할 멤버십 선택")


class ReceiptPage(Sharing, tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        Sharing.__init__(self)

        # used frame list #
        self.summary_frm = tk.Frame(self, width=600, height=300, relief="solid", bd=2)
        self.summary_frm.pack(fill="both", expand=True)
        self.summary_frm.propagate(False)
        self.etc_frm = tk.Frame(self, width=600, height=100, relief="solid", bd=2)
        self.etc_frm.pack(fill="both", expand=True)
        self.etc_frm.propagate(False)

        # in summary frame #
        self.announce = tk.Label(self.summary_frm, text="결제가 완료되었습니다.\n")
        self.announce.pack()
        self.show_result()

        # in etc frame #
        self.mv_main_btn = tk.Button(self.etc_frm, text="첫 화면으로",
                                     command=lambda: [master.switch_frame(MainPage)])
        self.mv_main_btn.pack(side="left")
        self.show_rcpt_btn = tk.Button(self.etc_frm, text="영수증 보기",
                                       command=self.new_tk_receipt)
        self.show_rcpt_btn.pack(side="left")

    def show_result(self):
        tk.Label(self.summary_frm, text="주문 항목").pack()
        tk.Label(self.summary_frm, text="메뉴     수량     가격").pack()
        tk.Label(self.summary_frm, text="=========================").pack()
        self.cur.execute("SELECT menuName, quantity, finalCost FROM orderTable")
        while True:
            row = self.cur.fetchone()
            if row is None:
                break
            tk.Label(self.summary_frm, text="%s     %d     %d" % (row[0], row[1], row[2])).pack()
        tk.Label(self.summary_frm, text="=========================").pack()
        tk.Label(self.summary_frm, text="총액     %d 원" % PersonalCard.final_cost).pack()

        # clear DB #
        self.cur.execute("DELETE FROM orderTable")
        self.order_DB.commit()    ### 이거 하면 database locked 뜨면서 제대로 안됨
        self.order_DB.close()
        PersonalCard.final_cost = 0

    def new_tk_receipt(self):
        receipt_tk = tk.Toplevel(app)
        tk.Label(receipt_tk, text="영수증").pack()
        tk.Label(receipt_tk, text="카드 잔액        %d 원" % PersonalCard.card_balance).pack()
        tk.Label(receipt_tk, text="결제 금액        %d 원" % PersonalCard.final_cost).pack()
        tk.Label(receipt_tk, text="적립금      %d point" % PersonalCard.rewards_point).pack()


app = DemoPro()
app.mainloop()