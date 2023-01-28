from django_hosts import patterns, host

host_patterns = patterns(
  '',
    host(r'blog', 'email_tracking.urls', name='email'),
)