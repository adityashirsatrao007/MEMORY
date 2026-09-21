# Datadog Monitoring — Free 2 Years

## Setup
```bash
# Claim at: https://www.datadoghq.com/student/
# Get API key from: https://app.datadoghq.com/account/settings#api

# Save key
echo "DD_API_KEY=<your-key>" >> ~/.config/global-apikeys/keys.env

# Install
pip install datadog
```

## Initialize
```python
import os
from datadog import initialize, statsd

initialize(api_key=os.environ.get('DD_API_KEY'))
```

## Track MEMORY Metrics
```python
# Agent sessions
statsd.increment('memory.agent.session.start')
statsd.increment('memory.agent.session.end')

# Token usage
statsd.histogram('memory.agent.tokens.used', token_count, tags=['model:gemini-flash'])

# Vector DB
statsd.gauge('memory.vector_db.chunks', col.count())
statsd.timing('memory.vector_db.search_ms', elapsed_ms, tags=['query_type:semantic'])

# Module loads
statsd.increment('memory.module.loaded', tags=['module:04-security'])

# Errors
statsd.increment('memory.error', tags=['type:oom', 'module:03-ml'])
```

## Custom Dashboard
```python
# Create via API or UI at app.datadoghq.com/dashboard
# Key widgets:
# - Agent sessions (count)
# - Token usage (histogram)
# - Vector DB search latency (timer)
# - Module load frequency (counter)
# - Error rate by type (counter)
```

## Alerts
```python
# Set up in Datadog UI:
# - Alert if vector DB search > 500ms
# - Alert if token usage > 25K per session
# - Alert if error rate > 5% of sessions
# - Alert if module load fails
```

## Student Benefits
- Pro account free for 2 years
- 10 servers monitored
- APM, logs, traces included
- Custom dashboards
