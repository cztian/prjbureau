from util import database


def pins(Mn, C1, E1, R, C2):
    return {
        **{
            f"M{1+mi}": pin
            for mi, pin in enumerate(Mn.split())
            if pin != "0"
        },
        **{
            "C1": C1,
            "E1": E1,
            "R":  R,
            "C2": C2,
        }
    }


def atf15xx(*, ranges, blocks, specials, pins, flip_muxes=False):
    return {
        "ranges": ranges,
        "blocks": {
            bn: {
                "macrocells": [f"MC{1+16*bi+mi}" for mi in range(16)],
                "switches": [],
                "pterm_points": {},
            } for bi, bn in enumerate(blocks)
        },
        "macrocells": {
            f"MC{1+mi}": {
                "block": blocks[mi // 16],
                "pad": f"M{1+mi}",
                "pterm_ranges": {
                    f"PT{1+pi}": None
                    for pi in range(5)
                }
            } for mi in range(len(blocks) * 16)
        },
        "switches": {
            f"UIM{1+xi}": {
                "block": None
            } for xi in range(len(blocks) * 40)[::-1 if flip_muxes else 1]
        },
        "globals": {
            "GCLR": {},
            **{
                f"GCLK{1+xi}": {
                } for xi in range(3)
            },
            **{
                f"GOE{1+xi}": {
                } for xi in range(6)[::-1 if flip_muxes else 1]
            },
        },
        "config": {
            "pins": {},
        },
        "user": [],
        "pins": pins,
        "specials": {
            "CLR":  "R",
            "CLK1": "C1",
            "CLK2": "C2",
            "OE1":  "E1",
            "OE2":  "C2",
            **specials
        }
    }


def atf1502xx(*, ranges, specials={}):
    return atf15xx(**{
        "ranges": ranges,
        "blocks": "AB",
        "pins": {
            "TQFP44": pins(
                Mn="42 43 44  1  2  3  5  6  7  8 10 11 12 13 14 15 "
                   "35 34 33 32 31 30 28 27 26 25 23 22 21 20 19 18 ",
                C1="37",
                E1="38",
                R ="39",
                C2="40"),
            "PLCC44": pins(
                Mn=" 4  5  6  7  8  9 11 12 13 14 16 17 18 19 20 21 "
                   "41 40 39 38 37 36 34 33 32 31 29 28 27 26 25 24 ",
                C1="43",
                E1="44",
                R ="1",
                C2="2"),
        },
        "specials": {
            "TDI":  "M4",
            "PD1":  "M7",
            "TMS":  "M9",
            "CLK3": "M17",
            "TDO":  "M20",
            "TCK":  "M25",
            "PD2":  "M31",
            **specials
        },
        "flip_muxes": True,
    })


def atf1504xx(*, ranges, specials={}):
    return atf15xx(**{
        "ranges": ranges,
        "blocks": "ABCD",
        "pins": {
            "TQFP100": pins(
                Mn=" 14  13  12  10   9   8   6   4 100  99  98  97  96 "
                   " 94  93  92  37  36  35  33  32  31  30  29  25  23 "
                   " 21  20  19  17  16  15  40  41  42  44  45  46  47 "
                   " 48  52  54  56  57  58  60  61  62  63  64  65  67 "
                   " 68  69  71  73  75  76  79  80  81  83  84  85",
                C1="87",
                E1="88",
                R ="89",
                C2="90"),
            "PQFP100": pins(
                Mn=" 16  15  14  12  11  10   8   6   4   3 100  99  98 "
                   " 96  95  94  39  38  37  35  34  33  32  31  27  25 "
                   " 23  22  21  19  18  17  42  43  44  46  47  48  49 "
                   " 50  54  56  58  59  60  62  63  64  65  66  67  69 "
                   " 70  71  73  75  77  78  81  82  83  85  86  87",
                C1="89",
                E1="90",
                R ="91",
                C2="92"),
            "PLCC84": pins(
                Mn=" 22  21  20  18  17  16  15  14  12  11  10   9   8 "
                   "  6   5   4  41  40  39  37  36  35  34  33  31  30 "
                   " 29  28  27  25  24  23  44  45  46  48  49  50  51 "
                   " 52  54  55  56  57  58  60  61  62  63  64  65  67 "
                   " 68  69  70  71  73  74  75  76  77  79  80  81",
                C1="83",
                E1="84",
                R ="1",
                C2="2"),
            "PLCC68": pins(
                Mn=" 18   0  17  15  14  13   0  12  10   0   9   8   7 "
                   "  5   0   4  33   0  32  30  29  28   0  27  25   0 "
                   " 24  23  22  20   0  19  36   0  37  39  40  41   0 "
                   " 42  44   0  45  46  47  49   0  50  51   0  52  54 "
                   " 55  56   0  57  59   0  60  61  62  64   0  65",
                C1="67",
                E1="68",
                R ="1",
                C2="2"),
            "TQFP44": pins(
                Mn="  6   0   5   3   2   0   0   1   0   0  44   0   0 "
                   " 43   0  42  15   0  14  13  12   0   0  11  10   0 "
                   "  0   0   0   8   0   7  18   0  19  20  21   0   0 "
                   " 22  23   0   0   0   0  25   0  26  27   0  28  30 "
                   " 31   0   0  32  33   0   0   0   0  34   0  35",
                C1="37",
                E1="38",
                R ="39",
                C2="40"),
            "PLCC44": pins(
                Mn=" 12   0  11   9   8   0   0   7   0   0   6   0   0 "
                   "  5   0   4  21   0  20  19  18   0   0  17  16   0 "
                   "  0   0   0  14   0  13  24   0  25  26  27   0   0 "
                   " 28  29   0   0   0   0  31   0  32  33   0  34  36 "
                   " 37   0   0  38  39   0   0   0   0  40   0  41",
                C1="43",
                E1="44",
                R ="1",
                C2="2"),
        },
        "specials": {
            "PD1":  "M3",
            "TDI":  "M8",
            "TMS":  "M32",
            "PD2":  "M35",
            "TCK":  "M48",
            "TDO":  "M56",
            "CLK3": "M64",
            **specials
        }
    })


def atf1508xx(*, ranges, specials={}):
    return atf15xx(**{
        "ranges": ranges,
        "blocks": "ABCDEFGH",
        "pins": {
            "PQFP160": pins(
                Mn="160   0 159 158 153 152   0 151 150   0 149 147 146 145   0 144  21   0  20 "
                   " 19  18  16   0  15  14   0  13  12  11  10   0   9  41   0  33  32  31  30 "
                   "  0  29  28   0  27  25  24  23   0  22  59   0  58  57  56  54   0  53  52 "
                   "  0  51  50  49  48   0  43  62   0  63  64  65  67   0  68  69   0  70  71 "
                   " 72  73   0  78  80   0  88  89  90  91   0  92  93   0  94  96  97  98   0 "
                   " 99 100   0 101 102 103 105   0 106 107   0 108 109 110 111   0 112 121   0 "
                   "122 123 128 129   0 130 131   0 132 134 135 136   0 137",
                C1="139",
                E1="140",
                R ="141",
                C2="142"),
            "PQFP100": pins(
                Mn="  4   0   3   0   2   1   0 100  99   0  98   0  96  95   0  94  16   0  15 "
                   "  0  14  12   0  11  10   0   9   0   8   7   0   6  27   0  26   0  25  24 "
                   "  0  23  22   0  21   0  19  18   0  17  39   0  38   0  37  35   0  34  33 "
                   "  0  32   0  31  30   0  29  42   0  43   0  44  46   0  47  48   0  49   0 "
                   " 50  51   0  52  54   0  55   0  56  57   0  58  59   0  60   0  62  63   0 "
                   " 64  65   0  66   0  67  69   0  70  71   0  72   0  73  74   0  75  77   0 "
                   " 78   0  79  80   0  81  82   0  83   0  85  86   0  87",
                C1="89",
                E1="90",
                R ="91",
                C2="92"),
            "TQFP100": pins(
                Mn="  2   0   1   0 100  99   0  98  97   0  96   0  94  93   0  92  14   0  13 "
                   "  0  12  10   0   9   8   0   7   0   6   5   0   4  25   0  24   0  23  22 "
                   "  0  21  20   0  19   0  17  16   0  15  37   0  36   0  35  33   0  32  31 "
                   "  0  30   0  29  28   0  27  40   0  41   0  42  44   0  45  46   0  47   0 "
                   " 48  49   0  50  52   0  53   0  54  55   0  56  57   0  58   0  60  61   0 "
                   " 62  63   0  64   0  65  67   0  68  69   0  70   0  71  72   0  73  75   0 "
                   " 76   0  77  78   0  79  80   0  81   0  83  84   0  85",
                C1="87",
                E1="88",
                R ="89",
                C2="90"),
            "PLCC84": pins(
                Mn="  0   0  12   0  11  10   0   9   0   0   8   0   6   5   0   4  22   0  21 "
                   "  0  20   0   0  18  17   0  16   0  15   0   0  14   0   0  31   0  30  29 "
                   "  0  28   0   0  27   0  25  24   0  23  41   0  40   0  39   0   0  37  36 "
                   "  0  35   0  34   0   0  33  44   0  45   0  46   0   0  48  49   0  50   0 "
                   " 51   0   0  52   0   0  54   0  55  56   0  57   0   0  58   0  60  61   0 "
                   " 62  63   0  64   0  65   0   0  67  68   0  69   0  70   0   0  71   0   0 "
                   " 73   0  74  75   0  76   0   0  77   0  79  80   0  81",
                C1="83",
                E1="84",
                R ="1",
                C2="2"),
        },
        "specials": {
            "PD1":  "M3",
            "TDI":  "M32",
            "TMS":  "M48",
            "PD2":  "M67",
            "TCK":  "M96",
            "TDO":  "M112",
            "CLK3": "M128",
            **specials
        }
    })


database.save({
    "ATF1502AS": atf1502xx(**{
        "ranges": {
            "pterms":     [    0, 15360],
            "macrocells": [15360, 16320],
            "uim_muxes":  [16320, 16720],
            "goe_muxes":  [16720, 16750],
            "config":     [16750, 16786],
            "user":       [16786, 16802],
            "reserved":   [16802, 16808],
        },
    }),
    "ATF1502BE": atf1502xx(**{
        "ranges": {
            "pterms":     [    0, 15360],
            "macrocells": [15360, 16320],
            "uim_muxes":  [16320, 16720],
            "goe_muxes":  [16720, 16750],
            "config":     [16750, 16790],
            "user":       [16790, 16806],
            "reserved":   [16806, 16814],
        }
    }),
    "ATF1504AS": atf1504xx(**{
        "ranges": {
            "pterms":     [    0, 30720],
            "macrocells": [30720, 32640],
            "uim_muxes":  [32640, 34080],
            "goe_muxes":  [34080, 34134],
            "config":     [34134, 34170],
            "user":       [34170, 34186],
            "reserved":   [34186, 34192],
        }
    }),
    "ATF1504BE": atf1504xx(**{
        "ranges": {
            "pterms":     [    0, 30720],
            "macrocells": [30720, 32640],
            "uim_muxes":  [32640, 34080],
            "goe_muxes":  [34080, 34134],
            "config":     [34134, 34174],
            "user":       [34174, 34190],
            "reserved":   [34190, 34198],
        },
        "specials": {
            "VREFA": "M3",
            "VREFB": "M46",
        }
    }),
    # "ATF1508AS": atf1508xx(**{
    #     "ranges": {
    #         "pterms":     [    0, 61440],
    #         "macrocells": [61440, 65280],
    #         "uim_muxes":  [65280, 73920],
    #         "goe_muxes":  [73920, 74082],
    #         "config":     [74082, 74118],
    #         "user":       [74118, 74134],
    #         "reserved":   [74134, 74136],
    #     },
    # }),
    # "ATF1508BE": atf1508xx(**{
    #     "ranges": {
    #         "pterms":     [    0, 61440],
    #         "macrocells": [61440, 65280],
    #         "uim_muxes":  [65280, 73920],
    #         "goe_muxes":  [73920, 74082],
    #         "config":     [74082, 74122],
    #         "user":       [74122, 74138],
    #         "reserved":   [74138, 74146],
    #     },
    #     "specials": {
    #         "VREFA": "M21",
    #         "VREFB": "M93",
    #     }
    # }),
})
