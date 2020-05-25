from subprocess import run

def main():
    result = run('sar', shell=True, capture_output=True, text=True)
    lines = result.stdout.split('\n')
    for i in range(len(lines)):
        if i > 4:
            print(lines[i])

if __name__ == "__main__":
    main()