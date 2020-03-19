{{ name | escape | underline}}

For methods of this class, see :doc:`gs_quant.base.Priceable`

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

   {% block attributes %}
   .. rubric:: Properties
   {% if attributes %}
   {% for item in attributes %}
   {% if item not in ('asset_class', 'type', 'PROVIDER') %}
   .. autoattribute:: {{ item }}
   {% endif %}
   {%- endfor %}
   {% endif %}
   {% endblock %}