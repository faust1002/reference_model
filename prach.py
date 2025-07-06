import logging
from dataclasses import dataclass
from enum import Enum

import numpy as np

import frame_defs


class PrachConfigurationIndex(Enum):
    CONFIGURATION_INDEX_0  = 0
    CONFIGURATION_INDEX_1  = 1
    CONFIGURATION_INDEX_2  = 2
    CONFIGURATION_INDEX_3  = 3
    CONFIGURATION_INDEX_28 = 28
    CONFIGURATION_INDEX_29 = 29
    CONFIGURATION_INDEX_30 = 30
    CONFIGURATION_INDEX_31 = 31
    CONFIGURATION_INDEX_34 = 34
    CONFIGURATION_INDEX_35 = 35
    CONFIGURATION_INDEX_36 = 36
    CONFIGURATION_INDEX_37 = 37
    CONFIGURATION_INDEX_40 = 40
    CONFIGURATION_INDEX_41 = 41
    CONFIGURATION_INDEX_42 = 42
    CONFIGURATION_INDEX_43 = 43
    CONFIGURATION_INDEX_53 = 53
    CONFIGURATION_INDEX_54 = 54
    CONFIGURATION_INDEX_55 = 55
    CONFIGURATION_INDEX_56 = 56
    CONFIGURATION_INDEX_60 = 60
    CONFIGURATION_INDEX_61 = 61
    CONFIGURATION_INDEX_62 = 62
    CONFIGURATION_INDEX_63 = 63

class PrachFormat(Enum):
    FORMAT_0 = 0
    FORMAT_1 = 1
    FORMAT_2 = 2
    FORMAT_3 = 3

class PrachRestrictedSet(Enum):
    UNRESTRICTED_SET      = 0
    RESTRICTED_SET_TYPE_A = 1
    RESTRICTED_SET_TYPE_B = 2

@dataclass
class RACH_ConfigGeneric:
    prach_ConfigurationIndex : PrachConfigurationIndex = PrachConfigurationIndex.CONFIGURATION_INDEX_0
    zeroCorrelationConfigZone : int = 1

@dataclass
class RACH_ConfigCommon:
    rach_ConfigGeneric : RACH_ConfigGeneric
    totalNumberOfRA_Preambles : int
    prach_RootSequenceIndex : int
    restrictedSetConfig : PrachRestrictedSet

    def __init__(self, rach_ConfigGeneric : RACH_ConfigGeneric | None = None, totalNumberOfRA_Preambles : int = 63,
                prach_RootSequenceIndex : int = 0, restrictedSetConfig : PrachRestrictedSet = PrachRestrictedSet.UNRESTRICTED_SET):
        if rach_ConfigGeneric is None:
            self.rach_ConfigGeneric = RACH_ConfigGeneric()
        else:
            self.rach_ConfigGeneric = rach_ConfigGeneric

        assert 1 <= totalNumberOfRA_Preambles <= 63, f'Total number of RA preambles ({totalNumberOfRA_Preambles}) out of bound (1, 63)'
        self.totalNumberOfRA_Preambles = totalNumberOfRA_Preambles

        assert 0 <= prach_RootSequenceIndex <= 837, f'PRACH root sequence index ({prach_RootSequenceIndex}) out of bound (0, 837)'
        self.prach_RootSequenceIndex = prach_RootSequenceIndex

        self.restrictedSetConfig = restrictedSetConfig

# 3GPP TS 38.211, Table 6.3.3.1-1
__PrachPreamblesFormats : dict[PrachFormat, dict[str, int]] = {
    PrachFormat.FORMAT_0: {'L_RA': 839, 'f_RA': int(1.25e3), 'N_u': 24576,     'N_RA_CP': 3168},
    PrachFormat.FORMAT_1: {'L_RA': 839, 'f_RA': int(1.25e3), 'N_u': 2 * 24576, 'N_RA_CP': 21024},
    PrachFormat.FORMAT_2: {'L_RA': 839, 'f_RA': int(1.25e3), 'N_u': 4 * 24576, 'N_RA_CP': 4688},
    PrachFormat.FORMAT_3: {'L_RA': 839, 'f_RA': int(5e3),    'N_u': 4 * 6144,  'N_RA_CP': 3168}
}

# 3GPP TS 38.211, Table 6.3.3.1-3
__root_sequence_index_mapping_L_RA_839 = [
    129, 710, 140, 699, 120, 719, 210, 629, 168, 671, 84, 755, 105, 734, 93, 746, 70, 769, 60, 779,
    2, 837, 1, 838, 56, 783, 112, 727, 148, 691, 80, 759, 42, 797, 40, 799, 35, 804, 73, 766,
    146, 693, 31, 808, 28, 811, 30, 809, 27, 812, 29, 810, 24, 815, 48, 791, 68, 771, 74, 765,
    178, 661, 136, 703, 86, 753, 78, 761, 43, 796, 39, 800, 20, 819, 21, 818, 95, 744, 202, 637,
    190, 649, 181, 658, 137, 702, 125, 714, 151, 688, 217, 622, 128, 711, 142, 697, 122, 717, 203, 636,
    118, 721, 110, 729, 89, 750, 103, 736, 61, 778, 55, 784, 15, 824, 14, 825, 12, 827, 23, 816,
    34, 805, 37, 802, 46, 793, 207, 632, 179, 660, 145, 694, 130, 709, 223, 616, 228, 611, 227, 612,
    132, 707, 133, 706, 143, 696, 135, 704, 161, 678, 201, 638, 173, 666, 106, 733, 83, 756, 91, 748,
    66, 773, 53, 786, 10, 829, 9, 830, 7, 832, 8, 831, 16, 823, 47, 792, 64, 775, 57, 782,
    104, 735, 101, 738, 108, 731, 208, 631, 184, 655, 197, 642, 191, 648, 121, 718, 141, 698, 149, 690,
    216, 623, 218, 621, 152, 687, 144, 695, 134, 705, 138, 701, 199, 640, 162, 677, 176, 663, 119, 720,
    158, 681, 164, 675, 174, 665, 171, 668, 170, 669, 87, 752, 169, 670, 88, 751, 107, 732, 81, 758,
    82, 757, 100, 739, 98, 741, 71, 768, 59, 780, 65, 774, 50, 789, 49, 790, 26, 813, 17, 822,
    13, 826, 6, 833, 5, 834, 33, 806, 51, 788, 75, 764, 99, 740, 96, 743, 97, 742, 166, 673,
    172, 667, 175, 664, 187, 652, 163, 676, 185, 654, 200, 639, 114, 725, 189, 650, 115, 724, 194, 645,
    195, 644, 192, 647, 182, 657, 157, 682, 156, 683, 211, 628, 154, 685, 123, 716, 139, 700, 212, 627,
    153, 686, 213, 626, 215, 624, 150, 689, 225, 614, 224, 615, 221, 618, 220, 619, 127, 712, 147, 692,
    124, 715, 193, 646, 205, 634, 206, 633, 116, 723, 160, 679, 186, 653, 167, 672, 79, 760, 85, 754,
    77, 762, 92, 747, 58, 781, 62, 777, 69, 770, 54, 785, 36, 803, 32, 807, 25, 814, 18, 821,
    11, 828, 4, 835, 3, 836, 19, 820, 22, 817, 41, 798, 38, 801, 44, 795, 52, 787, 45, 794,
    63, 776, 67, 772, 72, 767, 76, 763, 94, 745, 102, 737, 90, 749, 109, 730, 165, 674, 111, 728,
    209, 630, 204, 635, 117, 722, 188, 651, 159, 680, 198, 641, 113, 726, 183, 656, 180, 659, 177, 662,
    196, 643, 155, 684, 214, 625, 126, 713, 131, 708, 219, 620, 222, 617, 226, 613, 230, 609, 232, 607,
    262, 577, 252, 587, 418, 421, 416, 423, 413, 426, 411, 428, 376, 463, 395, 444, 283, 556, 285, 554,
    379, 460, 390, 449, 363, 476, 384, 455, 388, 451, 386, 453, 361, 478, 387, 452, 360, 479, 310, 529,
    354, 485, 328, 511, 315, 524, 337, 502, 349, 490, 335, 504, 324, 515, 323, 516, 320, 519, 334, 505,
    359, 480, 295, 544, 385, 454, 292, 547, 291, 548, 381, 458, 399, 440, 380, 459, 397, 442, 369, 470,
    377, 462, 410, 429, 407, 432, 281, 558, 414, 425, 247, 592, 277, 562, 271, 568, 272, 567, 264, 575,
    259, 580, 237, 602, 239, 600, 244, 595, 243, 596, 275, 564, 278, 561, 250, 589, 246, 593, 417, 422,
    248, 591, 394, 445, 393, 446, 370, 469, 365, 474, 300, 539, 299, 540, 364, 475, 362, 477, 298, 541,
    312, 527, 313, 526, 314, 525, 353, 486, 352, 487, 343, 496, 327, 512, 350, 489, 326, 513, 319, 520,
    332, 507, 333, 506, 348, 491, 347, 492, 322, 517, 330, 509, 338, 501, 341, 498, 340, 499, 342, 497,
    301, 538, 366, 473, 401, 438, 371, 468, 408, 431, 375, 464, 249, 590, 269, 570, 238, 601, 234, 605,
    257, 582, 273, 566, 255, 584, 254, 585, 245, 594, 251, 588, 412, 427, 372, 467, 282, 557, 403, 436,
    396, 443, 392, 447, 391, 448, 382, 457, 389, 450, 294, 545, 297, 542, 311, 528, 344, 495, 345, 494,
    318, 521, 331, 508, 325, 514, 321, 518, 346, 493, 339, 500, 351, 488, 306, 533, 289, 550, 400, 439,
    378, 461, 374, 465, 415, 424, 270, 569, 241, 598, 231, 608, 260, 579, 268, 571, 276, 563, 409, 430,
    398, 441, 290, 549, 304, 535, 308, 531, 358, 481, 316, 523, 293, 546, 288, 551, 284, 555, 368, 471,
    253, 586, 256, 583, 263, 576, 242, 597, 274, 565, 402, 437, 383, 456, 357, 482, 329, 510, 317, 522,
    307, 532, 286, 553, 287, 552, 266, 573, 261, 578, 236, 603, 303, 536, 356, 483, 355, 484, 405, 434,
    404, 435, 406, 433, 235, 604, 267, 572, 302, 537, 309, 530, 265, 574, 233, 606, 367, 472, 296, 543,
    336, 503, 305, 534, 373, 466, 280, 559, 279, 560, 419, 420, 240, 599, 258, 581, 229, 610
]

__root_sequence_index_mapping = {839: __root_sequence_index_mapping_L_RA_839}

# 3GPP TS 38.211, Table 6.3.3.1-5
__N_CS_1_25kHZ = {
    PrachRestrictedSet.UNRESTRICTED_SET:      [0, 13, 15, 18, 22, 26, 32, 38, 46, 59, 76, 93, 119, 167, 279, 419],
    PrachRestrictedSet.RESTRICTED_SET_TYPE_A: [15, 18, 22, 26, 32, 38, 46, 55, 68, 82, 100, 128, 158, 202, 237],
    PrachRestrictedSet.RESTRICTED_SET_TYPE_B: [15, 18, 22, 26, 32, 38, 46, 55, 68, 82, 100, 118, 137],
}

# 3GPP TS 38.211, Table 6.3.3.1-6
__N_CS_5kHZ = {
    PrachRestrictedSet.UNRESTRICTED_SET:      [0, 13, 26, 33, 38, 41, 49, 55, 64, 76, 93, 119, 139, 209, 279, 419],
    PrachRestrictedSet.RESTRICTED_SET_TYPE_A: [36, 57, 72, 81, 89, 94, 103, 112, 121, 132, 137, 152, 173, 195, 216, 237],
    PrachRestrictedSet.RESTRICTED_SET_TYPE_B: [36, 57, 60, 63, 65, 68, 71, 77, 81, 85, 97, 109, 122, 137],
}

__N_CS = {1.25e3: __N_CS_1_25kHZ, 5e3: __N_CS_5kHZ}

# 3GPP TS 38.211, Table 6.3.3.2-2 (4 entries for each long PRACH format)
__PrachConfigurationIndex_FDD : dict[PrachConfigurationIndex, dict[str, PrachFormat]] = {
    PrachConfigurationIndex.CONFIGURATION_INDEX_0:  {'preamble_format': PrachFormat.FORMAT_0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_1:  {'preamble_format': PrachFormat.FORMAT_0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_2:  {'preamble_format': PrachFormat.FORMAT_0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_3:  {'preamble_format': PrachFormat.FORMAT_0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_28: {'preamble_format': PrachFormat.FORMAT_1},
    PrachConfigurationIndex.CONFIGURATION_INDEX_29: {'preamble_format': PrachFormat.FORMAT_1},
    PrachConfigurationIndex.CONFIGURATION_INDEX_30: {'preamble_format': PrachFormat.FORMAT_1},
    PrachConfigurationIndex.CONFIGURATION_INDEX_31: {'preamble_format': PrachFormat.FORMAT_1},
    PrachConfigurationIndex.CONFIGURATION_INDEX_53: {'preamble_format': PrachFormat.FORMAT_2},
    PrachConfigurationIndex.CONFIGURATION_INDEX_54: {'preamble_format': PrachFormat.FORMAT_2},
    PrachConfigurationIndex.CONFIGURATION_INDEX_55: {'preamble_format': PrachFormat.FORMAT_2},
    PrachConfigurationIndex.CONFIGURATION_INDEX_56: {'preamble_format': PrachFormat.FORMAT_2},
    PrachConfigurationIndex.CONFIGURATION_INDEX_60: {'preamble_format': PrachFormat.FORMAT_3},
    PrachConfigurationIndex.CONFIGURATION_INDEX_61: {'preamble_format': PrachFormat.FORMAT_3},
    PrachConfigurationIndex.CONFIGURATION_INDEX_62: {'preamble_format': PrachFormat.FORMAT_3},
    PrachConfigurationIndex.CONFIGURATION_INDEX_63: {'preamble_format': PrachFormat.FORMAT_3}
}

__PrachConfigurationIndex_FDD_TD : dict[PrachConfigurationIndex, dict[str, int]] = {
    PrachConfigurationIndex.CONFIGURATION_INDEX_0:  {'subframe_number': 1, 'starting_symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_1:  {'subframe_number': 4, 'starting_symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_2:  {'subframe_number': 7, 'starting_symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_3:  {'subframe_number': 9, 'starting_symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_28: {'subframe_number': 1, 'starting_symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_29: {'subframe_number': 4, 'starting_symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_30: {'subframe_number': 7, 'starting_symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_31: {'subframe_number': 9, 'starting_symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_53: {'subframe_number': 1, 'starting_symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_54: {'subframe_number': 1, 'starting_symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_55: {'subframe_number': 1, 'starting_symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_56: {'subframe_number': 1, 'starting_symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_60: {'subframe_number': 1, 'starting_symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_61: {'subframe_number': 4, 'starting_symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_62: {'subframe_number': 7, 'starting_symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_63: {'subframe_number': 9, 'starting_symbol': 0}
}

__PrachConfigurationIndex_TDD : dict[PrachConfigurationIndex, dict[str, PrachFormat]] = {
    PrachConfigurationIndex.CONFIGURATION_INDEX_0:  {'preamble_format': PrachFormat.FORMAT_0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_1:  {'preamble_format': PrachFormat.FORMAT_0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_2:  {'preamble_format': PrachFormat.FORMAT_0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_3:  {'preamble_format': PrachFormat.FORMAT_0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_28: {'preamble_format': PrachFormat.FORMAT_1},
    PrachConfigurationIndex.CONFIGURATION_INDEX_29: {'preamble_format': PrachFormat.FORMAT_1},
    PrachConfigurationIndex.CONFIGURATION_INDEX_30: {'preamble_format': PrachFormat.FORMAT_1},
    PrachConfigurationIndex.CONFIGURATION_INDEX_31: {'preamble_format': PrachFormat.FORMAT_1},
    PrachConfigurationIndex.CONFIGURATION_INDEX_34: {'preamble_format': PrachFormat.FORMAT_2},
    PrachConfigurationIndex.CONFIGURATION_INDEX_35: {'preamble_format': PrachFormat.FORMAT_2},
    PrachConfigurationIndex.CONFIGURATION_INDEX_36: {'preamble_format': PrachFormat.FORMAT_2},
    PrachConfigurationIndex.CONFIGURATION_INDEX_37: {'preamble_format': PrachFormat.FORMAT_2},
    PrachConfigurationIndex.CONFIGURATION_INDEX_40: {'preamble_format': PrachFormat.FORMAT_2},
    PrachConfigurationIndex.CONFIGURATION_INDEX_41: {'preamble_format': PrachFormat.FORMAT_2},
    PrachConfigurationIndex.CONFIGURATION_INDEX_42: {'preamble_format': PrachFormat.FORMAT_2},
    PrachConfigurationIndex.CONFIGURATION_INDEX_43: {'preamble_format': PrachFormat.FORMAT_2},
}

__PrachConfigurationIndex_TDD_TD : dict[PrachConfigurationIndex, dict[str, int]] = {
    PrachConfigurationIndex.CONFIGURATION_INDEX_0:  {'subframe_number': 9, 'starting symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_1:  {'subframe_number': 9, 'starting symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_2:  {'subframe_number': 9, 'starting symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_3:  {'subframe_number': 9, 'starting symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_28: {'subframe_number': 7, 'starting symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_29: {'subframe_number': 7, 'starting symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_30: {'subframe_number': 7, 'starting symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_31: {'subframe_number': 7, 'starting symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_34: {'subframe_number': 6, 'starting symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_35: {'subframe_number': 6, 'starting symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_36: {'subframe_number': 6, 'starting symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_37: {'subframe_number': 6, 'starting symbol': 7},
    PrachConfigurationIndex.CONFIGURATION_INDEX_40: {'subframe_number': 9, 'starting symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_41: {'subframe_number': 9, 'starting symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_42: {'subframe_number': 9, 'starting symbol': 0},
    PrachConfigurationIndex.CONFIGURATION_INDEX_43: {'subframe_number': 9, 'starting symbol': 0},
}

__PrachConfigurationIndex : dict[frame_defs.FrameType, dict[PrachConfigurationIndex, dict[str, PrachFormat]]] = {frame_defs.FrameType.FDD: __PrachConfigurationIndex_FDD, frame_defs.FrameType.TDD: __PrachConfigurationIndex_TDD}
__PrachConfigurationIndex_TD : dict[frame_defs.FrameType, dict[PrachConfigurationIndex, dict[str, int]]] = {frame_defs.FrameType.FDD: __PrachConfigurationIndex_FDD_TD, frame_defs.FrameType.TDD: __PrachConfigurationIndex_TDD_TD}

def generate_prach(frame_type : frame_defs.FrameType, rach_ConfigCommon : RACH_ConfigCommon) -> np.ndarray:
    assert rach_ConfigCommon.restrictedSetConfig == PrachRestrictedSet.UNRESTRICTED_SET, 'Only unrestricted set is supported'

    preamble_id = np.random.randint(0, rach_ConfigCommon.totalNumberOfRA_Preambles)
    config_generic = rach_ConfigCommon.rach_ConfigGeneric
    fmt = __PrachConfigurationIndex[frame_type][config_generic.prach_ConfigurationIndex]['preamble_format']
    logging.debug('PRACH configuration index: %s, PRACH format: %s, logical root sequence index: %u, zero correlation config zone: %u, set %s, preamble ID:  %u',
                  config_generic.prach_ConfigurationIndex, fmt, rach_ConfigCommon.prach_RootSequenceIndex, config_generic.zeroCorrelationConfigZone, rach_ConfigCommon.restrictedSetConfig, preamble_id)
    preamble_format = __PrachPreamblesFormats[fmt]
    L_RA = preamble_format['L_RA']
    N_CS = __N_CS[preamble_format['f_RA']][rach_ConfigCommon.restrictedSetConfig][config_generic.zeroCorrelationConfigZone]
    if N_CS == 0:
        number_of_preambles_per_cyclic_shift = 1
    else:
        number_of_preambles_per_cyclic_shift = np.floor(L_RA / N_CS)
    assert number_of_preambles_per_cyclic_shift > 0, 'Number of preambles per cyclic shift equal to 0'
    root_sequence_index_offset, cyclic_shift = divmod(preamble_id, number_of_preambles_per_cyclic_shift)
    logical_root_sequence_index = rach_ConfigCommon.prach_RootSequenceIndex + int(root_sequence_index_offset)
    physical_root_sequence_index = __root_sequence_index_mapping[L_RA][logical_root_sequence_index]
    logging.debug('L_RA: %u, N_CS: %u, number of preambles per cyclic shift: %u, logical root sequence index: %u, physical root sequence index: %u, cyclic shift: %u',
                   L_RA, N_CS, number_of_preambles_per_cyclic_shift, logical_root_sequence_index, physical_root_sequence_index, cyclic_shift)

    n = np.mod(np.arange(L_RA) + cyclic_shift, L_RA) + 1
    x = np.exp(1.0j * np.pi * physical_root_sequence_index * n / L_RA)
    y = np.fft.fft(x, L_RA).astype(np.complex64)
    return y
