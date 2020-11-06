{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

   {% set l = methods | reject('equalto', '__init__') | list %}
   {% block methods -%}
   {% if l %}
   .. rubric:: {{ _('Methods') }}
   .. autosummary::
   {% for item in l %}
      ~{{ name }}.{{ item }}
   {% endfor %}
   {% endif %}
   {%- endblock %}