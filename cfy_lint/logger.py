# Copyright © 2023 Dell Inc. or its subsidiaries. All Rights Reserved.

import logging
logger = logging.getLogger('cfy-lint')
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
streamformatter = logging.Formatter(fmt='%(levelname)-7s: %(message)s')
stream_handler.setFormatter(streamformatter)
