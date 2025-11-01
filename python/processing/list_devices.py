from rtlsdr import RtlSdr

sdr = RtlSdr()
print("RTL-SDR Detected")
print(sdr:get_device_serial_address())
sdr.close()
