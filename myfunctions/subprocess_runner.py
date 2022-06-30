from shlex import join as shjoin
import asyncio

async def run_subprocess(coms, doPrint=False):
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
    if stderr:
        print(shjoin(coms))
        print(f"stderr ({return_code}):\n\033[;31m{stderr.decode('utf-8')}\033[0m")
    return process, stdout, stderr
