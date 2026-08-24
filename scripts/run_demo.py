"""Interactive CLI demonstration of WeatherGPT multilingual reasoning agent."""

import asyncio

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from weathergpt.agent.engine import weather_agent
from weathergpt.core.models import ChatRequest


async def run_cli_demo():
    console = Console()
    console.print(
        Panel.fit(
            "[bold cyan]🌦️ WeatherGPT Indic Multilingual Interactive Terminal[/bold cyan]\n"
            "[dim]Demonstrating LLM Function-Calling over IMD, Open-Meteo, GFS & GKMS in EN, HI, and AS[/dim]",
            border_style="cyan",
        )
    )

    demo_queries = [
        ("English", "What is the 7-day forecast and current weather for Guwahati?"),
        ("Hindi", "धान की फसल में सिंचाई और कीटनाशक छिड़काव की क्या सलाह है लखनऊ के लिए?"),
        ("Assamese", "কামৰূপ আৰু গুৱাহাটীৰ বাবে বতৰ বিজ্ঞান কেন্দ্ৰৰ কিবা সতৰ্কবাৰ্তা আছেনে?"),
        ("Climate Q&A", "Explain what is Bordoisila in Assam meteorology."),
    ]

    for lang_label, query in demo_queries:
        console.print(f"\n[bold yellow]User ({lang_label}):[/bold yellow] {query}")
        req = ChatRequest(message=query)
        resp = await weather_agent.chat(req)

        # Tools Table
        if resp.tool_calls:
            tool_table = Table(title="Executed Tools", show_header=True, header_style="bold magenta")
            tool_table.add_column("Tool Name", style="cyan")
            tool_table.add_column("Arguments", style="dim")
            tool_table.add_column("Latency", justify="right", style="green")

            for t in resp.tool_calls:
                tool_table.add_row(t.tool_name, str(t.arguments), f"{t.latency_ms} ms")
            console.print(tool_table)

        console.print(Panel(resp.reply, title=f"WeatherGPT Response ({resp.detected_language.upper()})", border_style="green"))


if __name__ == "__main__":
    asyncio.run(run_cli_demo())
