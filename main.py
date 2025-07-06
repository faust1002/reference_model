#!/usr/bin/env python3

import logging

import frame
import prach


def configure_logging() -> None:
    logging.basicConfig(format = '[%(asctime)s %(levelname)s] %(message)s',
                        encoding = 'utf-8',
                        level = logging.DEBUG)

def main() -> None:
    configure_logging()
    logging.info('Hello')

    uplinkConfigCommon = frame.construct_default_UplinkConfigCommon()
    frame_config = frame.FrameConfig(uplinkConfigCommon)
    _sfn = frame.generate_empty_sfn(frame_config)
    _channel = prach.generate_prach(frame_config.frame_type, uplinkConfigCommon.initialUplinkCommon.rach_ConfigCommon)

    logging.info('Goodbye')

if "__main__" == __name__:
    main()
