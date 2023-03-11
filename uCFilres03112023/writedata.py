#send data from the uart2 for data transmission

from pyb import repl_uart

"""This disables the Repl on the UART2
Now it can only read data and not write it

@ param sets the UART 2 Port and the  """
# repl_uart(None) this makes it so you can only read and not write

ser = UART(2,115200)

ser.write()

        

