How this works;

1. Waspmote connects to Raspberry Pi through serial.
2. Pi sends strings with numbers that ends in char c, eg '545c'. This number denotes concentration in ug/L of Chl-a.
3. Waspmote reads from USB and then sends to Gateway.
4. If approved Waspmote sends ACK to pi, othewise NACK.
5. Pi determines whether it should resend or send based on response.