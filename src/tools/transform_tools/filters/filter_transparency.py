# Licensed under GPL3 https://github.com/maoschanz/drawing/blob/master/LICENSE

import cairo
from gi.repository import Gdk
from .abstract_filter import AbstractFilter

class FilterTransparency(AbstractFilter):
	__gtype_name__ = 'FilterTransparency'

	def __init__(self, filter_id, filters_tool, *args):
		super().__init__(filter_id, filters_tool)
		self._label, self._spinbtn = self._tool.bar.add_spinbtn( \
		                       _("Transparency"), [0, 0, 100, 5, 10, 0], 3, '%')
		# it's [value, lower, upper, step_increment, page_increment, page_size]

	def get_preferred_minimum_width(self):
		return self._label.get_preferred_width()[0] + \
		     self._spinbtn.get_preferred_width()[0]

	def set_filter_compact(self, is_active, is_compact):
		self._label.set_visible(is_active and not is_compact)
		self._spinbtn.set_visible(is_active)

	def build_filter_op(self):
		options = {
			'percent': self._spinbtn.get_value() / 100
		}
		return options

	def do_filter_operation(self, source_pixbuf, operation):
		"""Create a temp_pixbuf from a surface of the same size, whose cairo
		context is painted (with alpha) using the original surface."""
		percent = operation['percent']
		surface = Gdk.cairo_surface_create_from_pixbuf(source_pixbuf, 0, None)
		scale = self._tool.scale_factor()
		surface.set_device_scale(scale, scale)
		width = source_pixbuf.get_width()
		height = source_pixbuf.get_height()
		new_surface = cairo.ImageSurface(cairo.Format.ARGB32, width, height)
		cairo_context = cairo.Context(new_surface)
		cairo_context.set_source_surface(surface)

		cairo_context.set_operator(cairo.Operator.SOURCE)
		cairo_context.paint_with_alpha(1.0 - percent)
		# TODO if percent is negative, paint first the normal version, and then
		# paint with [-1 * percent] alpha the pixbuf

		new_pixbuf = Gdk.pixbuf_get_from_surface(new_surface, 0, 0, \
		                      new_surface.get_width(), new_surface.get_height())
		self._tool.get_image().set_temp_pixbuf(new_pixbuf)

	############################################################################
################################################################################

