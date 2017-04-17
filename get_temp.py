#!/usr/bin/env python3

from datetime import datetime

def read_temperature(tfile):
    """Read the temperature from a given device file."""
    # open the file and read its content
    f = open(tfile)
    text = f.read()
    f.close()
    # Keep the time of the measurement
    m_time = datetime.utcnow()
    # read the temperature part from the file (20th argument)
    tempdata = text.split(" ")[20]
    # temperature from 3rd char in string, convert to float, divide by 1000 for C
    temperature = float(tempdata[2:]) / 1000
    return temperature, m_time

def main():
    temp01 = ("/sys/bus/w1/devices/28-031600954bff/w1_slave")
    temperature, m_time = read_temperature(temp01)
    print (temperature)


if __name__ == "__main__":
    main()

