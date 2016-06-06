# -*- coding: utf-8 -*-
from io import BytesIO

from tg.renderers.base import RendererFactory

try:
    from matplotlib.backends.backend_agg import FigureCanvasAgg
except ImportError:
    FigureCanvasAgg = None


class MatPlotLibRenderer(RendererFactory):
    engines = {'matplotfig': {'content_type': 'image/png'}}
    with_tg_vars = False

    @classmethod
    def create(cls, config, app_globals):
        if FigureCanvasAgg is None:  # pragma: no cover
            return None
        return {'matplotfig': cls.render_fig}

    @staticmethod
    def render_fig(template_name, template_vars, **kwargs):
        canvas = FigureCanvasAgg(_get_fig(template_vars))
        rendered_fig = BytesIO()
        canvas.print_figure(rendered_fig, **_get_render_opts(kwargs, template_vars))
        return rendered_fig.getvalue()


def _get_fig(result):
    if isinstance(result, dict):
        fig = result['fig']
        del result['fig']
        return fig
    else:
        return result


def _get_render_opts(render_opts, result):
    if isinstance(result, dict):
        render_opts.update(result)
    return render_opts