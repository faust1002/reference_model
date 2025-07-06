import pytest

import frame
import frame_defs
import prach


class TestFrame:

    def test_default_configuration(self) -> None:
        uplinkConfigCommon = frame.construct_default_UplinkConfigCommon()
        frame_config = frame.FrameConfig(uplinkConfigCommon)
        assert frame_config.frame_type         == frame_defs.FrameType.FDD
        assert frame_config.mu_not             == frame_defs.SubcarrierSpacing.kHz30
        assert frame_config.N_size_mu_not_grid == 273

    def test_initial_uplink_bwp_specific_subcarrier_list_carrier_mismatch(self) -> None:
        scs_SpecificCarrier_kHz15 = frame.SCS_SpecificCarrier(0, frame_defs.SubcarrierSpacing.kHz15, 105)
        scs_SpecificCarrierList = [scs_SpecificCarrier_kHz15]
        frequencyInfoUL = frame.FrequencyInfoUL(scs_SpecificCarrierList)
        bwp = frame.BWP(28875, frame_defs.SubcarrierSpacing.kHz15, frame_defs.CyclicPrefix.NORMAL)
        rach_configCommon = prach.RACH_ConfigCommon()
        bwp_uplinkCommon = frame.BWP_UplinkCommon(bwp, rach_configCommon)
        uplinkConfigCommon = frame.UplinkConfigCommon(frequencyInfoUL, bwp_uplinkCommon)
        with pytest.raises(AssertionError):
            _frame_config = frame.FrameConfig(uplinkConfigCommon)

    def test_two_different_grids_with_the_same_numerology(self) -> None:
        scs_SpecificCarrier = frame.SCS_SpecificCarrier(0, frame_defs.SubcarrierSpacing.kHz15, 106)
        scs_SpecificCarrierList = [scs_SpecificCarrier, scs_SpecificCarrier]
        frequencyInfoUL = frame.FrequencyInfoUL(scs_SpecificCarrierList)
        bwp = frame.BWP(28875, frame_defs.SubcarrierSpacing.kHz15, frame_defs.CyclicPrefix.NORMAL)
        rach_configCommon = prach.RACH_ConfigCommon()
        bwp_uplinkCommon = frame.BWP_UplinkCommon(bwp, rach_configCommon)
        uplinkConfigCommon = frame.UplinkConfigCommon(frequencyInfoUL, bwp_uplinkCommon)
        with pytest.raises(AssertionError):
            _frame_config = frame.FrameConfig(uplinkConfigCommon)

    def test_two_different_grids(self) -> None:
        scs_SpecificCarrier_kHz15 = frame.SCS_SpecificCarrier(0, frame_defs.SubcarrierSpacing.kHz15, 106)
        scs_SpecificCarrier_kHz30 = frame.SCS_SpecificCarrier(0, frame_defs.SubcarrierSpacing.kHz30, 51)
        scs_SpecificCarrierList = [scs_SpecificCarrier_kHz15, scs_SpecificCarrier_kHz30]
        frequencyInfoUL = frame.FrequencyInfoUL(scs_SpecificCarrierList)
        bwp = frame.BWP(28875, frame_defs.SubcarrierSpacing.kHz15, frame_defs.CyclicPrefix.NORMAL)
        rach_configCommon = prach.RACH_ConfigCommon()
        bwp_uplinkCommon = frame.BWP_UplinkCommon(bwp, rach_configCommon)
        uplinkConfigCommon = frame.UplinkConfigCommon(frequencyInfoUL, bwp_uplinkCommon)
        frame_config = frame.FrameConfig(uplinkConfigCommon)
        assert frame_config.frame_type         == frame_defs.FrameType.FDD
        assert frame_config.mu_not             == frame_defs.SubcarrierSpacing.kHz30
        assert frame_config.N_size_mu_not_grid == 51

    def test_initial_uplink_bwp_specific_subcarrier_list_subcarrier_mismatch(self) -> None:
        scs_SpecificCarrier_kHz30 = frame.SCS_SpecificCarrier(0, frame_defs.SubcarrierSpacing.kHz30, 51)
        scs_SpecificCarrierList = [scs_SpecificCarrier_kHz30]
        frequencyInfoUL = frame.FrequencyInfoUL(scs_SpecificCarrierList)
        bwp = frame.BWP(28875, frame_defs.SubcarrierSpacing.kHz15, frame_defs.CyclicPrefix.NORMAL)
        rach_configCommon = prach.RACH_ConfigCommon()
        bwp_uplinkCommon = frame.BWP_UplinkCommon(bwp, rach_configCommon)
        uplinkConfigCommon = frame.UplinkConfigCommon(frequencyInfoUL, bwp_uplinkCommon)
        with pytest.raises(AssertionError):
            _frame_config = frame.FrameConfig(uplinkConfigCommon)

    def test_default_bwp(self) -> None:
        bwp = frame.BWP(1099)
        assert bwp.locationAndBandwidth == 1099
        assert bwp.subcarrierSpacing    == frame_defs.SubcarrierSpacing.kHz30
        assert bwp.cyclicPrefix         == frame_defs.CyclicPrefix.NORMAL
        assert bwp.N_start_BWP          == 0
        assert bwp.N_size_BWP           == 273

    def test_different_locationAndBandwidth_values(self) -> None:
        bwp = frame.BWP(2750)
        assert bwp.N_start_BWP == 0
        assert bwp.N_size_BWP  == 11

        bwp = frame.BWP(6325)
        assert bwp.N_start_BWP == 0
        assert bwp.N_size_BWP  == 24

        bwp = frame.BWP(10175)
        assert bwp.N_start_BWP == 0
        assert bwp.N_size_BWP  == 38

        bwp = frame.BWP(17600)
        assert bwp.N_start_BWP == 0
        assert bwp.N_size_BWP  == 65

        bwp = frame.BWP(21175)
        assert bwp.N_start_BWP == 0
        assert bwp.N_size_BWP  == 78

        bwp = frame.BWP(28875)
        assert bwp.N_start_BWP == 0
        assert bwp.N_size_BWP  == 106

        bwp = frame.BWP(36300)
        assert bwp.N_start_BWP == 0
        assert bwp.N_size_BWP  == 133

        bwp = frame.BWP(31624)
        assert bwp.N_start_BWP == 0
        assert bwp.N_size_BWP  == 162

        bwp = frame.BWP(24199)
        assert bwp.N_start_BWP == 0
        assert bwp.N_size_BWP  == 189

        bwp = frame.BWP(16499)
        assert bwp.N_start_BWP == 0
        assert bwp.N_size_BWP  == 217

        bwp = frame.BWP(8799)
        assert bwp.N_start_BWP == 0
        assert bwp.N_size_BWP  == 245

        bwp = frame.BWP(1099)
        assert bwp.N_start_BWP == 0
        assert bwp.N_size_BWP  == 273

        bwp = frame.BWP(12928)
        assert bwp.N_start_BWP == 3
        assert bwp.N_size_BWP  == 48

    def test_locationAndBandwidth_range(self) -> None:
        with pytest.raises(AssertionError):
            _bwp = frame.BWP(0, frame_defs.SubcarrierSpacing.kHz30)

        with pytest.raises(AssertionError):
            _bwp = frame.BWP(37950, frame_defs.SubcarrierSpacing.kHz30)

        _bwp = frame.BWP(1099, frame_defs.SubcarrierSpacing.kHz30)
