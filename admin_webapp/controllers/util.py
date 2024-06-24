"""Helpers for :mod:`accounts.controllers`."""
from typing import Any
from math import ceil

from wtforms.widgets import ListWidget, CheckboxInput, Select, \
    html_params
from wtforms import SelectField, SelectMultipleField, Form
from markupsafe import Markup

class MultiCheckboxField(SelectMultipleField):
    """Multi-select with checkbox inputs."""

    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

    def __call__(self, ul_class: str = '', **kwargs: Any) -> str:
        """Render the multi-checkbox field."""
        kwargs.setdefault('type', 'checkbox')
        li_class = kwargs.pop('li_class')
        field_id = kwargs.pop('id', self.id)
        html = ['<ul %s>' % html_params(id=field_id, class_=ul_class)]
        for value, label, checked in self.iter_choices():
            choice_id = '%s-%s' % (field_id, value)
            options = dict(kwargs, name=self.name, value=value, id=choice_id)
            if checked:
                options['checked'] = 'checked'
            html.append(f'<li class="{li_class}">')
            html.append(f'<input {html_params(**options)} />')
            html.append(f'<label for="{choice_id}">{label}</label></li>')
            html.append('</li>')
        html.append('</ul>')
        return ''.join(html)


class OptGroupSelectWidget(Select):
    """Select widget with optgroups."""

    def __call__(self, field: SelectField, **kwargs: Any) -> Markup:
        """Render the `select` element with `optgroup`s."""
        kwargs.setdefault('id', field.id)
        if self.multiple:
            kwargs['multiple'] = True
        html = [f'<select {html_params(name=field.name, **kwargs)}>']
        html.append('<option></option>')
        for group_label, items in field.choices:
            html.append('<optgroup %s>' % html_params(label=group_label))
            for value, label in items:
                option = self.render_option(value, label, value == field.data)
                html.append(option)
            html.append('</optgroup>')
        html.append('</select>')
        return Markup(''.join(html))


class OptGroupSelectField(SelectField):
    """A select field with optgroups."""

    widget = OptGroupSelectWidget()

    def pre_validate(self, form: Form) -> None:
        """Don't forget to validate also values from embedded lists."""
        for group_label, items in self.choices:
            for value, label in items:
                if value == self.data:
                    return
        raise ValueError(self.gettext('Not a valid choice'))
    

# This code is stolen from flask_sqlalchemy
class Pagination(object):
    """Internal helper class returned by :meth:`BaseQuery.paginate`.  You
    can also construct it from any other SQLAlchemy query object if you are
    working with other libraries.  Additionally it is possible to pass `None`
    as query object in which case the :meth:`prev` and :meth:`next` will
    no longer work.
    """

    def __init__(self, query, page, per_page, total, items):
        #: the unlimited query object that was used to create this
        #: pagination object.
        self.query = query
        #: the current page number (1 indexed)
        self.page = page
        #: the number of items to be displayed on a page.
        self.per_page = per_page
        #: the total number of items matching the query
        self.total = total
        #: the items for the current page
        self.items = items

    @property
    def pages(self):
        """The total number of pages"""
        if self.per_page == 0:
            pages = 0
        else:
            pages = int(ceil(self.total / float(self.per_page)))
        return pages

    def prev(self, error_out=False):
        """Returns a :class:`Pagination` object for the previous page."""
        assert self.query is not None, 'a query object is required ' \
                                       'for this method to work'
        return self.query.paginate(self.page - 1, self.per_page, error_out)

    @property
    def prev_num(self):
        """Number of the previous page."""
        if not self.has_prev:
            return None
        return self.page - 1

    @property
    def has_prev(self):
        """True if a previous page exists"""
        return self.page > 1

    def next(self, error_out=False):
        """Returns a :class:`Pagination` object for the next page."""
        assert self.query is not None, 'a query object is required ' \
                                       'for this method to work'
        return self.query.paginate(self.page + 1, self.per_page, error_out)

    @property
    def has_next(self):
        """True if a next page exists."""
        return self.page < self.pages

    @property
    def next_num(self):
        """Number of the next page"""
        if not self.has_next:
            return None
        return self.page + 1

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        """Iterates over the page numbers in the pagination.  The four
        parameters control the thresholds how many numbers should be produced
        from the sides.  Skipped page numbers are represented as `None`.
        This is how you could render such a pagination in the templates:

        .. sourcecode:: html+jinja

            {% macro render_pagination(pagination, endpoint) %}
              <div class=pagination>
              {%- for page in pagination.iter_pages() %}
                {% if page %}
                  {% if page != pagination.page %}
                    <a href="{{ url_for(endpoint, page=page) }}">{{ page }}</a>
                  {% else %}
                    <strong>{{ page }}</strong>
                  {% endif %}
                {% else %}
                  <span class=ellipsis>…</span>
                {% endif %}
              {%- endfor %}
              </div>
            {% endmacro %}
        """
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num
