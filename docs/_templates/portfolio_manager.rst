{{ name | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
   :inherited-members:
   :undoc-members:

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
