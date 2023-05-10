import tkinter as tk
from tkcalendar import DateEntry
from cvd_model import *


class CVD_GUI:
    def __init__(self):

        # Create the main window.
        self.main_window = tk.Tk()
        self.main_window.title("Second-hand Mercedes Benz Seller Type Predictor")

        self.zero_frame = tk.Frame()
        self.one_frame = tk.Frame()
        self.two_frame = tk.Frame()
        self.three_frame = tk.Frame()
        self.four_frame = tk.Frame()
        self.five_frame = tk.Frame()
        self.six_frame = tk.Frame()
        self.seven_frame = tk.Frame()
        self.eight_frame = tk.Frame()
        self.nine_frame = tk.Frame()
        self.ten_frame = tk.Frame()

        self.title_label = tk.Label(self.zero_frame, text='Second-hand Mercedes Benz Seller Type Predictor',fg="Blue", font=("Helvetica", 18))
        self.title_label.pack()

        self.model_label = tk.Label(self.one_frame, text='Model:')
        self.model_entry = tk.Entry(self.one_frame, bg="white", fg="black")
        self.model_label.pack(side='left')
        self.model_entry.pack(side='left')

        self.first_registration_label = tk.Label(self.two_frame, text='First Registration:')
        self.first_registration_entry = DateEntry(self.two_frame, bg="white", fg="black", width=10)
        self.first_registration_label.pack(side='left')
        self.first_registration_entry.pack(side='left')

        self.fuel_label = tk.Label(self.three_frame, text='Fuel:')
        self.click_fuel_var = tk.StringVar()
        self.click_fuel_var.set("Diesel")
        self.fuel_inp = tk.OptionMenu(self.three_frame,self.click_fuel_var, "Diesel", "Gpl", "Electric")
        self.fuel_label.pack(side='left')
        self.fuel_inp.pack(side='left')

        self.mileage_label = tk.Label(self.four_frame, text='mileage:')
        self.mileage_entry = tk.Entry(self.four_frame, bg="white", fg="black")
        self.mileage_label.pack(side='left')
        self.mileage_entry.pack(side='left')

        self.swift_label = tk.Label(self.five_frame, text='Swift:')
        self.click_swift_var = tk.StringVar()
        self.click_swift_var.set("Automatic")
        self.swift_inp = tk.OptionMenu(self.five_frame, self.click_swift_var, "Automatic", "Manual")
        self.swift_label.pack(side='left')
        self.swift_inp.pack(side='left')

        self.price_label = tk.Label(self.six_frame, text='Price:')
        self.price_entry = tk.Entry(self.six_frame, bg="white", fg="black")
        self.price_label.pack(side='left')
        self.price_entry.pack(side='left')

        self.hp_label = tk.Label(self.seven_frame, text='Horsepower:')
        self.hp_entry = tk.Entry(self.seven_frame, bg="white", fg="black")
        self.hp_label.pack(side='left')
        self.hp_entry.pack(side='left')

        self.btn_predict = tk.Button(self.eight_frame, text='Predict Seller Type', command=self.predict_mb)
        self.btn_quit = tk.Button(self.eight_frame, text='Quit', command=self.main_window.destroy)
        self.btn_predict.pack(side='left')
        self.btn_quit.pack(side='left')

        self.mb_predict_ta = tk.Text(self.nine_frame,height = 5, width = 80,bg= 'light blue')
        self.mb_predict_ta.pack(side='left')

        self.zero_frame.pack()
        self.one_frame.pack()
        self.two_frame.pack()
        self.three_frame.pack()
        self.four_frame.pack()
        self.five_frame.pack()
        self.six_frame.pack()
        self.seven_frame.pack()
        self.eight_frame.pack()
        self.nine_frame.pack()


        tk.mainloop()

    def predict_mb(self):
        result_string = ""
        self.mb_predict_ta.delete(0.0, tk.END)

        car_model = float(self.model_entry.get())

        date_value = self.first_registration_entry.get_date()
        timestamp_value = pd.Timestamp(date_value)
        car_first_registration = timestamp_value.value // 10 ** 9

        car_fuel = self.click_fuel_var.get()
        if(car_fuel == "Diesel"):
            car_fuel = 0
        elif(car_fuel == "Gpl"):
            car_fuel = 1
        else:
            car_fuel = 2

        car_mileage = int(self.mileage_entry.get())

        car_swift = self.click_swift_var.get()
        if (car_swift == "Automatic"):
            car_swift = 0
        elif (car_swift == "Manual"):
            car_swift = 1

        car_price = int(self.price_entry.get())
        car_hp = int(self.hp_entry.get())

        result_string += "===Result=== \n"
        car_info = (car_model,car_first_registration,car_fuel,car_mileage,car_swift,car_price,car_hp)

        mb_prediction =  best_model.predict([car_info])
        disp_string = (str(model_accuracy))

        if(mb_prediction == [0]):
            result_string += ("Seller type:Dealer is probabilistically more likely.\nThis prediction has an accuracy of:"+disp_string)
        else:
            result_string += ("Seller type:Private is probabilistically more likely.\nThis prediction has an accuracy of:"+disp_string)
        self.mb_predict_ta.insert('1.0',result_string)



my_cvd_GUI = CVD_GUI()

