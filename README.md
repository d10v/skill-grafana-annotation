# opsdroid skill grafana-annotation

A skill for opsdroid to create and view Grafana annotations

# Requirements

 * Grafana instance
 * Create an API token with "Editor" role at `Configuration / API Keys` and paste `Bearer ...` to opsdroid configuration

# Configuration

``` yaml
  - name: grafana-annotation
    repo: "https://github.com/dimamedvedev/skill-grafana-annotation.git"
    grafana_url: "https://grafana.example.com"
    grafana_auth: "Bearer ..."
```

# Usage

#### `annotations (tag1 tag2)`

#### `annotate some text (tag1 tag2)`
