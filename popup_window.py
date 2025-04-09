import tkinter as tk
from sensor import TemperatureSensor, HumiditySensor, PressureSensor, WindSensor, InsolationSensor, Sensor
from sensor_window import SensorWindow


class AddSensorWindow(tk.Toplevel):
    def __init__(self, root, callback, list_of_dicts):
        tk.Toplevel.__init__(self, root)
        self.title("Add new sensor")
        self.protocol('WM_DELETE_WINDOW', self.display_msg)
        self.resizable(False, False)

        self.callback = callback
        self.list_of_dicts = list_of_dicts
        sensor_options = ["Temperature", "Humidity", "Pressure", "Wind", "Insolation"]

        self.selected_sensor = tk.StringVar(self)
        self.selected_sensor.set(sensor_options[0])

        option_menu_sensor_of = tk.OptionMenu(self, self.selected_sensor, *sensor_options)

        unit = Sensor.to_sensor(self.selected_sensor.get()).unit()

        label_sensor_name = tk.Label(self, text="Sensor name:")
        label_sensor_of = tk.Label(self, text="Sensor of:")
        self.label_low_limit = tk.Label(self, text=f"Low limit [{unit}]:")
        self.label_high_limit = tk.Label(self, text=f"High limit [{unit}]:")
        label_measurement = tk.Label(self, text="Measurement interval [ms]:")

        self.entry_sensor_name = tk.Entry(self)
        self.entry_low_limit = tk.Entry(self)
        self.entry_high_limit = tk.Entry(self)
        self.entry_measurement = tk.Entry(self)

        btn_add_sensor = tk.Button(self, text="Add", command=self.func_confirm_add)

        '''Placement widgets'''
        label_sensor_name.grid(row=0, column=0)
        self.entry_sensor_name.grid(row=0, column=1)

        label_sensor_of.grid(row=1, column=0)
        option_menu_sensor_of.grid(row=1, column=1)

        label_measurement.grid(row=2, column=0)
        self.entry_measurement.grid(row=2, column=1)

        self.label_low_limit.grid(row=0, column=3)
        self.entry_low_limit.grid(row=0, column=4)

        self.label_high_limit.grid(row=1, column=3)
        self.entry_high_limit.grid(row=1, column=4)

        btn_add_sensor.grid(row=3, column=2)

        '''Trace changes to the selected_sensor variable and update unit labels'''
        self.selected_sensor.trace_add("write", self.update_unit_labels)

    def update_unit_labels(self, *args):

        unit = Sensor.to_sensor(self.selected_sensor.get()).unit()
        label_low_limit = f"Low limit ({unit}): "
        label_high_limit = f"High limit ({unit}): "

        self.label_low_limit.config(text=label_low_limit)
        self.label_high_limit.config(text=label_high_limit)

    def test(self):
        tescik = True
        try:
            entry_low_limit = int(self.entry_low_limit.get())
        except ValueError as v:
            print(f"Error:{v}")
            tescik = False
            print('Zła wartosc zostala wpisana do rubryki "Low limit"')

        try:
            entry_high_limit = int(self.entry_high_limit.get())
        except ValueError as v:
            print(f"Error:{v}")
            tescik = False
            print('Zła wartosc zostala wpisana do rubryki "High limit"')

       
        return tescik

    def func_confirm_add(self):

        if self.test() is True:
            sensor_type = self.selected_sensor.get()
            sensor_name = self.entry_sensor_name.get()
            interval = int(self.entry_measurement.get())
            low_limit = int(self.entry_low_limit.get())
            high_limit = int(self.entry_high_limit.get())
      
            self.callback({"name": sensor_name, "type": sensor_type, "interval": interval, "low_limit": low_limit, "high_limit": high_limit})

            self.destroy()

    def display_msg(self):
        print("Setting sensor parameters canceled")
        self.destroy()


if __name__ == '__main__':
    from main import main
    main()
