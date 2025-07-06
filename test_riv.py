import riv


class TestRiv:

    def test_calculate_offset_and_bandwidth(self) -> None:
        N_size_BWP = 275

        offset, bandwidth = riv.calculate_offset_and_bandwidth(2750, N_size_BWP)
        assert offset    == 0
        assert bandwidth == 11

        offset, bandwidth = riv.calculate_offset_and_bandwidth(6325, N_size_BWP)
        assert offset    == 0
        assert bandwidth == 24

        offset, bandwidth = riv.calculate_offset_and_bandwidth(10175, N_size_BWP)
        assert offset    == 0
        assert bandwidth == 38

        offset, bandwidth = riv.calculate_offset_and_bandwidth(17600, N_size_BWP)
        assert offset    == 0
        assert bandwidth == 65

        offset, bandwidth = riv.calculate_offset_and_bandwidth(21175, N_size_BWP)
        assert offset    == 0
        assert bandwidth == 78

        offset, bandwidth = riv.calculate_offset_and_bandwidth(28875, N_size_BWP)
        assert offset     == 0
        assert bandwidth == 106

        offset, bandwidth = riv.calculate_offset_and_bandwidth(36300, N_size_BWP)
        assert offset    == 0
        assert bandwidth == 133

        offset, bandwidth = riv.calculate_offset_and_bandwidth(31624, N_size_BWP)
        assert offset    == 0
        assert bandwidth == 162

        offset, bandwidth = riv.calculate_offset_and_bandwidth(24199, N_size_BWP)
        assert offset    == 0
        assert bandwidth == 189

        offset, bandwidth = riv.calculate_offset_and_bandwidth(16499, N_size_BWP)
        assert offset    == 0
        assert bandwidth == 217

        offset, bandwidth = riv.calculate_offset_and_bandwidth(8799, N_size_BWP)
        assert offset    == 0
        assert bandwidth == 245

        offset, bandwidth = riv.calculate_offset_and_bandwidth(1099, N_size_BWP)
        assert offset    == 0
        assert bandwidth == 273

        offset, bandwidth = riv.calculate_offset_and_bandwidth(12928, N_size_BWP)
        assert offset    == 3
        assert bandwidth == 48

    def test_calculate_riv(self) -> None:
        N_size_BWP = 275

        calculated_riv = riv.calculate_riv(0, 11, N_size_BWP)
        assert calculated_riv == 2750

        calculated_riv = riv.calculate_riv(0, 24, N_size_BWP)
        assert calculated_riv == 6325

        calculated_riv = riv.calculate_riv(0, 38, N_size_BWP)
        assert calculated_riv == 10175

        calculated_riv = riv.calculate_riv(0, 65, N_size_BWP)
        assert calculated_riv == 17600

        calculated_riv = riv.calculate_riv(0, 78, N_size_BWP)
        assert calculated_riv == 21175

        calculated_riv = riv.calculate_riv(0, 106, N_size_BWP)
        assert calculated_riv == 28875

        calculated_riv = riv.calculate_riv(0, 133, N_size_BWP)
        assert calculated_riv == 36300

        calculated_riv = riv.calculate_riv(0, 162, N_size_BWP)
        assert calculated_riv == 31624

        calculated_riv = riv.calculate_riv(0, 189, N_size_BWP)
        assert calculated_riv == 24199

        calculated_riv = riv.calculate_riv(0, 217, N_size_BWP)
        assert calculated_riv == 16499

        calculated_riv = riv.calculate_riv(0, 245, N_size_BWP)
        assert calculated_riv == 8799

        calculated_riv = riv.calculate_riv(0, 273, N_size_BWP)
        assert calculated_riv == 1099

        calculated_riv = riv.calculate_riv(3, 48, N_size_BWP)
        assert calculated_riv == 12928
