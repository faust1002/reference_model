from enum import Enum


class FrameType(Enum):
    FDD = 0
    TDD = 1

class SubcarrierSpacing(Enum):
    kHz15  = 0
    kHz30  = 1
    kHz120 = 2

    def __gt__(self, other) -> bool:
        return self.value > other.value

    def __lt__(self, other) -> bool:
        return self.value < other.value

class CyclicPrefix(Enum):
    NORMAL   = 0
    EXTENDED = 1

class Bandwidth(Enum):
    MHz3 =   0
    MHz5 =   1
    MHz10 =  2
    MHz15 =  3
    MHz20 =  4
    MHz25 =  5
    MHz30 =  6
    MHz35 =  7
    MHz40 =  8
    MHz45 =  9
    MHz50 =  10
    MHz60 =  11
    MHz70 =  12
    MHz80 =  13
    MHz90 =  14
    MHz100 = 15
    MHz200 = 16
    MHz400 = 17

N_RB_sc = 12
N_slot_symb = 14
NUMBER_SUBFRAMES_PER_SFN = 1024

# 3GPP TS 38.101-1 Table 5.3.2-1 & 3GPP TS 38.101-2 Table 5.3.2-1
__Max_Transmission_Bandwidth = {
    SubcarrierSpacing.kHz15:  {Bandwidth.MHz3: 15, Bandwidth.MHz5: 25, Bandwidth.MHz10: 52, Bandwidth.MHz15: 79, Bandwidth.MHz20: 106, Bandwidth.MHz25: 133,
                               Bandwidth.MHz30: 160, Bandwidth.MHz35: 188, Bandwidth.MHz40: 216, Bandwidth.MHz45: 242, Bandwidth.MHz50: 270},
    SubcarrierSpacing.kHz30:  {Bandwidth.MHz5: 11, Bandwidth.MHz10: 20, Bandwidth.MHz15: 38, Bandwidth.MHz20: 51, Bandwidth.MHz25: 65, Bandwidth.MHz30: 78,
                               Bandwidth.MHz40: 106, Bandwidth.MHz45: 119, Bandwidth.MHz50: 133, Bandwidth.MHz60: 162, Bandwidth.MHz70: 189, Bandwidth.MHz80: 217,
                               Bandwidth.MHz90: 245, Bandwidth.MHz100: 273},
    SubcarrierSpacing.kHz120: {Bandwidth.MHz50: 32, Bandwidth.MHz100: 66, Bandwidth.MHz200: 132, Bandwidth.MHz400: 264},
}

def get_max_number_of_rbs(bandwidth : Bandwidth, scs : SubcarrierSpacing) -> int:
    return __Max_Transmission_Bandwidth[scs][bandwidth]

def calculate_fft_size(number_of_rbs : int) -> int:
    return 1 << (number_of_rbs * N_RB_sc - 1).bit_length()
