import click
import subprocess

SYSTEMS = {
        'MOM': 'test_MoM.py',
        'INGESTION': 'test_Storm.py',
        'WEB': 'test_Web_processed.py',
        'ANTIVIRUS': 'test_Antivirus_processed.py',
        }

DEFAULT_TAU = {
        "MOM_INGESTION": 15,
        "WEB_ANTIVIRUS": 3
        }


def validate_save(ctx, param, value):
    if value is None:
        return None
    elif value == "":
        raise click.BadParameter("Filename cannot be empty if --save is provided.")
    elif value == "--show":
        raise click.BadParameter("Filename cannot be empty.")
    else:
        return value

@click.command(help = "Run a script for test")
@click.argument('system', type=click.Choice(SYSTEMS.keys(), case_sensitive = False))
@click.argument('method', type=click.Choice(['CBNB_W', 'CBNB_E', 'NBCB_W', 'NBCB_E', 'GCMVL', 'PCMCI', 'PCGCE', 'VARLINGAM', 'TIMINO', 'DYNOTEARS'], case_sensitive=False))
@click.option('--tau', default=None, type=int, help='param_tau_level')
@click.option('--sig', default=0.05, type=float, help='param_sig_level')
@click.option('--dataset', default=1, help='1 or 2 for MOM, WEB and ANTIVIRUS')
@click.option('--save', default=None, type=str, callback=validate_save, help='save the graph with the given filename')
@click.option('--show', is_flag=True, help='show the graph')
def run_test(system, method, tau, sig, dataset, save, show):
    system = system.upper()
    script = SYSTEMS[system]

    if script in ["test_Antivirus_processed.py", "test_Web_processed.py"]:
        default_tau = DEFAULT_TAU["WEB_ANTIVIRUS"]
    else:
        default_tau = DEFAULT_TAU["MOM_INGESTION"]

    if tau is None:
        tau = default_tau

    command = [
            'python3', 
            script, 
            str(method), 
            '--tau', 
            str(tau), 
            '--sig', 
            str(sig), 
            '--dataset', str(dataset)]

    if system == "INGESTION":
        command = command[:-2]

    if save:
        command.extend(['--save', save])
    if show:
        command.extend(['--show'])

    print(command)
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)

if __name__ == '__main__':
    run_test()
