'''
!!! USE THE Australian_Vehicle_Prices_GUI CSV FILE WHEN RUNNING THIS PROGRAM !!!

'''

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

class VehiclePricePredictionApp:
    def __init__(self, master):
        self.master = master
        self.master.title('Vehicle Price Prediction')
        self.data = pd.read_csv('Australian_Vehicle_Prices_GUI.csv')
        self.sliders = []

        self.data = self.data.dropna(subset=['Kilometres'], axis=0)
        self.data = self.data.dropna(subset=['Price'], axis=0)
        self.data = self.data.dropna(subset=['FuelConsumption'], axis=0)
        self.data = self.data.dropna(subset=['CylindersinEngine'], axis=0)

        self.X = self.data.drop('Price', axis=1).values
        self.y = self.data['Price'].values

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)

        self.model = XGBRegressor()
        self.model.fit(self.X_train, self.y_train)

        self.create_widgets()
    
    UorN_D = 0
    UorN_N = 0
    UorN_N = 0
    def UorN(self, type):
        global UorN_D
        global UorN_U
        global UorN_N
        if type == "DEMO":
            self.UorN_D_BTN.config(bg = "green")
            self.UorN_U_BTN.config(bg = "white")
            self.UorN_N_BTN.config(bg = "white")
            UorN_D = 1
            UorN_U = 0
            UorN_N = 0
        elif type == "NEW":
            self.UorN_D_BTN.config(bg = "white")
            self.UorN_U_BTN.config(bg = "white")
            self.UorN_N_BTN.config(bg = "green")
            UorN_D = 0
            UorN_U = 0
            UorN_N = 1
        else:
            self.UorN_D_BTN.config(bg = "white")
            self.UorN_U_BTN.config(bg = "green")
            self.UorN_N_BTN.config(bg = "white")
            UorN_D = 0
            UorN_U = 1
            UorN_N = 0


    def create_widgets(self):
        self.yearLbl = tk.Label(self.master, text = 'Year')
        self.yearLbl.grid()
        self.yearEntry = tk.Entry(self.master, text = 'Year')
        self.yearEntry.grid()

        self.UorNLbl = tk.Label(self.master, text = 'Is your car used, new or a demo car')
        self.UorNLbl.grid()

        self.ButtonFrame = tk.LabelFrame(self.master)
        self.ButtonFrame.grid()

        self.UorN_D_BTN = tk.Button(self.ButtonFrame, text = "Demo", command = lambda: self.UorN("DEMO"))
        self.UorN_D_BTN.pack(side = "left")

        self.UorN_U_BTN = tk.Button(self.ButtonFrame, text = "Used", command = lambda: self.UorN("USED"))
        self.UorN_U_BTN.pack(side = "left")

        self.UorN_N_BTN = tk.Button(self.ButtonFrame, text = "NEW", command = lambda: self.UorN("NEW"))
        self.UorN_N_BTN.pack(side = "left")

        self.FCLbl = tk.Label(self.master, text = 'Litres of Fuel Consumption per 100km')
        self.FCLbl.grid()

        self.FuelConsumption = tk.Entry(self.master, text = 'Litres of Fuel Consumption per 100km')
        self.FuelConsumption.grid()

        self.KMLbl = tk.Label(self.master, text = "Number of Kilometres the car has done")
        self.KMLbl.grid()

        self.Kilometres = tk.Entry(self.master)
        self.Kilometres.grid()

        self.CylLbl = tk.Label(self.master, text = "Number of cylinders in the engine")
        self.CylLbl.grid()

        self.CylInEngine = tk.Entry(self.master)
        self.CylInEngine.grid()

        predict_button = tk.Button(self.master, text='Predict Price', command=self.predict_price)
        predict_button.grid()

    def predict_price(self):
        global UorN_D
        global UorN_U
        global UorN_N
        Year = float(self.yearEntry.get())
        Kilometres = float(self.Kilometres.get())
        FuelConsumption = float(self.FuelConsumption.get())
        CylInEngine = float(self.CylInEngine.get())

        inputs = [Year,UorN_D,UorN_N,UorN_U,FuelConsumption,Kilometres,CylInEngine]
        price = self.model.predict([inputs])
        messagebox.showinfo('Predicted Price', f'The predicted vehicle price is ${price[0]:.2f}')
        self.UorN_D_BTN.config(bg = "white")
        self.UorN_U_BTN.config(bg = "white")
        self.UorN_N_BTN.config(bg = "white")

if __name__ == '__main__':
    root = tk.Tk()
    app = VehiclePricePredictionApp(root)
    root.mainloop()