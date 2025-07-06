import logging
from dataclasses import dataclass

import numpy as np

import frame_defs
import prach
import riv


@dataclass
class SCS_SpecificCarrier:
    offsetToCarrier : int
    subcarrierSpacing : frame_defs.SubcarrierSpacing
    carrierBandwidth : int

@dataclass
class BWP:
    locationAndBandwidth : int
    subcarrierSpacing : frame_defs.SubcarrierSpacing
    cyclicPrefix : frame_defs.CyclicPrefix

    N_start_BWP : int
    N_size_BWP : int

    def __init__(self, locationAndBandwidth = 0, subcarrierSpacing : frame_defs.SubcarrierSpacing = frame_defs.SubcarrierSpacing.kHz30, cyclicPrefix : frame_defs.CyclicPrefix = frame_defs.CyclicPrefix.NORMAL):
        assert 1 <= locationAndBandwidth <= 37949, f'Provided locationAndBandwidth ({locationAndBandwidth}) outside the allowed range (1, 37949)'
        self.locationAndBandwidth = locationAndBandwidth
        self.N_start_BWP, self.N_size_BWP = riv.calculate_offset_and_bandwidth(self.locationAndBandwidth, 275)
        self.subcarrierSpacing = subcarrierSpacing
        self.cyclicPrefix = cyclicPrefix

@dataclass
class FrequencyInfoUL:
    scs_SpecificCarrierList : list[SCS_SpecificCarrier]

@dataclass
class BWP_UplinkCommon:
    genericParameters : BWP
    rach_ConfigCommon : prach.RACH_ConfigCommon

@dataclass
class UplinkConfigCommon:
    frequencyInfoUL : FrequencyInfoUL
    initialUplinkCommon : BWP_UplinkCommon

def construct_default_UplinkConfigCommon(bandwidth : frame_defs.Bandwidth = frame_defs.Bandwidth.MHz100, subcarrierSpacing : frame_defs.SubcarrierSpacing = frame_defs.SubcarrierSpacing.kHz30, cyclicPrefix : frame_defs.CyclicPrefix = frame_defs.CyclicPrefix.NORMAL) -> UplinkConfigCommon:
    # For time being let us assume that initial Uplink BWP occupies the entire available cell bandwidth
    num_rbs = frame_defs.get_max_number_of_rbs(bandwidth, subcarrierSpacing)

    scs_SpecificCarrier = SCS_SpecificCarrier(0, subcarrierSpacing, num_rbs)
    scs_SpecificCarrierList = [scs_SpecificCarrier]
    frequencyInfoUL = FrequencyInfoUL(scs_SpecificCarrierList)

    locationAndBandwidth = riv.calculate_riv(0, num_rbs, 275)
    bwp = BWP(locationAndBandwidth, subcarrierSpacing, cyclicPrefix)

    rach_configCommon = prach.RACH_ConfigCommon()
    bwp_UplinkCommon = BWP_UplinkCommon(bwp, rach_configCommon)

    uplinkConfigCommon = UplinkConfigCommon(frequencyInfoUL, bwp_UplinkCommon)
    return uplinkConfigCommon

@dataclass
class FrameConfig:
    frame_type : frame_defs.FrameType
    uplinkConfigCommon : UplinkConfigCommon

    mu_not : frame_defs.SubcarrierSpacing
    N_size_mu_not_grid : int
    fft_size : int

    def __init__(self, uplinkConfigCommon : UplinkConfigCommon, frame_type : frame_defs.FrameType = frame_defs.FrameType.FDD):
        initialBWP = uplinkConfigCommon.initialUplinkCommon.genericParameters
        known_mus = []
        scs_SpecificCarrierList = uplinkConfigCommon.frequencyInfoUL.scs_SpecificCarrierList
        for scs_SpecificCarrier in scs_SpecificCarrierList:
            if scs_SpecificCarrier.subcarrierSpacing == initialBWP.subcarrierSpacing:
                assert initialBWP.N_size_BWP <= scs_SpecificCarrier.carrierBandwidth, f'BWP size ({initialBWP.N_size_BWP}) larger than carrier bandwidth ({scs_SpecificCarrier.carrierBandwidth})'
            assert scs_SpecificCarrier.subcarrierSpacing not in known_mus, f'Subcarrier spacing {scs_SpecificCarrier.subcarrierSpacing} already configured'
            known_mus.append(scs_SpecificCarrier.subcarrierSpacing)
        assert initialBWP.subcarrierSpacing in known_mus, f'Subcarrier spacing for initial UL BWP ({initialBWP.subcarrierSpacing}) not in SpecificCarrierList'
        self.mu_not = max(mu for mu in known_mus)
        self.N_size_mu_not_grid = next((scs_SpecificCarrier.carrierBandwidth for scs_SpecificCarrier in scs_SpecificCarrierList if scs_SpecificCarrier.subcarrierSpacing == self.mu_not), 0)
        self.fft_size = frame_defs.calculate_fft_size(self.N_size_mu_not_grid)

        self.uplinkConfigCommon = uplinkConfigCommon
        self.frame_type = frame_type

def generate_empty_sfn(cfg : FrameConfig) -> np.ndarray:
    logging.debug('Generating an empty sfn. Frame type: %s, number of RBs: %d, subcarrier spacing: %s',
                  cfg.frame_type, cfg.N_size_mu_not_grid, cfg.mu_not)
    N_subframe_slot = 1 << cfg.mu_not.value
    total_number_of_symbols = frame_defs.N_slot_symb * N_subframe_slot * frame_defs.NUMBER_SUBFRAMES_PER_SFN
    return np.ndarray((cfg.fft_size, total_number_of_symbols), dtype = np.complex64)
