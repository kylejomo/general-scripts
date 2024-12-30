#!/Users/username/dev/project01/bin/python

# This script telnets into a server, runs a command, and exits. 
# Requires username and password to be environment variables. 
# This is a quick draft...still plenty to clean up if using it
# for anything real.

import asyncio
import telnetlib3
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def shell(reader, writer):
    rules = [
        ('hostname login:', os.getenv('TELNET_USERNAME', 'default_user')),
        ('hostname login:', os.getenv('TELNET_PASSWORD', 'default_password')),
        #('hostname login:', 'username'),
        #('Password:', 'password123'),
        ('$', 'uname -a'),
        ('$', 'exit'),
    ]

    ruleiter = iter(rules)
    expect, send = next(ruleiter)
    while True:
        try:
            outp = await reader.read(1024)
            if not outp:
                break

            if expect in outp:
                writer.write(send)
                writer.write('\r\n')
                try:
                    expect, send = next(ruleiter)
                except StopIteration:
                    break

            # Log all server output
            logging.info(outp.strip())
        except Exception as e:
            logging.error(f"Error during communication: {e}")
            break

    # EOF
    logging.info("Connection closed")

async def main():
    try:
        reader, writer = await telnetlib3.open_connection('192.168.1.2', 23, shell=shell)
        await writer.protocol.waiter_closed
    except Exception as e:
        logging.error(f"Failed to connect: {e}")

if __name__ == '__main__':
    asyncio.run(main())
