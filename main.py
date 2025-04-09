import tkinter as tk
from graphic_weather_station import GraphicWeatherStation
from popup_window import AddSensorWindow


def main():
    root = tk.Tk()
    app = GraphicWeatherStation(root)
    root.mainloop()


if __name__ == '__main__':

    main()
