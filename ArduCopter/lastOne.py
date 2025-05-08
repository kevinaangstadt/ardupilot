import serial
import time
import datetime

def calculate_checksum(nmea_sentence):
    checksum = 0
    for char in nmea_sentence:
        checksum ^= ord(char)
    return f"{checksum:02X}"


def send_continuous_gps_data(serial_port, baud_rate):
    try:
        ser = serial.Serial(serial_port, baud_rate, timeout=1)
        print(f"Connected to {ser.name} at {ser.baudrate} baudrate")


        time_after_loop = time.time() # initialization
        frequency = 1/7



        while True:
            current_time_utc = datetime.datetime.utcnow().strftime('%H%M%S.%f')[:-3]
            current_date_utc = time.strftime('%d%m%y', time.gmtime())
            other_date = time.strftime('%d,%m,%Y', time.gmtime())
            nmea_sentences_without = [
                f"GPRMC,{current_time_utc},A,4435.269116,N,07509.683358,W,0.0,113.6,{current_date_utc},,A",
                f"GPGGA,{current_time_utc},4435.269116,N,07509.683358,W,1,08,1.2,-0.219,M,0.0,M,,",
                f"GPVTG,113.6,T,113.6,M,0.0,N,0.0,K,A*",
                f"GPZDA,{current_time_utc},{other_date},00,00"
            ]
            nmea_sentences = []
            for sentence in nmea_sentences_without:
                checksum = calculate_checksum(sentence)
                nmea_sentences.append(f"${sentence}*{checksum}")




            time_before_loop = time.time()
            if time_before_loop - time_after_loop >= frequency:
                real_frequency = time_before_loop - time_after_loop
                #print(real_frequency)
      # main programm
                send(nmea_sentences, ser)
                time_after_loop = time.time()
#            print(current_time_utc)
 #           print(current_date_utc)
  #          print(other_date)

            # Define the NMEA 0183 sentences to be sent


#            combined_sentences = '\r\n'.join(nmea_sentences) + '\r\n'
#            ser.write(combined_sentences.encode('utf-8'))
#            ser.flush()
#            print(f"Sent NMEA 0183 Sentence: {combined_sentences}")
#            time.sleep(.009)  # Adjust the delay as needed

    except serial.SerialException as e:
        print(f"Error: {e}")

    finally:
        if ser.is_open:
            ser.close()
            print("Serial connection closed")

def send(sentences, serr):
    combined_sentences = '\r\n'.join(sentences) + '\r\n'
    serr.write(combined_sentences.encode('utf-8'))

if __name__ == "__main__":
    serial_port = '/dev/ttyUSB0'  # Adjust with your serial port
    baud_rate = 115200  # Adjust with your baud rate
    send_continuous_gps_data(serial_port, baud_rate)

