from shlex import join as shjoin
import asyncio


class SubprocessError(Exception):
    def __init__(self, err_code, message):
        self.err = err_code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.err} -> {self.message}"


async def run_subprocess(coms, doPrint=False, shell=None):
    if shell:
        process = await asyncio.create_subprocess_shell(
            coms, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT
        )
    else:
        process = await asyncio.create_subprocess_exec(
            *coms, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT
        )
    stdout, stderr = await process.communicate()
    return_code = process.returncode
    if return_code == 0:
        if doPrint:
            print(shjoin(coms))
            print(f"stdout ({return_code}):\n\033[;32m{stdout.decode('utf-8')}\033[0m")
    else:
        print(shjoin(coms))
        print(f"stdout ({return_code}):\n\033[;31m{stdout.decode('utf-8')}\033[0m")
        raise SubprocessError(return_code, stdout.decode("utf-8"))
    if stderr:
        print(shjoin(coms))
        print(f"stderr ({return_code}):\n\033[;31m{stderr.decode('utf-8')}\033[0m")
        raise SubprocessError(return_code, stdout.decode("utf-8"))
    return process, stdout, stderr
