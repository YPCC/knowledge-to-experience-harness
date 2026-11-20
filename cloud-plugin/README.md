# Knowledge-to-Experience Cloud Plugin

Cloud-ready MCP (Model Context Protocol) plugin that turns any source material into short educational videos.

## What it does

Given:
- **Source**: any GitHub URL, paper URL, document text, or raw content
- **Instruction** (optional): natural-language description of the videos you want

It generates videos. By default it produces:
- **Executive / Business Overview**
- **Technical Deep Dive / Architecture**

You can override the defaults with the instruction (keywords: executive, business, technical, architecture, dialogue, how it works, walkthrough).

Outputs: short MP4s, timestamped transcripts, metadata JSON, and evaluation notes — written to an output directory.

## Usage as MCP Server

### Local (stdio — Claude Desktop, Cursor, etc.)

```bash
cd knowledge-to-experience-harness
pip install -r cloud-plugin/requirements.txt
python cloud-plugin/server.py
```

Add to your MCP client config:

```json
{
  "mcpServers": {
    "k2e-harness": {
      "command": "python",
      "args": ["/absolute/path/to/knowledge-to-experience-harness/cloud-plugin/server.py"]
    }
  }
}
```

Then ask: "Generate executive and technical videos from https://github.com/YPCC/cms-policy-as-code"

### Cloud / HTTP (SSE)

```bash
fastmcp run cloud-plugin/server.py --transport sse --port 8000
```

Or with Docker:

```bash
docker build -f cloud-plugin/Dockerfile -t k2e-cloud-plugin .
docker run -p 8000:8000 -v $(pwd)/generated:/data/generated k2e-cloud-plugin
```

## Tools

| Tool | Description |
|------|-------------|
| `generate_videos` | Main entry point. `source` + optional `instruction`. |
| `list_default_video_types` | Shows the default executive + technical set and available keywords. |

## Configuration

- Set `K2E_OUTPUT_DIR` to control where artifacts are written (default `/tmp/k2e-generated` or `/data/generated` in Docker).
- LLM and TTS providers are optional; the plugin falls back to the harness's structured script + title-card assembly when they are not configured.
- See the root `docs/llm-configuration.md` for full LLM setup.

## Notes

This plugin reuses the modular stages already present in `scripts/generation_stages.py` and `scripts/evaluation.py`. It is designed to be dropped into any MCP-compatible agent environment or deployed as a cloud service.
