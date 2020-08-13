from util import database, toolchain, bitdiff


with database.transact() as db:
    for device_name, device in db.items():
        package, pinout = next(iter(device['pins'].items()))
        for macrocell_idx, (macrocell_name, macrocell) in enumerate(device['macrocells'].items()):
            def run(code):
                return toolchain.run(
                    f"module top(input CLK, output O); "
                    f"wire Q; TRI tri(Q, 1'b0, O); "
                    f"{code} "
                    f"endmodule",
                    {
                        'CLK': pinout[device['clocks']['1']['pad']],
                        'ff': str(601 + macrocell_idx),
                    },
                    f"{device_name}-{package}")

            f_dff = run("DFF ff(.CLK(CLK), .D(1'b0), .Q(Q));")
            f_tff = run("TFF ff(.CLK(CLK), .T(1'b0), .Q(Q));")

            # The GND choice of XOR B mux is shared with !PT1 and !PT2 choices: if o_inv is off,
            # then it is GND; otherwise: if pt2_mux is xor and xor_a_mux is sum, then it is !PT2;
            # if pt1_mux is flb and xor_a_mux is vcc_pt2, then it is !PT1; otherwise it is GND.
            # Further, the XOR B mux is linked to FLB: if XOR B mux is !PT1, then FLB is always 1,
            # otherwise FLB follows pt1_mux.

            macrocell.update({
                'xor_b_mux':
                    bitdiff.describe(1, {
                        'gnd_npt12': f_dff,
                        'ff_q':      f_tff
                    })
            })
