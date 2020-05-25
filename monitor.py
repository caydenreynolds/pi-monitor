from subprocess import run

def main():
    result = run('sar', shell=True, capture_output=True)
    for line in result.stdout.split('\n'):
        print(line + "LINE_END")