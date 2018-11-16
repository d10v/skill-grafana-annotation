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

tags in parenthesis are optional

#### `annotate some text (tag1 tag2)`
> user: annotate important event started (prod)
>
> opsdroid: Creating annotation, Grafana replies: '{'id': 1, 'message': 'Annotation added'}'

#### `annotations (tag1 tag2)`
> user: annotations (prod)
>
> opsdroid: Getting annotaions
>
> opsdroid: 2018-11-16T12:30:41+00:00 (seconds ago) important event started (prod dima)
