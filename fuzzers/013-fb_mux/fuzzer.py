from util import database, toolchain, bitdiff


with database.transact() as db:
    for device_name, device in db.items():
        package, pinout = next(iter(device['pins'].items()))
        for macrocell_idx, (macrocell_name, macrocell) in enumerate(device['macrocells'].items()):
            for other1_macrocell_name, other1_macrocell in device['macrocells'].items():
                if other1_macrocell_name != macrocell_name and other1_macrocell['pad'] in pinout:
                    break
            else:
                assert False
            for other2_macrocell_name, other2_macrocell in device['macrocells'].items():
                if (other2_macrocell_name != macrocell_name and
                        other2_macrocell_name != other1_macrocell_name and
                        other2_macrocell['pad'] in pinout):
                    break
            else:
                assert False

            def run(code, **kwargs):
                return toolchain.run(
                    f"module top(input CLK1, CLK2, output O1, O2); "
                    f"{code} "
                    f"endmodule",
                    {
                        'CLK1': pinout[device['clocks']['1']['pad']],
                        'CLK2': pinout[device['clocks']['2']['pad']],
                        'O1': pinout[other1_macrocell['pad']],
                        'O2': pinout[other2_macrocell['pad']],
                        'dff1': str(601 + macrocell_idx),
                        # Pretty gross to rely on autogenerated names, but the other
                        # netlist/constraint sets I came up were even less reliable.
                        'Com_Ctrl_13': str(601 + macrocell_idx),
                    },
                    f"{device_name}-{package}", **kwargs)

            f_sync = run(
                f"wire Y1; XOR2 x1(CLK1, CLK2, Y1); "
                f"wire Q1; DFF dff1(1'b0, Y1, Q1); "
                f"TRI t1(1'b0, Q1, O1); "
                f"TRI t2(1'b0, Q1, O2); ",
                name="work-sync"
            )
            f_comb = run(
                f"wire Y1; XOR2 x1(CLK1, CLK2, Y1); "
                f"TRI t1(1'b0, Y1, O1); "
                f"TRI t2(1'b0, Y1, O2); ",
                name="work-comb"
            )

            # Feedback can be taken from either XOR term or FF/latch output.
            macrocell.update({
                'fb_mux':
                    bitdiff.describe(1, {'comb': f_comb, 'sync': f_sync}),
            })
