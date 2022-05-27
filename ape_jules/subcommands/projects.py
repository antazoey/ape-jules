from pathlib import Path
import shutil

import click
from ape.cli import ape_cli_context
from ape.logging import LogLevel
from rich.console import Console


@click.group(short_help="Manage smart-contract projects.")
def projects():
    pass


@projects.command("list")
@ape_cli_context()
def _list(cli_ctx):
    """Lists your projects."""

    config = cli_ctx.config_manager.get_config("jules")
    path = Path(config.projects_directory)

    project_map = {}
    all_project_paths = [p for p in path.iterdir() if p.is_dir() and not p.name.startswith(".")]
    for project_path in all_project_paths:

        # Disable warnings for this part.
        level = cli_ctx.logger.level
        cli_ctx.logger.set_level(LogLevel.ERROR)

        with cli_ctx.config_manager.using_project(project_path) as project:
            project_type_str = str(type(project._project).__name__)
            if project_type_str not in project_map:
                project_map[project_type_str] = [project_path]
            else:
                project_map[project_type_str].append(project_path)

        # Restore logger level
        cli_ctx.logger.set_level(level)

    console = Console()
    num_project_types = len(project_map)
    index = 0
    for project_type, project_paths in project_map.items():
        console.print(f"[bold magenta]{project_type}s:[/]")
        for project_path in project_paths:
            console.print(f"- {project_path.name}")

        if index < num_project_types - 1:
            click.echo()

        index += 1


@projects.command()
@ape_cli_context()
@click.argument("project_names", nargs=-1)
def delete(cli_ctx, project_names):
    """Delete a project."""

    if not project_names:
        cli_ctx.abort("No projects given.")

    config = cli_ctx.config_manager.get_config("jules")
    path = Path(config.projects_directory)

    for project_name in project_names:
        project_path = path / project_name
        if not project_path.is_dir():
            cli_ctx.logger.error(f"No project found named '{project_name}'.")

        shutil.rmtree(project_path)
        cli_ctx.logger.success(f"Project '{project_name}' has been deleted.")