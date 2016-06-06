from .renderer import MatPlotLibRenderer

import logging
log = logging.getLogger('tgext.matplotrender')


def plugme(configurator, options=None):
    log.info('Setting up tgext.matplotrender extension...')
    configurator.register_rendering_engine(MatPlotLibRenderer)

    # This is required to be compatible with the
    # tgext.pluggable interface
    return dict(appid='tgext.matplotrender')
