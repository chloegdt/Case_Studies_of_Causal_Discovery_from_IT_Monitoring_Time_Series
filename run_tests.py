import click
import subprocess

SCRIPT_MAP = {
        'MOM': 'test_MoM.py',
        'INGESTION': 'test_Storm.py',
        'WEB': 'test_Web_processed.py',
        'ANTIVIRUS': 'test_Antivirus_processed.py',
        }

DEFAULT_TAU = {
        "MOM_INGESTION": 15,
        "WEB_ANTIVIRUS": 3
        }

@click.command(help = "Run a script for test")
@click.argument('dataset', type=click.Choice(SCRIPT_MAP.keys(), case_sensitive = False))
@click.argument('method', type=click.Choice(['CBNB_W', 'CBNB_E', 'NBCB_W', 'NBCB_E', 'GCMVL', 'PCMCI', 'PCGCE', 'VARLINGAM', 'TIMINO', 'DYNOTEARS'], case_sensitive=False))
@click.option('--tau', default=None, type=int, help='param_tau_level')
@click.option('--sig', default=0.05, type=float, help='param_sig_level')
@click.option('--param_dataset', default=1, help='1 or 2 for MOM, WEB and ANTIVIRUS')

def run_test(dataset, method, tau, sig, param_dataset):
    dataset = dataset.upper()
    script = SCRIPT_MAP[dataset]

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
            '--param_dataset', str(param_dataset)]

    if dataset == "INGESTION":
        command = command[:-2]

    print(command)
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)
    #print(result.stderr)

if __name__ == '__main__':
    run_test()
