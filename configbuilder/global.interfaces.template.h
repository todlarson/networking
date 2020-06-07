replace: iterfaces {
{% if ACCSW1 %}
    xe-0/0/0
{% endif %}
{% if ACCSW2 %}
    xe-0/0/1
{% endif %}
{% if ACCSW3 %}
    xe-0/0/2
{% endif %}
}
