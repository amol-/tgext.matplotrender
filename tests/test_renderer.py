# -*- coding: utf-8 -*-
from io import BytesIO
import PIL
import matplotlib, matplotlib.figure, numpy
from tg import TGController, expose

import tgext.matplotrender
from .utils import BaseTestClass


def _make_fig():
    fig = matplotlib.figure.Figure(figsize=(9, 6))
    fig.Name = "Sinewave"
    ax = fig.add_subplot(111)
    ax.set_xlabel("angle")
    ax.set_ylabel("amplitude")
    t = numpy.arange(0.0, 2.0, 0.01)
    s1 = numpy.sin(2 * numpy.pi * t)
    ax.plot(t, s1, color="k")
    return fig


class TestRenderer(BaseTestClass):
    class RootController(TGController):
        @expose('matplotfig', render_params=dict(dpi=72))
        def highres(self, *args, **kwargs):
            return dict(fig=_make_fig())

        @expose('matplotfig', render_params=dict(dpi=36))
        def lowres(self, *args, **kwargs):
            return dict(fig=_make_fig())

        @expose('matplotfig')
        def customres(self, *args, **kwargs):
            options = {}
            try:
                options['dpi'] = int(kwargs['dpi'])
            except:
                pass
            return dict(fig=_make_fig(), **options)

    @classmethod
    def setup_app(cls, config):
        config['renderers'] = ['matplotfig']
        tgext.matplotrender.plugme(config)

    def test_render_fig(self):
        r = self.app.get('/highres')
        self.assertEquals(r.content_type, 'image/png')

        img = PIL.Image.open(BytesIO(r.body))
        self.assertEquals(img.size, (648, 432))

    def test_render_fig2(self):
        r = self.app.get('/lowres')
        self.assertEquals(r.content_type, 'image/png')

        img = PIL.Image.open(BytesIO(r.body))
        self.assertEquals(img.size, (324, 216))

    def test_render_custom(self):
        r = self.app.get('/customres?dpi=16')
        self.assertEquals(r.content_type, 'image/png')

        img = PIL.Image.open(BytesIO(r.body))
        self.assertEquals(img.size, (144, 96))

    def test_render_custom_defaults(self):
        r = self.app.get('/customres')
        self.assertEquals(r.content_type, 'image/png')

        img = PIL.Image.open(BytesIO(r.body))
        self.assertEquals(img.size, (900, 600))
