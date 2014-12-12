# coding: utf-8

import os
import click

plugin_dir = os.path.join(os.path.dirname(__file__), 'commands')


class MultiCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(plugin_dir):
            if filename.endswith('.py'):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        ns = {}
        fn = os.path.join(plugin_dir, name + '.py')
        try:
            with open(fn) as f:
                code = compile(f.read(), fn, 'exec')
                eval(code, ns, ns)
        except IOError:
            click.secho("unknown command '%s'" % name, fg='red')
            click.echo(ctx.get_help())
            ctx.abort()
        return ns['cli']


@click.command(cls=MultiCLI)
def main():
    """potte command line interface"""
    pass
