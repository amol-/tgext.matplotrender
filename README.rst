About tgext.matplotrender
-------------------------

.. image:: https://travis-ci.org/amol-/tgext.matplotrender.png
    :target: https://travis-ci.org/amol-/tgext.matplotrender

.. image:: https://coveralls.io/repos/amol-/tgext.matplotrender/badge.png
    :target: https://coveralls.io/r/amol-/tgext.matplotrender

.. image:: https://img.shields.io/:license-mit-blue.svg?style=flat-square
    :target: https://pypi.python.org/pypi/tgext.matplotrender

tgext.matplotrender is a TurboGears2 extension that provides a Rendering Engine
for MatplotLib Figures.

Installing
----------

tgext.matplotrender can be installed from pypi::

    pip install tgext.matplotrender

should just work for most of the users.

Enabling
--------

To enable tgext.matplotrender add the ``matplotfig`` renderer to your
configuration:

.. code-block:: python

    base_config.renderers.append('matplotfig')

and plug the rendering engine inside your ``config/app_cfg.py``:

.. code-block:: python

    import tgext.matplotrender
    tgext.matplotrender.plugme(base_config)

Usage
-----

Using tgext.matplotrender is as simple as exposing an action with
the ``matplotfig`` template and returning the figure itself inside
the ``fig`` key of action returned dictionary.

Given the following figure:

.. code-block:: python

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

It can be exposed through TurboGears actions as:

.. code-block:: python

    class RootController(TGController):
        @expose('matplotfig')
        def figure(self, *args, **kwargs):
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

Any other value provided in the dictionary will be used as
a ``print_figure`` argument in ``matplotlib``