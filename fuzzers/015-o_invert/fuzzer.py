from util import database, toolchain, bitdiff, progress


with database.transact() as db:
    for device_name, device in db.items():
        if device_name.startswith('ATF1508'):
            progress()
            print(f"Skipping {device_name} because the fuzzer is broken on it")
            continue
        else:
            progress(device_name)

        package, pinout = next(iter(device['pins'].items()))
        for macrocell_name, macrocell in device['macrocells'].items():
            if macrocell['pad'] not in pinout:
                continue
            progress(1)

            def run(code):
                return toolchain.run(
                    f"module top(input CLK1, CLK2, OE1, output Q);"
                    f"{code}"
                    f"endmodule",
                    {
                        'CLK1': pinout['C1'],
                        'CLK2': pinout['C2'],
                        'OE1': pinout['E1'],
                        'Q': pinout[macrocell['pad']],
                    },
                    f"{device_name}-{package}")

            f_n = run("OR3    o1 (CLK1, CLK2, OE1, Q);")
            f_p = run("AND3I3 ai1(CLK1, CLK2, OE1, Q);")

            # According to the datasheet, "At [power on reset], all registers will be initialized,
            # and the state of each output will depend on the polarity of its buffer." Indeed,
            # the XOR term inversion fuse controls the power-up state of the flip-flop as well.
            # Interestingly, it does not affect AR or AS inputs (AR always resets FF to 0,
            # AS to 1), does not affect either of the fast FF input paths, and affects output
            # of buried FFs.
            #
            # It seems more accurate to say this bit controls reset value and combinatorial term
            # polarity rather than output buffer polarity; it appears to be an inverter placed
            # between the XOR gate and the 3:1 FF D mux on the diagram.

            # https://www.dataman.com/media/datasheet/Atmel/ATF15xxAE_doc2398.pdf
            macrocell.update({
                'xor_invert':
                    bitdiff.describe(1, {'off': f_n, 'on':  f_p}),
                'reset':
                    bitdiff.describe(1, {'GND': f_p, 'VCC': f_n}),
            })
