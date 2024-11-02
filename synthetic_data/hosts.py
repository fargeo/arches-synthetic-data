import re
from django_hosts import patterns, host

host_patterns = patterns(
    "",
    host(re.sub(r"_", r"-", r"synthetic_data"), "synthetic_data.urls", name="synthetic_data"),
)
