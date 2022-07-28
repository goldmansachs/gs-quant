{{ name | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

   {% block methods %}
   {% if methods %}
   .. rubric:: Methods
   {% for item in methods %}
   {% if item not in ('has_default',) %}
   .. automethod:: {{ item }}
   {% endif %}
   {%- endfor %}
   {% endif %}
   {% endblock %}



   {% block attributes %}
   {% if attributes %}
   .. rubric:: Properties
   {% for item in attributes %}
   {% if item not in () %}
   .. autoattribute:: {{ item }}
   {% endif %}
   {%- endfor %}
   {% endif %}
   {% endblock %}